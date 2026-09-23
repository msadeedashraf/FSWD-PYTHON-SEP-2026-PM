balance = 1000.00
transactions = []

from datetime import datetime


def deposit(amount):
    global balance 
    balance += amount

    current_time = datetime.now()
    transaction= [
        current_time.strftime("%Y-%m-%d") , #Date part
        current_time.strftime("%I:%M:%S") , #Time part
        "Deposit",
        amount, # money IN 
        0, # money OUT
        balance
    ]
    transactions.append(transaction)


    print(f"Dposited : {amount} successfully." ) 
    print(f"New Balance is : {balance}")



def withdraw(amount):
    global balance 
    balance -= amount

    current_time = datetime.now()
    transaction= [
        current_time.strftime("%Y-%m-%d") , #Date part
        current_time.strftime("%I:%M:%S") , #Time part
        "Withdraw",
        0, # money IN 
        amount, # money OUT
        balance
    ]
    transactions.append(transaction)


    print(f"Withdraw : {amount} successfully." ) 
    print(f"New Balance is : {balance}")



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
                f"{transaction[0]:<12}"
                f"{transaction[1]:<12}"
                f"{transaction[2]:<15}"
                f"${transaction[3]:>11.2f}"
                f"${transaction[4]:>11.2f}"
                f"${transaction[5]:>11.2f}"
            )

        print("-" * 75)
        print(f"{'Closing Balance':>63}: ${balance:.2f}")



def menu():
        print("===========Bank Account==============")
        print("1. Dposit")
        print("2. Withdraw")
        print("3. Show Statement")
        print("4. Quit")
        print("=====================================")


def main():
    
    while True:
        menu()
    
        choice = input("Slect the option")

        if choice == "4":
            print("Close bank account")
            print("Thankyou for using the world's best bank account")        
            break
            
        if choice not in ["1", "2", "3"]:
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

            
main()
