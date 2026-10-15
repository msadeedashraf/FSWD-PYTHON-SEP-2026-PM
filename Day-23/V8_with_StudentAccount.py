# CLASSROOM NOTES — V8 ABSTRACTION
# PROBLEM: New products must not accidentally inherit an incorrect policy.
# SOLUTION: abstract BankAccount requires withdraw(amount) in every child.
# TRY: BankAccount("Ali", 1000, "123", "a@b.ca") -> TypeError.
# TRY: class StudentAccount(BankAccount): pass; then instantiate -> TypeError.
# FIX: implement withdraw(self, amount) in StudentAccount.
# NOTE: A base class may still provide shared concrete methods such as deposit.

"""SADEED NATIONAL BANK — Version 8: ABSTRACTION.

Teaching goal: preserve all V7/V6 behavior and add an abstract withdrawal contract.
Savings and Business retain their V6 policies. Chequing explicitly implements
the same $2-fee policy previously inherited from BankAccount.
Encapsulated account state, SQLite persistence, menus and statements remain.
Run: python V8_with_StudentAccount.py
Uses bank_v8.db; V5 remains untouched.
"""
from abc import ABC, abstractmethod
from datetime import datetime
import random
import sqlite3

DB_FILE = "bank_v8_student_extended.db"


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            account_title TEXT NOT NULL,
            balance INTEGER NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            is_active INTEGER NOT NULL,
            account_type TEXT NOT NULL DEFAULT 'BankAccount',
            overdraft_limit INTEGER NOT NULL DEFAULT 0,
            student_age INTEGER,
            student_daily_limit INTEGER NOT NULL DEFAULT 500
        )""")
        # Migration for students who previously ran this extended version.
        columns = {row[1] for row in conn.execute("PRAGMA table_info(accounts)")}
        if "student_age" not in columns:
            conn.execute("ALTER TABLE accounts ADD COLUMN student_age INTEGER")
        if "student_daily_limit" not in columns:
            conn.execute("ALTER TABLE accounts ADD COLUMN student_daily_limit INTEGER NOT NULL DEFAULT 500")
        # Student daily usage survives application restarts.
        conn.execute("""CREATE TABLE IF NOT EXISTS student_withdrawals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            withdrawal_date TEXT NOT NULL,
            amount INTEGER NOT NULL CHECK(amount > 0),
            FOREIGN KEY(account_number) REFERENCES accounts(account_number)
        )""")


class BankAccount(ABC):
    """Parent class: common account data and common operations."""

    bank_name = "SADEED NATIONAL BANK"
    account_type = "BankAccount"

    def __init__(self, account_title, balance, phone, email,
                 creation_date=None, is_active=False, account_number=None):
        self.__account_number = account_number or self.generate_iban()
        self.account_title = account_title
        # Reject invalid balances instead of silently truncating decimals.
        if isinstance(balance, bool) or not isinstance(balance, (int, float)) or not float(balance).is_integer():
            raise ValueError("Balance must be a whole-dollar amount.")
        self.__balance = int(balance)
        self.phone = phone
        self.email = email
        self.transactions = []  # Session-only history, as in Version 4.
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__is_active = bool(is_active)

    # Account number is assigned only during construction/reconstruction.
    @property
    def account_number(self):
        return self.__account_number

    # Account status is also read-only to callers. Use activate/deactivate.
    @property
    def is_active(self):
        return self.__is_active

    # ENCAPSULATION: callers can READ balance but cannot assign to it.
    # __balance is name-mangled. It is a guardrail, not absolute security.
    @property
    def balance(self):
        return self.__balance

    # Protected-by-convention helper: subclasses use this ONLY after
    # validating a transaction. This centralizes balance mutations.
    def _change_balance(self, delta):
        if isinstance(delta, bool) or not isinstance(delta, (int, float)) or not float(delta).is_integer():
            raise ValueError("Balance changes must use whole-dollar amounts.")
        self.__balance += int(delta)

    def get_timestamp(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d"), now.strftime("%I:%M:%S %p")

    def generate_iban(self):
        # Classroom demonstration only: not a real validated IBAN.
        return f"CA{random.randint(10,99)}SNBC{random.randint(10000000,99999999)}"

    def save_to_db(self):
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("""INSERT INTO accounts
                (account_number, account_title, balance, phone, email,
                 creation_date, is_active, account_type, overdraft_limit, student_age, student_daily_limit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(account_number) DO UPDATE SET
                    account_title=excluded.account_title,
                    balance=excluded.balance, phone=excluded.phone,
                    email=excluded.email, creation_date=excluded.creation_date,
                    is_active=excluded.is_active, account_type=excluded.account_type,
                    overdraft_limit=excluded.overdraft_limit,
                    student_age=excluded.student_age,
                    student_daily_limit=excluded.student_daily_limit""",
                (self.account_number, self.account_title, self.balance,
                 self.phone, self.email, self.creation_date, int(self.is_active),
                 self.account_type, getattr(self, "overdraft_limit", 0),
                 getattr(self, "student_age", None), getattr(self, "daily_withdrawal_limit", 500)))

    def activate_account(self):
        self.__is_active = True
        self.save_to_db()
        print("Account activated.")

    def deactivate_account(self):
        self.__is_active = False
        self.save_to_db()
        print("Account deactivated.")

    def record_transaction(self, kind, money_in, money_out):
        date, time = self.get_timestamp()
        self.transactions.append({"type": kind, "date": date, "time": time,
                                  "money_in": money_in, "money_out": money_out,
                                  "balance": self.balance})

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or not float(amount).is_integer():
            print("Amount must be a whole-dollar number.")
            return
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        self._change_balance(amount)
        self.save_to_db()
        self.record_transaction("Deposit", amount, 0)
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")

    # ABSTRACTION: every concrete bank product MUST define a withdrawal rule.
    # BankAccount describes the contract, not the product-specific policy.
    @abstractmethod
    def withdraw(self, amount):
        """Withdraw money according to this product's banking rules."""
        pass

    def account_info(self):
        print("\n========== ACCOUNT INFO ==========")
        for label, value in (
            ("Account Type", self.account_type),
            ("Account Number", self.account_number),
            ("Account Title", self.account_title),
            ("Phone", self.phone), ("Email", self.email),
            ("Balance", f"${self.balance:.2f}"),
            ("Created", self.creation_date),
            ("Active", "Yes" if self.is_active else "No"),
        ):
            print(f"{label:<18}: {value}")
        if isinstance(self, BusinessAccount):
            print(f"{'Overdraft Limit':<18}: ${self.overdraft_limit:.2f}")
        if isinstance(self, StudentAccount):
            print(f"{'Student Age':<18}: {self.student_age}")
            print(f"{'Daily Limit':<18}: ${self.daily_withdrawal_limit:.2f}")
            print(f"{'Withdrawn Today':<18}: ${self.withdrawn_today():.2f}")
        print("==================================")

    def show_statement(self):
        print(f"\n{self.bank_name} — {self.account_title} ({self.account_type})")
        if not self.transactions:
            print("No transactions for this session. (History is not yet stored in SQLite.)")
            return
        print(f"{'Date':<12} {'Time':<12} {'Description':<14} {'In':>10} {'Out':>10} {'Balance':>12}")
        for tx in self.transactions:
            print(f"{tx['date']:<12} {tx['time']:<12} {tx['type']:<14} "
                  f"{tx['money_in']:>10.2f} {tx['money_out']:>10.2f} {tx['balance']:>12.2f}")

    @classmethod
    def open_account(cls):
        print(f"\nOpening {cls.account_type} at {cls.bank_name}")
        name = input("Account title: ").strip()
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()
        if not name or not phone or not email:
            print("Name, phone and email are required.")
            return None
        with sqlite3.connect(DB_FILE) as conn:
            found = conn.execute("SELECT account_number FROM accounts WHERE phone = ?", (phone,)).fetchone()
        if found:
            print(f"Phone already registered under account {found[0]}.")
            return None
        balance = read_amount("Opening deposit (Enter for 0): ", allow_blank=True)
        if balance is None:
            return None
        if cls is StudentAccount:
            try:
                age = int(input("Student age (16–25): ").strip())
            except ValueError:
                print("Enter a valid age.")
                return None
            if not 16 <= age <= 25:
                print("Student Accounts are available for ages 16 through 25.")
                return None
            account = cls(name, balance, phone, email, student_age=age)
        elif cls is BusinessAccount:
            limit = read_amount("Approved overdraft limit (Enter for 0): ", allow_blank=True)
            if limit is None:
                return None
            account = cls(name, balance, phone, email, overdraft_limit=limit)
        else:
            account = cls(name, balance, phone, email)
        account.save_to_db()
        print(f"Created {account.account_type}: {account.account_number} (inactive)")
        return account

    @classmethod
    def get_account_by_number(cls, number):
        with sqlite3.connect(DB_FILE) as conn:
            row = conn.execute("""SELECT account_number, account_title, balance,
                phone, email, creation_date, is_active, account_type, overdraft_limit, student_age, student_daily_limit
                FROM accounts WHERE account_number = ?""", (number,)).fetchone()
        if row is None:
            return None
        account_cls = ACCOUNT_TYPES.get(row[7])
        if account_cls is None or account_cls is BankAccount:
            print("Unknown or legacy account type; cannot load abstract BankAccount.")
            return None
        kwargs = dict(account_title=row[1], balance=row[2], phone=row[3], email=row[4],
                      creation_date=row[5], is_active=bool(row[6]), account_number=row[0])
        if account_cls is BusinessAccount:
            kwargs["overdraft_limit"] = row[8]
        elif account_cls is StudentAccount:
            kwargs["student_age"] = row[9]
            kwargs["daily_withdrawal_limit"] = row[10]
        return account_cls(**kwargs)

    @classmethod
    def find_account(cls):
        search = input("Search account number, name, or phone: ").strip()
        with sqlite3.connect(DB_FILE) as conn:
            rows = conn.execute("""SELECT account_number, account_title, phone, email, account_type
                FROM accounts WHERE account_number = ? OR account_title LIKE ? OR phone = ?""",
                (search, f"%{search}%", search)).fetchall()
        if not rows:
            print("Account not found.")
            return None
        for number, name, phone, email, kind in rows:
            print(f"{number} | {name} | {phone} | {email} | {kind}")
        number = rows[0][0] if len(rows) == 1 else input("Enter exact account number: ").strip()
        return cls.get_account_by_number(number)

    @classmethod
    def list_accounts(cls):
        with sqlite3.connect(DB_FILE) as conn:
            rows = conn.execute("""SELECT account_number, account_title, phone,
                balance, is_active, account_type FROM accounts ORDER BY account_title""").fetchall()
        if not rows:
            print("No accounts yet.")
            return
        for number, name, phone, balance, active, kind in rows:
            print(f"{number} | {name:<20} | {kind:<16} | {phone:<14} | ${balance:.2f} | "
                  f"{'Active' if active else 'Inactive'}")


# V5: Inheritance. Each child IS A BankAccount and inherits its common methods.
class SavingsAccount(BankAccount):
    account_type = "SavingsAccount"
    annual_interest_rate = 0.03

    # OVERRIDE: the same withdraw(amount) call behaves differently for savings.
    # Savings does not charge the $2 fee in this fictional banking policy.
    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or not float(amount).is_integer():
            print("Amount must be a whole-dollar number.")
            return
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        if amount > self.balance:
            print("Insufficient funds in Savings Account.")
            return
        self._change_balance(-amount)
        self.save_to_db()
        self.record_transaction("Savings Withdrawal", 0, amount)
        print(f"Savings withdrew ${amount:.2f}, no fee. Balance: ${self.balance:.2f}")

    def calculate_annual_interest(self):
        """Calculate only; does not credit money to the account."""
        return self.balance * self.annual_interest_rate


class ChequingAccount(BankAccount):
    account_type = "ChequingAccount"
    # IMPORTANT: V7 inherited this behavior from the parent. In V8 the parent
    # withdraw() becomes abstract, so the same fee policy is moved here.
    # This changes WHERE the rule lives, not WHAT it does.
    # CONCRETE IMPLEMENTATION: fulfills the abstract withdraw() contract.
    # Chequing has the $2 fee that V5 originally placed in the parent.
    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or not float(amount).is_integer():
            print("Amount must be a whole-dollar number.")
            return
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        fee = 2
        if amount + fee > self.balance:
            print("Insufficient funds (including $2 fee).")
            return
        self._change_balance(-(amount + fee))
        self.save_to_db()
        # Preserve the V7 parent withdrawal's statement description as well.
        self.record_transaction("Withdrawal", 0, amount + fee)
        print(f"Chequing withdrew ${amount:.2f} + ${fee:.2f} fee. Balance: ${self.balance:.2f}")


class BusinessAccount(BankAccount):
    account_type = "BusinessAccount"

    def __init__(self, account_title, balance, phone, email, overdraft_limit=0,
                 creation_date=None, is_active=False, account_number=None):
        # super() reuses the parent's initialization.
        super().__init__(account_title, balance, phone, email,
                         creation_date=creation_date, is_active=is_active,
                         account_number=account_number)
        if (isinstance(overdraft_limit, bool) or
                not isinstance(overdraft_limit, (int, float)) or
                not float(overdraft_limit).is_integer() or overdraft_limit < 0):
            raise ValueError("Overdraft limit must be a non-negative whole-dollar amount.")
        self.overdraft_limit = int(overdraft_limit)
        # The limit is a separate feature of the business account.

    # OVERRIDE: business customers can use their approved overdraft.
    # For V6 we assume there is no withdrawal fee on this account type.
    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or not float(amount).is_integer():
            print("Amount must be a whole-dollar number.")
            return
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        if amount > self.balance + self.overdraft_limit:
            print("Insufficient funds including approved overdraft.")
            return
        self._change_balance(-amount)
        self.save_to_db()
        self.record_transaction("Business Withdrawal", 0, amount)
        print(f"Business withdrew ${amount:.2f}. Balance: ${self.balance:.2f}")


# V8 ABSTRACTION — NEW CONCRETE BANKING PRODUCT
# BankAccount defines withdraw() as abstract. StudentAccount MUST implement it.
# Business assumptions (fictional): eligible age 16–25, no fee, no overdraft,
# and a maximum of $500 in total withdrawals per calendar day.
class StudentAccount(BankAccount):
    account_type = "StudentAccount"
    DEFAULT_DAILY_LIMIT = 500

    def __init__(self, account_title, balance, phone, email, student_age,
                 daily_withdrawal_limit=DEFAULT_DAILY_LIMIT,
                 creation_date=None, is_active=False, account_number=None):
        # INHERITANCE: reuse common attributes and methods from BankAccount.
        super().__init__(account_title, balance, phone, email,
                         creation_date=creation_date, is_active=is_active,
                         account_number=account_number)
        # Only enforce age when opening a new account. Existing accounts can
        # continue to be loaded even after their owner turns 26.
        if not isinstance(student_age, int) or isinstance(student_age, bool):
            raise ValueError("Student age must be an integer.")
        if account_number is None and not 16 <= student_age <= 25:
            raise ValueError("Student Account applicants must be 16–25.")
        if (not isinstance(daily_withdrawal_limit, int) or
                isinstance(daily_withdrawal_limit, bool) or daily_withdrawal_limit <= 0):
            raise ValueError("Daily withdrawal limit must be a positive whole-dollar amount.")
        self.student_age = student_age
        self.daily_withdrawal_limit = daily_withdrawal_limit

    def withdrawn_today(self):
        # Unlike session-only statements, daily usage is stored in SQLite.
        # This prevents restarting the program from resetting the limit.
        today = datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect(DB_FILE) as conn:
            row = conn.execute("""SELECT COALESCE(SUM(amount), 0)
                FROM student_withdrawals
                WHERE account_number = ? AND withdrawal_date = ?""",
                (self.account_number, today)).fetchone()
        return int(row[0])

    def withdraw(self, amount):
        # ABSTRACTION: this concrete implementation fulfills BankAccount's
        # required withdraw() contract.
        # POLYMORPHISM: the same account.withdraw(100) call follows student rules.
        if (not isinstance(amount, (int, float)) or isinstance(amount, bool)
                or not float(amount).is_integer()):
            print("Amount must be a whole-dollar number.")
            return
        amount = int(amount)
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        if amount > self.balance:
            print("Insufficient funds; Student Accounts do not allow overdrafts.")
            return
        used = self.withdrawn_today()
        if used + amount > self.daily_withdrawal_limit:
            remaining = self.daily_withdrawal_limit - used
            print(f"Daily limit exceeded. Remaining today: ${remaining:.2f}")
            return

        # ENCAPSULATION: use the protected balance helper rather than assigning
        # to the read-only account.balance property.
        self._change_balance(-amount)
        try:
            # Record daily usage in the database so the rule survives restarts.
            # Saving balance and daily usage in the same transaction avoids a
            # partially persisted withdrawal.
            today = datetime.now().strftime("%Y-%m-%d")
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute("UPDATE accounts SET balance = ? WHERE account_number = ?",
                             (self.balance, self.account_number))
                conn.execute("""INSERT INTO student_withdrawals
                    (account_number, withdrawal_date, amount) VALUES (?, ?, ?)""",
                    (self.account_number, today, amount))
        except sqlite3.Error:
            self._change_balance(amount)  # Undo in-memory change if SQLite fails.
            print("Withdrawal failed; no money deducted.")
            return
        self.record_transaction("Student Withdrawal", 0, amount)
        print(f"Student withdrew ${amount:.2f} (no fee). Balance: ${self.balance:.2f}")


ACCOUNT_TYPES = {
    "SavingsAccount": SavingsAccount,
    "ChequingAccount": ChequingAccount,
    "BusinessAccount": BusinessAccount,
    "StudentAccount": StudentAccount,
}


def read_amount(prompt, allow_blank=False):
    raw = input(prompt).strip()
    if allow_blank and raw == "":
        return 0
    try:
        value = float(raw)
        if not value.is_integer() or value < 0:
            raise ValueError
        return int(value)
    except ValueError:
        print("Enter a non-negative whole-dollar amount.")
        return None


def account_menu(account):
    while True:
        print("\n" + "=" * 46)
        print(f"{account.account_title.upper()} — {account.account_type}".center(46))
        print("=" * 46)
        print("1. Deposit\n2. Withdraw\n3. Account Info\n4. Statement\n"
              "5. Activate\n6. Deactivate\n7. Specialized Feature\n0. Back")
        choice = input("Choice: ").strip()
        # POLYMORPHISM IN ACTION: this menu never asks which subclass it has.
        # Python chooses the correct withdraw() implementation at runtime.
        if choice in ("1", "2"):
            amount = read_amount("Amount (whole dollars): ")
            if amount is not None:
                if choice == "1":
                    account.deposit(amount)
                else:
                    account.withdraw(amount)
        elif choice == "3":
            account.account_info()
        elif choice == "4":
            account.show_statement()
        elif choice == "5":
            account.activate_account()
        elif choice == "6":
            account.deactivate_account()
        elif choice == "7":
            if isinstance(account, SavingsAccount):
                print(f"Illustrative annual interest: ${account.calculate_annual_interest():.2f}")
            elif isinstance(account, StudentAccount):
                print(f"Student daily limit: ${account.daily_withdrawal_limit:.2f}; "
                      f"used today: ${account.withdrawn_today():.2f}; "
                      f"remaining: ${account.daily_withdrawal_limit - account.withdrawn_today():.2f}")
            elif isinstance(account, BusinessAccount):
                print(f"Approved overdraft limit: ${account.overdraft_limit:.2f} "
                      "(overdraft enabled in V6)")
            else:
                print("Chequing implements the required $2-fee withdrawal policy.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def main():
    init_db()
    while True:
        print("\n========== SADEED NATIONAL BANK — V8 ==========")
        print("1. Open Savings Account\n2. Open Chequing Account\n"
              "3. Open Business Account\n4. Open Student Account\n5. Find Account\n6. List Accounts\n0. Quit")
        choice = input("Choice: ").strip()
        if choice in ("1", "2", "3", "4"):
            kind = {"1": SavingsAccount, "2": ChequingAccount,
                    "3": BusinessAccount, "4": StudentAccount}[choice]
            account = kind.open_account()
            if account:
                account_menu(account)
        elif choice == "5":
            account = BankAccount.find_account()
            if account:
                account_menu(account)
        elif choice == "6":
            BankAccount.list_accounts()
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
