class Banks():
    bankname = "台南銀行"
    def __init__(self, name, money):
        self.name = name # 公有屬性
        self.__money = money # 私有屬性 (前面加了 __)
        self.__rate = 30 # 私有屬性，預設匯率

    def get_money(self): # 定義一個取得餘額的方法
        return self.__money
    def save_money(self, money):
        self.__money += money
        print(f"存錢{money}完成")
    def withdraw_money(self, money):
        self.__money -= money
        print(f"提款{money}完成")
    def __cal_rate(self): # 台幣換算美金 => 私有方法
        return int(self.__money/self.__rate)
    # 私有方法：計算目前餘額可換算的美金
    def __cal_rate(self): 
        return int(self.__money / self.__rate) # 在類別內部，可以自由存取自己的私有屬性 self.__money 和 self.__rate
    
    # 公有方法：提供給外部呼叫，用來將台幣餘額換算成美金
    def twd_to_usa(self):
        usa_dollar = self.__cal_rate() # 呼叫內部的私有方法來完成計算
        print(f"目前的台幣餘額 {self.__money} 元，約可兌換成美金 {usa_dollar} 元")
        return usa_dollar
    

hungbank = Banks('JF', 1000) # 建立 hungbank 物件，並傳入初始值
hungbank.__money = -10000 # 這行是無效的，無法從外部竄改私有屬性
print(f"{hungbank.name} 目前的存款是: {hungbank.get_money()} 元") 

hungbank.save_money(200)
hungbank.withdraw_money(100)
print(f"{hungbank.name} 目前的存款是: {hungbank.get_money()} 元") 

# 呼叫換匯功能
hungbank.twd_to_usa()

# 再次存款後換匯
hungbank.save_money(5000)
print(f"{hungbank.name} 目前的存款是: {hungbank.get_money()} 元")
hungbank.twd_to_usa()