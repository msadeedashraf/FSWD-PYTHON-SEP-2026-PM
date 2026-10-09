# Inheritance
#The bank introduces different account products. How can we reuse existing banking functionality without copying code?
#add interest calculation for the saving account and apply fee method in the the chequing Class
# overdraft method in Business Account
 
from datetime import datetime
import random
import sqlite3
 
DB_FILE = "bank_v5.db"
 
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            account_title TEXT NOT NULL,
            balance REAL NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            is_active INTEGER NOT NULL,
            account_type TEXT NOT NULL DEFAULT 'BankAccount',
            overdraft_limit REAL NOT NULL DEFAULT 0
        )""")
 
 
class BankAccount:
    """Parent class: common account data and common operations."""
 
    bank_name = "SADEED NATIONAL BANK"
    account_type = "BankAccount"
 
    def __init__(self, account_title, balance, phone, email,
                    creation_date=None, is_active=False, account_number=None):
        self.account_number = account_number or self.generate_iban()
        self.account_title = account_title
        self.balance = float(balance)
        self.phone = phone
        self.email = email
        self.transactions = []  # Session-only history, as in Version 4.
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = bool(is_active)
 
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
                    creation_date, is_active, account_type, overdraft_limit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(account_number) DO UPDATE SET
                    account_title=excluded.account_title,
                    balance=excluded.balance, phone=excluded.phone,
                    email=excluded.email, creation_date=excluded.creation_date,
                    is_active=excluded.is_active, account_type=excluded.account_type,
                    overdraft_limit=excluded.overdraft_limit""",
                (self.account_number, self.account_title, self.balance,
                    self.phone, self.email, self.creation_date, int(self.is_active),
                    self.account_type, getattr(self, "overdraft_limit", 0)))
 
    def activate_account(self):
        self.is_active = True
        self.save_to_db()
        print("Account activated.")
 
    def deactivate_account(self):
        self.is_active = False
        self.save_to_db()
        print("Account deactivated.")
 
    def record_transaction(self, kind, money_in, money_out):
        date, time = self.get_timestamp()
        self.transactions.append({"type": kind, "date": date, "time": time,
                                    "money_in": money_in, "money_out": money_out,
                                    "balance": self.balance})
 
    def deposit(self, amount):
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        self.balance += amount
        self.save_to_db()
        self.record_transaction("Deposit", amount, 0)
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
 
    def withdraw(self, amount): # Signature
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        if amount > self.balance:
            print("Insufficient funds.")
            return
        self.balance -= amount
        self.save_to_db()
        self.record_transaction("Withdrawal", 0, amount)
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
 
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
        if cls is BusinessAccount:
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
                phone, email, creation_date, is_active, account_type, overdraft_limit
                FROM accounts WHERE account_number = ?""", (number,)).fetchone()
        if row is None:
            return None
        account_cls = ACCOUNT_TYPES.get(row[7], BankAccount)
        kwargs = dict(account_title=row[1], balance=row[2], phone=row[3], email=row[4],
                        creation_date=row[5], is_active=bool(row[6]), account_number=row[0])
        if account_cls is BusinessAccount:
            kwargs["overdraft_limit"] = row[8]
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
 
 
class SavingsAccount(BankAccount):
    account_type = "SavingsAccount"
    annual_interest_rate = 0.03
 
    def calculate_annual_interest(self):
        """Calculate interest without changing the balance."""
        return self.balance * self.annual_interest_rate
 
    def apply_interest(self):
        """Credit annual interest to the savings account."""
        if not self.is_active:
            print("Activate the account first.")
            return
        interest = self.calculate_annual_interest()
        if interest <= 0:
            print("No interest to apply.")
            return
        self.balance += interest
        self.save_to_db()
        self.record_transaction("Interest", interest, 0)
        print(f"Interest added: ${interest:.2f}")
        print(f"New balance: ${self.balance:.2f}")
 
 
class ChequingAccount(BankAccount):
    account_type = "ChequingAccount"
    withdrawal_fee = 2.00
 
    def apply_fee(self, amount):
        """Calculate the withdrawal amount including the fee."""
        return amount + self.withdrawal_fee
   
# method Overrding (Polymorphism)
 
    def withdraw(self, amount):
        """Withdraw money and charge the chequing fee."""
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        total = self.apply_fee(amount)
        if total > self.balance:
            print("Insufficient funds (including fee).")
            return
        self.balance -= total
        self.save_to_db()
        self.record_transaction("Withdrawal", 0, total)
        print(f"Withdrawal: ${amount:.2f}")
        print(f"Fee: ${self.withdrawal_fee:.2f}")
        print(f"New balance: ${self.balance:.2f}")
 
 
class BusinessAccount(BankAccount):
    account_type = "BusinessAccount"
 
    def __init__(self, account_title, balance, phone, email, overdraft_limit=0,
                 creation_date=None, is_active=False, account_number=None):
        super().__init__(account_title, balance, phone, email,
                         creation_date=creation_date, is_active=is_active,
                         account_number=account_number)
        self.overdraft_limit = float(overdraft_limit)
 
    def overdraft(self, amount):
        """Withdraw using the approved overdraft limit."""
        if not self.is_active:
            print("Activate the account first.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        available_funds = self.balance + self.overdraft_limit
        if amount > available_funds:
            print("Withdrawal exceeds the overdraft limit.")
            print(f"Available funds including overdraft: ${available_funds:.2f}")
            return
        self.balance -= amount
        self.save_to_db()
        self.record_transaction("Withdrawal", 0, amount)
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
 
    def withdraw(self, amount):
        """Use the business account's overdraft rules for withdrawals."""
        self.overdraft(amount)
 
