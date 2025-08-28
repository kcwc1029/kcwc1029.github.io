class Character:
    def __init__(self, name):
        self.name = name
        self.__level = 1
        self.__exp = 0
        self.__max_hp = self.__level * 10
        self.__hp = self.__max_hp

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        if value > self.__max_hp:
            self.__hp = self.__max_hp
        elif value < 0:
            self.__hp = 0
        else:
            self.__hp = value

    def __level_up(self):
        self.__level += 1
        self.__exp = 0 # 歸零或減去升級所需經驗值，此處簡化為歸零
        self.__max_hp = self.__level * 10
        self.hp = self.__max_hp # 補滿血
        print(f"{self.name} has reached level {self.__level}!")


    def gain_exp(self, points):
        self.__exp += points
        while self.__exp >= self.__level * 100:
            self.__exp -= self.__level * 100
            self.__level_up()
            
    def display_status(self):
        print(f"Name: {self.name}")
        print(f"Level: {self.__level}")
        print(f"HP: {self.__hp}/{self.__max_hp}")
        print(f"EXP: {self.__exp}")

# 讀取輸入
char_name = input()
character = Character(char_name)

while True:
    line = input()
    if line == "END":
        break
    action, value = line.split()
    if action == "set_hp":
        character.hp = int(value)
    elif action == "gain_exp":
        character.gain_exp(int(value) )

character.display_status()