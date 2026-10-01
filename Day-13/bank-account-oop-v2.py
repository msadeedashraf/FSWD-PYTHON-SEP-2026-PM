from datetime import datetime
import random

class BankAccount:
    def __init__(self, account_title, balance):
        self.account_number = self.generate_iban()
        self.account_title = account_title        
        self.balance = int(balance)
        self.transactions = []
        self.creation_date = datetime.now()
        self.is_active =False

    def get_timestamp(self):
        current_time = datetime.now()

        timestamp = (
                current_time.strftime("%Y-%m-%d"),
                current_time.strftime("%I:%M:%S %p")
            )
        
        return timestamp

    def generate_iban(self):
        country_code = "CA"
        check_digits = str(random.randint(10, 99))
        bank_identifier = "SNBC"
        account_number = str(random.randint(10000000, 99999999))
        return f"{country_code}{check_digits}{bank_identifier}{account_number}"

    def activate_account(self):
        self.is_active = True
        print(f"Account {self.account_number} is activated")

    def deactivate_account(self):
        self.is_active = False
        print(f"Account {self.account_number} is deactivated")

    def deposit(self, amount):
        if self.is_active == False:
            return print(f"{self.account_title} your account has to be active before depositing.\nContact the branch")

        if amount <= 0:
            print("Amount must be greater than zero")
            return
        
        self.balance += int(amount)
        
        timestamp = self.get_timestamp()

         # Dictionary
        transaction = {
        'type':'Deposit',
        'date':timestamp[0],
        'time': timestamp[1],
        'money_in': amount,
        'money_out':0,
        'balance': self.balance
        }
        
        self.transactions.append(transaction)

        print(f"Dposited : {amount} successfully." ) 
        print(f"New Balance for {self.account_title} : {self.balance}")

    
    def withdraw(self, amount):
        
        if amount > self.balance:
            print("Insufficient funds")
            return


        fee = 2
        amount  += fee

        self.balance -= amount  

        timestamp = self.get_timestamp()

            
        # Dictionary
        transaction = {
            'type':'Deposit',
            'date':timestamp[0],
            'time': timestamp[1],
            'money_in': 0,
            'money_out':amount,
            'balance': self.balance
        }
        


        self.transactions.append(transaction)

        print(f"Withdraw : {amount}")
        print(f"New Balance is : {self.balance}")



    def account_info(self):
        print("\n========== ACCOUNT INFO ==========")
        print(f"Account Number      : {self.account_number}")
        print(f"Account Holder Name : {self.account_title}")
        print(f"Balance             : ${self.balance:.2f}")
        print(f"Creation Date       : {self.creation_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Account Active      : {self.is_active}")
        print("==================================")
    

    def show_statement(self):

        if len(self.transactions) == 0:
            print("\nNo transactions to display.")
            return

        print("\n==============================================================")
        print("                    SADEED NATIONAL BANK")
        print("==============================================================")

        print(f"{'Account Title':>63}: {self.account_title}")
        print(f"{'Account Number':>63}: {self.account_number}")
        
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


bankaccount1 = BankAccount("Frank", "1000")
#bankaccount1.deposit(100);
bankaccount2 = BankAccount("Sara", "1200")
bankaccount3 = BankAccount("Hazla", "2200")
bankaccount4 = BankAccount("Umar", "5000")

bankaccounts = [bankaccount1, bankaccount2, bankaccount3, bankaccount4]



while True: 
    print("\n============================")
    print("\n   Bank Account Main Menu")
    print("\n============================")

    for  index , account in enumerate(bankaccounts, start=1):
        print(f"{index}. {account.account_title}")

    print("0. Quit")

    choice = input("\n Select an account: ")

    if choice == "0":
        print("Thank you for choosing the Bank Account")
        break

# Convert choice to integer
    choice = int(choice)

    # Check if account exists
    if choice < 1 or choice > len(bankaccounts):
        print("Invalid account selection.")
        continue

    # Get selected account
    selected_account = bankaccounts[choice - 1]

     # ACCOUNT MENU
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
            #print(f"Current Balance: ${selected_account.balance}")

        elif account_choice == "4":
            print(selected_account.show_statement())

        elif account_choice == "5":
            print(selected_account.activate_account())

        elif account_choice == "6":
            print(selected_account.deactivate_account())


        elif account_choice == "0":
            break

        else:
            print("Invalid option.")