ACCOUNT_TYPES = {
    "BankAccount": BankAccount,
    "SavingsAccount": SavingsAccount,
    "ChequingAccount": ChequingAccount,
    "BusinessAccount": BusinessAccount,
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
                print("1. Calculate annual interest")
                print("2. Apply annual interest")
                feature = input("Choose an option: ").strip()
                if feature == "1":
                    interest = account.calculate_annual_interest()
                    print(f"Annual interest: ${interest:.2f}")
                elif feature == "2":
                    account.apply_interest()
                else:
                    print("Invalid choice.")
            elif isinstance(account, ChequingAccount):
                amount = read_amount("Withdrawal amount to calculate fee for: ")
                if amount is not None and amount > 0:
                    total = account.apply_fee(amount)
                    print(f"Withdrawal amount: ${amount:.2f}")
                    print(f"Fee: ${account.withdrawal_fee:.2f}")
                    print(f"Total deduction: ${total:.2f}")
            elif isinstance(account, BusinessAccount):
                print(f"Current balance: ${account.balance:.2f}")
                print(f"Overdraft limit: ${account.overdraft_limit:.2f}")
                print(
                    f"Available funds including overdraft: "
                    f"${account.balance + account.overdraft_limit:.2f}"
                )
            else:
                print("No specialized features available for this account.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
 
 
 
def main():
    init_db()
    while True:
        print("\n========== SADEED NATIONAL BANK — V5 ==========")
        print("1. Open Savings Account\n2. Open Chequing Account\n"
              "3. Open Business Account\n4. Find Account\n5. List Accounts\n0. Quit")
        choice = input("Choice: ").strip()
        if choice in ("1", "2", "3"):
            kind = {"1": SavingsAccount, "2": ChequingAccount,
                    "3": BusinessAccount}[choice]
            account = kind.open_account()
            if account:
                account_menu(account)
        elif choice == "4":
            account = BankAccount.find_account()
            if account:
                account_menu(account)
        elif choice == "5":
            BankAccount.list_accounts()
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")
 
 
if __name__ == "__main__":
    main()
 
 

 #v5_2
 # DRY
 # Implement Overdraft for other types of banks accounts as well.
 # Student Account without fee