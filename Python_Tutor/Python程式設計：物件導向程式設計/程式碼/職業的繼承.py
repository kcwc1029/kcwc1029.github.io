class Adventurer:
    """
    父類別 (Base Class)
    """
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def show_status(self):
        return f"Name: {self.name}, HP: {self.hp}"

class Knight(Adventurer):
    """
    子類別 (Derived Class)，繼承 Adventurer
    """
    def __init__(self, name, hp, armor):
        # 使用 super() 呼叫父類別的 __init__ 來初始化 name 和 hp
        super().__init__(name, hp)
        # 初始化自己獨有的屬性
        self.armor = armor

    # 覆寫 (Override) 父類別的 show_status 方法
    def show_status(self):
        return f"Name: {self.name}, HP: {self.hp}, Armor: {self.armor}"

    # 子類別自己獨有的方法
    def defend(self):
        return f"{self.name} is defending with armor {self.armor}!"

# 讀取輸入
name, hp = input().split()
hp = int(hp)
armor = int(input())

# 建立 Knight 物件
knight = Knight(name, hp, armor)

# 呼叫方法並印出結果
print(knight.show_status())
print(knight.defend())