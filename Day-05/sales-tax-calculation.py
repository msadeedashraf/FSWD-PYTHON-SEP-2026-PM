product_name = input("Enter the product name : ")
price = float(input("Enter the price: "))

taxRate = 0.13
tax_amount = price * taxRate
final_price = price + tax_amount

print("===============================")
print("         Receipt               ")
print("===============================")

print(f"Product : {product_name}")
print(f"Original Price : ${price} ")
print(f"Tax : ${tax_amount} ")
print(f"Final Price : ${final_price} ")

print("===============================")
print("       End of Receipt          ")
print("===============================")

