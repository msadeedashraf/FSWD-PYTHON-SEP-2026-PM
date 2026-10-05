 
# ============================================================
# STUDENT CHALLENGE
# ============================================================
 
# Add phone/cell no and email in the account creation process
 
# When you create the account, check if the account already exists
# using the phone/cell number
 
# Enhance the search capability and list all similar accounts
# with basic info:
# account_no, title, phone, email
 
# When an account is found, display more data such as:
# title, account no, balance, account creation date, phone and email
# and center align the operations menu
 
# Update all the other relevant methods such as:
# view / create / read statements
 
 
# ============================================================
# BONUS
# ============================================================
 
# Apply DRY to that version
# (No APIE yet - just simple objects, methods and classes)
 
# Read more about class methods
 
# Apply and save this in a Database (SQLite)
 
# ============================================================
# SADEED NATIONAL BANK
# Bank Account OOP - Version 4 (SQLite Database & Challenges)
# ============================================================
 
from datetime import datetime
import random
import sqlite3
 
# ============================================================
# DATABASE SETUP (SQLite)
# ============================================================
# This creates a persistent file on your hard drive called 'bank.db'
# so your data is never lost when the program closes.
def init_db():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            account_title TEXT,
            balance INTEGER,
            phone TEXT,
            email TEXT,
            creation_date TEXT,
            is_active INTEGER
        )
    """)
    conn.commit()
    conn.close()
 
 
class BankAccount:
 
    bank_name = "SADEED NATIONAL BANK"
 
    def __init__(self, account_title, balance, phone, email, creation_date=None, is_active=0):
        self.account_number = self.generate_iban()
        self.account_title = account_title
        self.balance = int(balance)
        self.phone = phone
        self.email = email
        self.transactions = []
        # Keep track of creation date as string for easy storage
        self.creation_date = creation_date if creation_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = is_active  # 0 for False, 1 for True in SQLite
 
    def get_timestamp(self):
        current_time = datetime.now()
        return (
            current_time.strftime("%Y-%m-%d"),
            current_time.strftime("%I:%M:%S %p")
        )
 
    def generate_iban(self):
        country_code = "CA"
        check_digits = str(random.randint(10, 99))
        bank_identifier = "SNBC"
        account_number = str(random.randint(10000000, 99999999))
        return f"{country_code}{check_digits}{bank_identifier}{account_number}"
 
    # Save or update this account object inside the SQLite database
    def save_to_db(self):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO accounts
            (account_number, account_title, balance, phone, email, creation_date, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.account_number,
            self.account_title,
            self.balance,
            self.phone,
            self.email,
            self.creation_date,
            1 if self.is_active else 0
        ))
        conn.commit()
        conn.close()
 
    def activate_account(self):
        self.is_active = True
        self.save_to_db()
        print(f"Account {self.account_number} is activated.")
 
    def deactivate_account(self):
        self.is_active = False
        self.save_to_db()
        print(f"Account {self.account_number} is deactivated.")
 
    def deposit(self, amount):
        if not self.is_active:
            print(f"{self.account_title}, your account must be active before depositing.\nContact the branch.")
            return
 
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
 
        self.balance += int(amount)
        self.save_to_db()  # Update balance in database
 
        timestamp = self.get_timestamp()
        transaction = {
            'type': 'Deposit',
            'date': timestamp[0],
            'time': timestamp[1],
            'money_in': amount,
            'money_out': 0,
            'balance': self.balance
        }
        self.transactions.append(transaction)
 
        print(f"Deposited: ${amount:.2f} successfully.")
        print(f"New Balance for {self.account_title}: ${self.balance:.2f}")
 
    def withdraw(self, amount):
        if not self.is_active:
            print("Account must be active to withdraw.")
            return
 
        fee = 2
        total_deduction = amount + fee
 
        if total_deduction > self.balance:
            print("Insufficient funds (including $2 withdrawal fee).")
            return
 
        self.balance -= total_deduction
        self.save_to_db()  # Update balance in database
 
        timestamp = self.get_timestamp()
        transaction = {
            'type': 'Withdrawal',
            'date': timestamp[0],
            'time': timestamp[1],
            'money_in': 0,
            'money_out': total_deduction,
            'balance': self.balance
        }
        self.transactions.append(transaction)
 
        print(f"Withdrawn: ${amount:.2f} (plus $2 fee). Total deducted: ${total_deduction:.2f}")
        print(f"New Balance is: ${self.balance:.2f}")
 
    # Enhanced Account Info displaying extra required contact data
    def account_info(self):
        print("\n========== ACCOUNT INFO ==========")
        print(f"Account Number      : {self.account_number}")
        print(f"Account Holder Name : {self.account_title}")
        print(f"Phone Number        : {self.phone}")
        print(f"Email Address       : {self.email}")
        print(f"Balance             : ${self.balance:.2f}")
        print(f"Creation Date       : {self.creation_date}")
        print(f"Account Active      : {'Yes' if self.is_active else 'No'}")
        print("==================================")
 
    def show_statement(self):
        if len(self.transactions) == 0:
            print("\nNo transactions to display for this session.")
            return
 
        print("\n==============================================================")
        print(f"                    {BankAccount.bank_name}")
        print("==============================================================")
        print(f"{'Account Title':>63}: {self.account_title}")
        print(f"{'Account Number':>63}: {self.account_number}")
        print(f"{'Phone Number':>63}: {self.phone}")
 
        print(
            f"{'Date':<12}"
            f"{'Time':<12}"
            f"{'Description':<15}"
            f"{'Money In':>12}"
            f"{'Money Out':>12}"
            f"{'Balance':>12}"
        )
        print("-" * 75)
 
        for transaction in self.transactions:
            print(
                f"{transaction['date']:<12}"
                f"{transaction['time']:<12}"
                f"{transaction['type']:<15}"
                f"${transaction['money_in']:>11.2f}"
                f"${transaction['money_out']:>11.2f}"
                f"${transaction['balance']:>11.2f}"
            )
 
        print("-" * 75)
        print(f"{'Closing Balance':>63}: ${self.balance:.2f}")
 
    @classmethod
    def open_account(cls):
        print(f"\nWelcome to {cls.bank_name} \nLet's open an account")
 
        # Collect user info including cell number and email
        name = input("Enter your Account Title: ").strip()
        phone = input("Enter your Cell/Phone Number: ").strip()
        email = input("Enter your Email Address: ").strip()
 
        # Check database to see if phone number already exists (Duplicate Check)
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE phone = ?", (phone,))
        existing_account = cursor.fetchone()
        conn.close()
 
        if existing_account:
            print(f"\n[!] Error: An account with phone number {phone} already exists!")
            print(f"Existing Account Holder: {existing_account[1]} (Account No: {existing_account[0]})")
            return None
 
        user_deposit_amount = input("Enter the initial deposit amount (press Enter for 0): ").strip()
        opening_balance = float(user_deposit_amount) if user_deposit_amount else 0
 
        # Create the new account object
        account = cls(name, opening_balance, phone, email)
       
        # Save straight to the database file
        account.save_to_db()
 
        print("\nAccount created successfully!")
        print(f"Account Holder : {account.account_title}")
        print(f"Account Number : {account.account_number}")
        print(f"Phone Number   : {account.phone}")
        print(f"Email          : {account.email}")
        print(f"Balance        : ${account.balance:.2f}")
        print("\nAccount is currently deactivated. Please activate it before making transactions.")
 
        return account
 
    @classmethod
    def find_account(cls):
        search = input("\nEnter Account Number, Name, or Phone Number to search: ").strip()
 
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
 
        # Search by account number, exact name match, or phone number
        cursor.execute("""
            SELECT account_number, account_title, balance, phone, email, creation_date, is_active
            FROM accounts
            WHERE account_number = ? OR account_title LIKE ? OR phone = ?
        """, (search, f"%{search}%", search))
 
        results = cursor.fetchall()
        conn.close()
 
        if not results:
            print("\nAccount not found.")
            return None
 
        # If multiple matches found (Enhanced Search capability)
        if len(results) > 1:
            print(f"\nFound {len(results)} matching accounts:")
            print(f"{'Account Number':<22} | {'Title':<18} | {'Phone':<15} | {'Email':<20}")
            print("-" * 80)
            for row in results:
                print(f"{row[0]:<22} | {row[1]:<18} | {row[3]:<15} | {row[4]:<20}")
           
            # Let user specify the exact account number from the matched list
            chosen_acc_no = input("\nEnter the exact Account Number you want to open: ").strip()
            return cls.get_account_by_number(chosen_acc_no)
 
        # If only one match, turn it right back into a BankAccount object
        row = results[0]
        return cls.get_account_by_number(row[0])
 
    @classmethod
    def get_account_by_number(cls, acc_no):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (acc_no,))
        row = cursor.fetchone()
        conn.close()
 
        if row:
            # Rebuild the Python object from the database row data
            acc = cls(
                account_title=row[1],
                balance=row[2],
                phone=row[3],
                email=row[4],
                creation_date=row[5],
                is_active=bool(row[6])
            )
            acc.account_number = row[0]
            return acc
        return None
 
    @classmethod
    def list_accounts(cls):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("SELECT account_number, account_title, balance, phone, email, is_active FROM accounts")
        rows = cursor.fetchall()
        conn.close()
 
        if len(rows) == 0:
            print("\nNo bank accounts have been created yet.")
            return
 
        print("\n==================================================================================")
        print(f"                  {cls.bank_name} - ACCOUNT LIST")
        print("==================================================================================")
        print(
            f"{'Account Number':<22}"
            f"{'Account Title':<18}"
            f"{'Phone No':<15}"
            f"{'Balance':>10}"
            f"{'Status':>10}"
        )
        print("-" * 80)
 
        for row in rows:
            status = "Active" if row[5] == 1 else "Inactive"
            print(
                f"{row[0]:<22}"
                f"{row[1]:<18}"
                f"{row[3]:<15}"
                f"${row[2]:>9.2f}"
                f"{status:>10}"
            )
        print("-" * 80)
 
 
# ============================================================
# ACCOUNT OPERATIONS MENU (Center Aligned as requested)
# ============================================================
 
def account_menu(selected_account):
    while True:
        # Center-aligned styling for the operations menu (Fixed string quotes)
        header_text = f"{selected_account.account_title.upper()}'S ACCOUNT"
        print("\n" + "=" * 40)
        print(f"{header_text:^40}")
        print("=" * 40)
        print(f"{'1. Deposit':^40}")
        print(f"{'2. Withdraw':^40}")
        print(f"{'3. Account Info':^40}")
        print(f"{'4. View Statement':^40}")
        print(f"{'5. Activate Account':^40}")
        print(f"{'6. Deactivate Account':^40}")
        print(f"{'0. Back to Main Menu':^40}")
        print("=" * 40)
 
        account_choice = input("\nSelect an option: ").strip()
 
        if account_choice == "1":
            amount = float(input("Enter deposit amount: "))
            selected_account.deposit(amount)
 
        elif account_choice == "2":
            amount = float(input("Enter withdrawal amount: "))
            selected_account.withdraw(amount)
 
        elif account_choice == "3":
            selected_account.account_info()
 
        elif account_choice == "4":
            selected_account.show_statement()
 
        elif account_choice == "5":
            selected_account.activate_account()
 
        elif account_choice == "6":
            selected_account.deactivate_account()
 
        elif account_choice == "0":
            break
 
        else:
            print("Invalid option. Please try again.")
 
 
# ============================================================
# MAIN BANK MENU
# ============================================================
 
def main():
    # Initialize the database file upon starting up
    init_db()
 
    while True:
        print("\n============================")
        print("   Bank Account Main Menu")
        print("============================")
        print("1. Open Bank Account")
        print("2. Find Bank Account")
        print("3. List All Accounts")
        print("0. Quit")
 
        choice = input("\nInput your choice: ").strip()
 
        if choice == "1":
            account = BankAccount.open_account()
            if account is not None:
                account_menu(account)
 
        elif choice == "2":
            account = BankAccount.find_account()
            if account is not None:
                account_menu(account)
 
        elif choice == "3":
            BankAccount.list_accounts()
 
        elif choice == "0":
            print(f"\nThank you for choosing {BankAccount.bank_name}. Goodbye!")
            break
 
        else:
            print("\nInvalid option.")
 
 
# Start the application
if __name__ == "__main__":
    main()
 