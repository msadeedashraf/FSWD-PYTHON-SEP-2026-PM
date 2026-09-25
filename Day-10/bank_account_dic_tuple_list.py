balance = 1000.00
overdraft = 100
transactions = []
FILE_NAME = "bank_statrment.txt"
file_path = f"D:\\CBC\\SEProject\\FSD-APR-20226\\Python\\FSWD-PYTHON-SEP-2026-PM\\Day-10\\statements\\{FILE_NAME}"
    
from datetime import datetime 


def deposit(amount):
    global balance


    # To implement checking zero $ deposit
    if amount == 0:
        print("Deposit Amount can not be equal to zero")
        return   
    

    balance += amount 
    # TUPLE
    timestamp = (
        datetime.now().strftime("%Y-%m-%d"), # Date part from the current date
        datetime.now().strftime("%I:%M:%S") # Time Part from the current date
    )

     # Dictionary
    transaction = {
        'type':'Deposit',
        'date':timestamp[0],
        'time': timestamp[1],
        'money_in': amount,
        'money_out':0,
        'balance': balance
    }
    


   # current_time = datetime.now()

    # transaction = [
    # current_time.strftime("%Y-%m-%d"), # Date part    
    # current_time.strftime("%I:%M:%S"), # time part
    # "Deposit",
    # amount, # money in
    # 0, # money out
    # balance
    # ]


    transactions.append(transaction)

    print(f"Dposited : {amount} successfully." ) 
    print(f"New Balance is : {balance}")

def withdraw(amount):
    global balance

    if amount > balance + overdraft :
        print("Insufficient funds")
        return


    fee = 2
    amount  += fee

    balance -= amount  

    # TUPLE
    timestamp = (
        datetime.now().strftime("%Y-%m-%d"), # Date part from the current date
        datetime.now().strftime("%I:%M:%S") # Time Part from the current date
    )
  

    # Dictionary
    transaction = {
        'type':'Deposit',        
        'date':timestamp[0],
        'time': timestamp[1],
        'money_in': 0,
        'money_out':amount,
        'balance': balance
    }
    


    # current_time = datetime.now()

    # transaction = [
    # current_time.strftime("%Y-%m-%d"), # Date part    
    # current_time.strftime("%I:%M:%S"), # time part
    # "Withdraw",
    # 0, # money in
    # amount, # money out
    # balance
    # ]

    transactions.append(transaction)

    print(f"Withdraw : {amount}")
    print(f"New Balance is : {balance}")


def create_statement():

    if (transactions) == 0:
        print("No transaction available")
        return
    
    

    with open(file_path, "w") as file:

            file.write("============================================================\n")
            file.write("                    SADEED NATIONAL BANK\n")
            file.write("============================================================\n")
            file.write("Account Holder : Student Demo Account\n")
            file.write("Account Number : **** **** **** 1234\n")
            file.write(f"Statement Date : {datetime.now()}\n")
            file.write("Currency       : CAD\n")
            file.write("============================================================\n\n")

            file.write(
                f"{'Date':<12}"
                f"{'Time':<12}"
                f"{'Description':<15}"
                f"{'Money In':>12}"
                f"{'Money Out':>12}"
                f"{'Balance':>12}\n"
            )

            file.write("-" * 75 + "\n")

            for transaction in transactions:

                file.write(
                    f"{transaction['date']:<12}"
                    f"{transaction['time']:<12}"
                    f"{transaction['type']:<15}"
                    f"${transaction['money_in']:>11.2f}"
                    f"${transaction['money_out']:>11.2f}"
                    f"${transaction['balance']:>11.2f}\n"
                )

            file.write("-" * 75 + "\n")
            file.write(f"{'Closing Balance':>63}: ${balance:.2f}\n")
            file.write(f"{'Total Available Balance':>63}: ${balance+overdraft:.2f}\n")

            file.write("============================================================\n")

            print("\n Successfully created the statement")
            print(f"Saved at : {file_path}")


def read_statement():
    
    with open(file_path, "r" ) as file:
        print("\n")
        print(file.read())


def show_statement():
    if (transactions) == 0:
        print("No transaction available")
        return
    
    print("\n==============================================================")
    print("                    SADEED NATIONAL BANK")
    print("==============================================================")

    print(
        f"{'Date':<12}"
        f"{'Time':<12}"
        f"{'Description':<15}"
        f"{'Money In':>12}"
        f"{'Money Out':>12}"
        f"{'Balance':>12}"
    )

    print("-" * 75)

    # LOOP THROUGH LIST
    for transaction in transactions:

        print(
                f"{transaction['date']:<12}"
                f"{transaction['time']:<12}"
                f"{transaction['type']:<15}"
                f"${transaction['money_in']:>11.2f}"
                f"${transaction['money_out']:>11.2f}"
                f"${transaction['balance']:>11.2f}\n"
        )

    print("-" * 75)
    print(f"{'Closing Balance':>63}: ${balance:.2f}")
    print(f"{'Total Available Balance':>63}: ${balance+overdraft:.2f}\n")


def menu():
        print("===========Bank Account==============")
        print("1. Dposit")
        print("2. Withdraw")
        print("3. Show Statement")
        print("4. Quit")
        print("5. Create Statement")
        print("6. Read Statement from file")
        print("=====================================")


def main():
    
    while True:
        menu()
    
        choice = input("Slect the option")

        if choice == "4":
            print("Close bank account")
            print("Thankyou for using the world's best bank account")        
            break
            
        if choice not in ["1", "2", "3","5", "6"]:
            print("Invalid choice")
            print("select correct option to continue from the menu")
            continue

        elif choice == '1' :
            d = float(input("Enter the amount to deposit: "))
            deposit(d)

        elif choice == '2' :
            w = float(input("Enter the amount to withdraw: "))    
            withdraw(w)

        elif choice == '3' :
           show_statement()
        
        elif choice == '5' :
           create_statement()

        elif choice == '6' :
           read_statement()
    
main()
