def add(num1, num2):
    print(f"Adding {num1} {num2} = {num1 + num2}")


def subtract(num1, num2):
    print(f"Subtracting {num1} {num2} = {num1 - num2}")

def multiply(num1, num2):
    print(f"Multiplying {num1} {num2} = {num1 * num2}")

def divide(num1, num2):
    print(f"Dividing {num1} {num2} = {num1 / num2}")


def main():

    n1 = float(input("Enter the 1st number: "))
    n2 = float(input("Enter the 2nd number: "))
    
    add(n1,n2)
    subtract(n1, n2)
    multiply(n1, n2)
    divide(n1, n2)



main()