from datetime import datetime
import os

# =========================================================
# GLOBAL VARIABLES
# =========================================================

balance = 1000.00
overdraft = 150.00
withdraw_fee = 2.00

transactions = []          # LIST: stores all transaction dictionaries
transaction_types = set()  # SET: stores unique transaction types only


FILE_NAME = "bank_statement.txt"

FOLDER_PATH =  r"D:\CBC\DSAI-Jan-2026-AM\05-Python\DSAI-PYTHON-MAY-2026-AM\Day-11\statements"

# =========================================================
# FUNCTION: CREATE TIMESTAMP
# =========================================================
def get_timestamp():
    current_time = datetime.now()

    # TUPLE: fixed date/time pair
    timestamp = (
        current_time.strftime("%Y-%m-%d"),
        current_time.strftime("%I:%M:%S %p")
    )

    return timestamp

# =========================================================
# FUNCTION: ADD TRANSACTION
# DRY PRINCIPLE:
# Same function handles deposit and withdrawal
# =========================================================

def add_transaction(transaction_type, amount):
    global balance
    
    if amount <= 0:
        print("\nAmount must be greater than zero.")
        return
    
    money_in = 0 
    money_out = 0 

    # -----------------------------
    # DEPOSIT LOGIC
    # -----------------------------

    if transaction_type == "DEPOSIT":
        balance += amount 
        money_in = amount

    
    # -----------------------------
    # WITHDRAW LOGIC
    # -----------------------------
    elif transaction_type == "WITHDRAW":
        total_withdrawal = amount + withdraw_fee

        if total_withdrawal > balance + overdraft :
            print("Insufficient funds")
            return
        
        balance -= total_withdrawal 
        money_out = total_withdrawal

    else:
        print("\nInvalid transaction type.")
        return
    
    # tuple returned from function
    mytimestamp = get_timestamp()
    
    # DICTIONARY: one transaction record
    transaction = {
        "type": transaction_type,
        "money_in": money_in,
        "money_out": money_out,
        "date": mytimestamp[0],
        "time": mytimestamp[1],
        "balance": balance
    }

    # LIST: add transaction to history
    transactions.append(transaction)
    
    # SET: stores unique transaction categories
    transaction_types.add(transaction_type)

    print(f"\n{transaction_type} successful.")
    print(f"Current Balance ${balance:.2f}")

    
# =========================================================
# FUNCTION: SHOW STATEMENT ON SCREEN
# =========================================================

def show_statement():

    if len(transactions) == 0:
        print("\nNo transactions to display.")
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

    for transaction in transactions:
        print(
            f"{transaction['date']:<12}"
            f"{transaction['time']:<12}"
            f"{transaction['type']:<15}"
            f"${transaction['money_in']:>11.2f}"
            f"${transaction['money_out']:>11.2f}"
            f"${transaction['balance']:>11.2f}"
        )

    print("-" * 75)
    print(f"{'Closing Balance':>63}: ${balance:.2f}")


# =========================================================
# FUNCTION: CREATE STATEMENT FILE
# =========================================================
# =========================================================
# FUNCTION: CREATE STATEMENT FILE
# =========================================================
def create_statement():

    if len(transactions) == 0:
        print("\nNo transactions to write.")
        return

    os.makedirs(FOLDER_PATH, exist_ok=True)

    file_path = os.path.join(FOLDER_PATH, FILE_NAME)

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
        file.write("============================================================\n")

    print("\nStatement created successfully.")
    print(f"Saved At: {file_path}")

# =========================================================
# FUNCTION: READ STATEMENT FILE
# =========================================================
def read_statement():

    file_path = os.path.join(FOLDER_PATH, FILE_NAME)

    try:
        with open(file_path, "r") as file:
            print("\n")
            print(file.read())

    except FileNotFoundError:
        print("\nStatement file not found.")


5
# =========================================================
# FUNCTION: SHOW UNIQUE TRANSACTION TYPES
# =========================================================
def show_transaction_types():

    if len(transaction_types) == 0:
        print("\nNo transaction types used yet.")
        return

    print("\nUnique Transaction Types:")

    for transaction_type in transaction_types:
        print(f"- {transaction_type}")



# =========================================================
# MAIN PROGRAM
# =========================================================
def main():

    while True:
        print("\n=========== BANK ACCOUNT ==============")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Statement")
        print("4. Create Statement File")
        print("5. Read Statement File")
        print("6. Show Transaction Types")
        print("7. Show Balance")
        print("8. Quit")
        print("=======================================")

        choice = input("Select an option: ")

        if choice == "1":
            amount = float(input("Enter deposit amount: $"))
            add_transaction("DEPOSIT", amount)

        elif choice == "2":
            amount = float(input("Enter withdrawal amount: $"))
            add_transaction("WITHDRAW", amount)

        elif choice == "3":
            show_statement()

        elif choice == "4":
            create_statement()

        elif choice == "5":
            read_statement()

        elif choice == "6":
            show_transaction_types()

        elif choice == "7":
            print(f"\nCurrent Balance: ${balance:.2f}")

        elif choice == "8":
            print("\nThank you for using our bank.")
            break

        else:
            print("\nInvalid option. Please try again.")


main()


















# Testing 
# mytimestamp = get_timestamp()
# print(f"Date is {mytimestamp[0]}")
# print(f"Time is {mytimestamp[1]}")