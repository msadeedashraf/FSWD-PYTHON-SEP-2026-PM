# ============================================================
# SADEED NATIONAL BANK
# Bank Account OOP - Version 3
# ============================================================
# Features:
# - Create bank accounts dynamically
# - Generate an IBAN-style account number
# - Activate / deactivate accounts
# - Deposit and withdraw money
# - Display account information
# - Display transaction statements
# - Search accounts by account number or account holder name
# - List all bank accounts
# ============================================================

from datetime import datetime
import random


class BankAccount:

    # Class variable shared by all BankAccount objects
    bank_name = "SADEED NATIONAL BANK"

    # Constructor - runs automatically when a BankAccount object is created
    def __init__(self, account_title, balance):
        self.account_number = self.generate_iban()
        self.account_title = account_title
        self.balance = int(balance)
        self.transactions = []
        self.creation_date = datetime.now()
        self.is_active = False

    # Return the current date and time as a tuple
    def get_timestamp(self):
        current_time = datetime.now()

        timestamp = (
            current_time.strftime("%Y-%m-%d"),
            current_time.strftime("%I:%M:%S %p")
        )

        return timestamp

    # Generate an IBAN-style account number for the new account
    def generate_iban(self):
        country_code = "CA"
        check_digits = str(random.randint(10, 99))
        bank_identifier = "SNBC"
        account_number = str(random.randint(10000000, 99999999))

        return f"{country_code}{check_digits}{bank_identifier}{account_number}"

    # Activate the selected bank account
    def activate_account(self):
        self.is_active = True
        print(f"Account {self.account_number} is activated")

    # Deactivate the selected bank account
    def deactivate_account(self):
        self.is_active = False
        print(f"Account {self.account_number} is deactivated")

    # Deposit money into the selected account
    def deposit(self, amount):

        # Deposits are only allowed on active accounts
        if self.is_active == False:
            return print(
                f"{self.account_title} your account has to be active "
                f"before depositing.\nContact the branch"
            )

        # Deposit amount must be greater than zero
        if amount <= 0:
            print("Amount must be greater than zero")
            return

        # Update account balance
        self.balance += int(amount)

        # Get transaction date and time
        timestamp = self.get_timestamp()

        # Store transaction details in a dictionary
        transaction = {
            'type': 'Deposit',
            'date': timestamp[0],
            'time': timestamp[1],
            'money_in': amount,
            'money_out': 0,
            'balance': self.balance
        }

        # Add transaction to the account transaction list
        self.transactions.append(transaction)

        print(f"Dposited : {amount} successfully.")
        print(f"New Balance for {self.account_title} : {self.balance}")

    # Withdraw money from the selected account
    def withdraw(self, amount):

        # Check whether enough funds are available
        if amount > self.balance:
            print("Insufficient funds")
            return

        # Add the bank withdrawal fee
        fee = 2
        amount += fee

        # Update account balance
        self.balance -= amount

        # Get transaction date and time
        timestamp = self.get_timestamp()

        # Store transaction details in a dictionary
        transaction = {
            'type': 'Deposit',
            'date': timestamp[0],
            'time': timestamp[1],
            'money_in': 0,
            'money_out': amount,
            'balance': self.balance
        }

        # Add transaction to the account transaction list
        self.transactions.append(transaction)

        print(f"Withdraw : {amount}")
        print(f"New Balance is : {self.balance}")

    # Display information about the selected account
    def account_info(self):
        print("\n========== ACCOUNT INFO ==========")
        print(f"Account Number      : {self.account_number}")
        print(f"Account Holder Name : {self.account_title}")
        print(f"Balance             : ${self.balance:.2f}")
        print(
            f"Creation Date       : "
            f"{self.creation_date.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f"Account Active      : {self.is_active}")
        print("==================================")

    # Display all transactions for the selected account
    def show_statement(self):

        # Stop if the account does not have any transactions
        if len(self.transactions) == 0:
            print("\nNo transactions to display.")
            return

        print("\n==============================================================")
        print(f"                    {BankAccount.bank_name}")
        print("==============================================================")

        print(f"{'Account Title':>63}: {self.account_title}")
        print(f"{'Account Number':>63}: {self.account_number}")

        # Statement column headings
        print(
            f"{'Date':<12}"
            f"{'Time':<12}"
            f"{'Description':<15}"
            f"{'Money In':>12}"
            f"{'Money Out':>12}"
            f"{'Balance':>12}"
        )

        print("-" * 75)

        # Display each transaction stored in the transaction list
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

    # Class method used to create and return a new BankAccount object
    @classmethod
    def open_account(cls):
        print(f"Welcome to {cls.bank_name} \nLet's open an account")

        # Collect account opening information from the user
        name = input("\nEnter your Account Title:")
        user_deposit_amount = float(
            input("Enter the initial depost amount: ")
        )

        opening_balance = (
            user_deposit_amount if user_deposit_amount else 0
        )

        # Create the new BankAccount object
        account = cls(name, opening_balance)

        # Display the newly created account details
        print(f"Account Holder : {account.account_title}")
        print(f"Account Number : {account.account_number}")
        print(f"Balance        : ${account.balance:.2f}")

        print("\nAccount is currently deactivated.")
        print("Please activate it before making transactions.")

        # Return the object so main() can store it
        return account

    # Search for an account by account number or account holder name
    @classmethod
    def find_account(cls, accounts):

        search = input(
            "\nEnter Account Number or Account Holder Name: "
        ).strip()

        # Search by exact account number
        # Account numbers are dictionary keys
        if search in accounts:
            return accounts[search]

        # Search by account holder name
        for account in accounts.values():

            # lower() makes the name search case-insensitive
            if account.account_title.lower() == search.lower():
                return account

        print("\nAccount not found.")
        return None

    # Display all bank accounts currently stored in the program
    @classmethod
    def list_accounts(cls, accounts):

        # Check whether any accounts have been created
        if len(accounts) == 0:
            print("\nNo bank accounts have been created.")
            return

        print("\n============================================================")
        print(f"                  {cls.bank_name}")
        print("                     ACCOUNT LIST")
        print("============================================================")

        # Account list column headings
        print(
            f"{'Account Number':<22}"
            f"{'Account Title':<20}"
            f"{'Balance':>12}"
            f"{'Status':>12}"
        )

        print("-" * 66)

        # Loop through all BankAccount objects in the dictionary
        for account in accounts.values():

            # Convert the Boolean status into readable text
            status = "Active" if account.is_active else "Inactive"

            print(
                f"{account.account_number:<22}"
                f"{account.account_title:<20}"
                f"${account.balance:>11.2f}"
                f"{status:>12}"
            )

        print("-" * 66)


# ============================================================
# ACCOUNT OPERATIONS MENU
# Receives the selected BankAccount object from the main menu
# ============================================================

def account_menu(selected_account):

    while True:
        print("\n============================")
        print(f"   {selected_account.account_title}'s Account")
        print("============================")

        print("1. Deposit")
        print("2. Withdraw")
        print("3. Account Info")
        print("4. View Statement")
        print("5. Activate Account")
        print("6. Deactivate Account")
        print("0. Back")

        account_choice = input("\nSelect an option: ")

        if account_choice == "1":
            amount = int(input("Enter deposit amount: "))
            selected_account.deposit(amount)

        elif account_choice == "2":
            amount = int(input("Enter withdrawal amount: "))
            selected_account.withdraw(amount)

        elif account_choice == "3":
            selected_account.account_info()
            # print(f"Current Balance: ${selected_account.balance}")

        elif account_choice == "4":
            print(selected_account.show_statement())

        elif account_choice == "5":
            print(selected_account.activate_account())

        elif account_choice == "6":
            print(selected_account.deactivate_account())

        elif account_choice == "0":
            # Return control to the main bank menu
            break

        else:
            print("Invalid option.")


# ============================================================
# MAIN BANK MENU
# Allows users to create, find, or list bank accounts
# ============================================================

def main():

    # In-memory account storage
    # Key   = account number
    # Value = BankAccount object
    accounts = {}

    while True:
        print("\n============================")
        print("\n   Bank Account Main Menu")
        print("\n============================")

        print("1. Open Bank Account")
        print("2. Find Bank Account")
        print("3. List All Accounts")
        print("0. Quit")

        choice = input("\n Input your choice: ")

        # Create a new bank account
        if choice == "1":
            account = BankAccount.open_account()

            # Store the new object using its account number as the key
            accounts[account.account_number] = account

            # Pass control to the account operations menu
            account_menu(account)

        # Find an existing account
        elif choice == "2":
            account = BankAccount.find_account(accounts)

            # Only open the account menu when an account was found
            if account is not None:
                account_menu(account)

        # Display all existing accounts
        elif choice == "3":
            BankAccount.list_accounts(accounts)

        # Exit the application
        elif choice == "0":
            print(
                f"\nThank you for choosing "
                f"{BankAccount.bank_name}."
            )
            break

        else:
            print("\nInvalid option.")


# Start the bank application
main()


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
