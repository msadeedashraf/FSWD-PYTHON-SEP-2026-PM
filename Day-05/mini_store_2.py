store_name = "flipZila"

product_1 = "Laptop"
product_1_price = 1200
product_1_stock = 5

product_2 = "Keyboard"
product_2_price = 50
product_2_stock = 10

product_3 = "Mouse"
product_3_price = 20
product_3_stock = 15


print("===========================")
print(store_name)
print("===========================")

print(f"Product : {product_1}")
print(f"Price :$ {product_1_price}")
print(f"Stock : {product_1_stock}")

print(f"Product : {product_2}")
print(f"Price :$ {product_2_price}")
print(f"Stock : {product_2_stock}")

print(f"Product : {product_3}")
print(f"Price :$ {product_3_price}")
print(f"Stock : {product_3_stock}")

print("===========================")
print("Inventory Summary")
print("===========================")

total_inventory_value = (
    product_1_price*product_1_stock + 
    product_2_price*product_2_stock +
    product_3_price*product_3_stock 
    )
print(f"Total Inventory Value: ${total_inventory_value}")
print("===========================")