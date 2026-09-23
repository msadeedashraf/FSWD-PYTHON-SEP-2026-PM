def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2


def main():

    print("=======================================")
    print("\t\tCalculator")
    print("=======================================")
    print("\t\t1. Add")
    print("\t\t2. Subtract")
    print("\t\t3. Multiply")
    print("\t\t4. Divide")
    print("\t\t0. Quit")
    print("=======================================")

    choice = input("Enter the choice (0-4):")

    if choice == "0":
        print("Calculator Closed")
    
    elif choice == "1":
        n1 = float(input("Enter the 1st number: "))
        n2 = float(input("Enter the 2nd number: "))
        result = add(n1,n2)
        print(f"Adding {n1} and {n2} =  {result}")

    elif choice == "2":
        n1 = float(input("Enter the 1st number: "))
        n2 = float(input("Enter the 2nd number: "))
        result = subtract(n1,n2)
        print(f"Subtracting {n1} and {n2} =  {result}")


    elif choice == "3":
        n1 = float(input("Enter the 1st number: "))
        n2 = float(input("Enter the 2nd number: "))
        result = multiply(n1,n2)
        print(f"Multiplying {n1} and {n2} =  {result}")
        
    elif choice == "4":
        n1 = float(input("Enter the 1st number: "))
        n2 = float(input("Enter the 2nd number: "))
        result =3e(n1,n2)
        print(f"Dividing {n1} and {n2} =  {result}")






main()