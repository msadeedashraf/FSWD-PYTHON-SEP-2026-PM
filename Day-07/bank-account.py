balance = 1000

def deposit(amount):
    global balance
    balance += amount 
    print(f"Dposited : {amount}") 
    print(f"New Balance is : {balance}")

def withdraw(amount):
    global balance
    balance -= amount  
    print(f"Withdraw : {amount}")
    print(f"New Balance is : {balance}")

def showbalance():
    print(f"Your remaning balance is : {balance}")
    
def menu():
        print("===========Bank Account==============")
        print("1. Dposit")
        print("2. Withdraw")
        print("3. Show balance")
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
           showbalance()

            
main()

"""
create a menu
1.deposit
2. withdraw
3. Balance check
4. quit

ask user the choice

based on that deposit or withdraw 
"""
