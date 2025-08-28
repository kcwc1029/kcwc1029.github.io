class Account:
    def __init__(self, name, account_number, balance):
        self.__name = name
        self.__account_number = account_number
        if balance >= 0:
            self.__balance = balance
        else:
            self.__balance = 0

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            print("Invalid operation.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Invalid operation.")
            
    def display_status(self):
        print(f"Account {self.__account_number} ({self.__name}) has ${self.__balance}.")

# 讀取輸入
init_name, init_acc_num, init_balance = input().split()
acc = Account(init_name, init_acc_num, int(init_balance))

op1, val1 = input().split()
if op1 == "deposit":
    acc.deposit(int(val1))
elif op1 == "withdraw":
    acc.withdraw(int(val1))

op2, val2 = input().split()
if op2 == "deposit":
    acc.deposit(int(val2))
elif op2 == "withdraw":
    acc.withdraw(int(val2))

op3, val3 = input().split()
if op3 == "deposit":
    acc.deposit(int(val3))
elif op3 == "withdraw":
    acc.withdraw(int(val3))

acc.display_status()