class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.__price = 0
        self.__quantity = 0
        self.set_price(price)
        self.set_quantity(quantity)

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if price >= 0:
            self.__price = price
        else:
            print("Invalid value.")

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        if quantity >= 0:
            self.__quantity = quantity
        else:
            print("Invalid value.")

    def get_total_value(self):
        return self.__price * self.__quantity

    def display_status(self):
        print(f"Product: {self.name}")
        print(f"Price: ${self.get_price()}")
        print(f"Quantity: {self.get_quantity()}")
        print(f"Total Value: ${self.get_total_value()}")


# 讀取輸入
name, price, quantity = input().split()
product = Product(name, int(price), int(quantity))

action1, value1 = input().split()
if action1 == "set_price":
    product.set_price(int(value1))

action2, value2 = input().split()
if action2 == "set_quantity":
    product.set_quantity(int(value2))

action3, value3 = input().split()
if action3 == "set_quantity":
    product.set_quantity(int(value3))

product.display_status()