balance = 1000

def deposit(amount):
    global balance
    balance += amount  
    print(f"New Balance is : {balance}")

def withdraw(amount):
    global balance
    balance -= amount  
    print(f"New Balance is : {balance}")

def main():
    d = float(input("Enter the amount to deposit: "))
    deposit(d)

    w = float(input("Enter the amount to withdraw: "))    
    withdraw(w)

main()


