# 檔案名稱: makefood.py

# 定義一個製作冰淇淋的函式
def make_icecream(*toppings):
    """ 列出製作冰淇淋的配料 """
    print("你點的冰淇淋配料如下：")
    for topping in toppings:
        print("--- ", topping)

# 定義一個製作飲料的函式
def make_drink(size, drink):
    """ 輸出飲料的資訊 """
    print(f"飲料大小: {size}, 飲料名稱: {drink}")