import customtkinter as ctk


### 基本視窗設定

ctk.set_appearance_mode("dark") # 設定外觀模式為深色模式
ctk.set_default_color_theme("blue") # 設定 CustomTkinter 預設主題顏色為藍色

window = ctk.CTk() # 建立 CustomTkinter 主視窗
window.title("飲料點餐機") # 設定視窗標題
window.geometry("520x720") # 設定視窗大小


### 建立變數

drink_var = ctk.StringVar(value="紅茶") # 儲存目前選擇的飲料

size_var = ctk.StringVar(value="中杯") # 儲存目前選擇的杯型

pearl_var = ctk.BooleanVar(value=False) # 儲存是否加珍珠
pudding_var = ctk.BooleanVar(value=False) # 儲存是否加布丁
coconut_var = ctk.BooleanVar(value=False) # 儲存是否加椰果


### 飲料選擇函式

def on_drink_select(choice):

    print("目前選擇：", choice) # 顯示 OptionMenu 選擇的飲料


### 確認訂單函式

def order_drink():

    drink = drink_var.get() # 取得目前選擇的飲料
    size = size_var.get() # 取得目前選擇的杯型

    toppings = [] # 建立串列，用來儲存加料項目

    if pearl_var.get():
        toppings.append("珍珠")

    if pudding_var.get():
        toppings.append("布丁")

    if coconut_var.get():
        toppings.append("椰果")


    ### 判斷是否有加料

    if len(toppings) == 0:
        topping_text = "不加料"
    else:
        topping_text = "、".join(toppings)


    ### 顯示訂單結果

    result_label.configure(
        text=f"你的訂單\n\n"
             f"飲料：{drink}\n"
             f"杯型：{size}\n"
             f"加料：{topping_text}"
    )


### 建立標題 Label

title_label = ctk.CTkLabel(
    window,
    text="飲料點餐機",
    font=("Microsoft JhengHei", 30, "bold")
)

title_label.pack(pady=(25, 15))


### 飲料品項標題

drink_label = ctk.CTkLabel(
    window,
    text="選擇飲料",
    font=("Microsoft JhengHei", 20, "bold")
)

drink_label.pack(pady=(10, 5))


### 建立 OptionMenu

drink_menu = ctk.CTkOptionMenu(
    window,
    values=[
        "紅茶",
        "綠茶",
        "奶茶",
        "烏龍茶",
        "水果茶"
    ],
    variable=drink_var,
    command=on_drink_select,
    width=220,
    height=40,
    font=("Microsoft JhengHei", 18)
)

drink_menu.pack(pady=10)


### 杯型標題

size_label = ctk.CTkLabel(
    window,
    text="選擇杯型",
    font=("Microsoft JhengHei", 20, "bold")
)

size_label.pack(pady=(20, 10))


### 建立 RadioButton

medium_radio = ctk.CTkRadioButton(
    window,
    text="中杯",
    variable=size_var,
    value="中杯",
    font=("Microsoft JhengHei", 18)
)

medium_radio.pack(pady=5)


large_radio = ctk.CTkRadioButton(
    window,
    text="大杯",
    variable=size_var,
    value="大杯",
    font=("Microsoft JhengHei", 18)
)

large_radio.pack(pady=5)


### 加料標題

topping_label = ctk.CTkLabel(
    window,
    text="選擇加料",
    font=("Microsoft JhengHei", 20, "bold")
)

topping_label.pack(pady=(20, 10))


### 建立 CheckBox

pearl_checkbox = ctk.CTkCheckBox(
    window,
    text="珍珠",
    variable=pearl_var,
    font=("Microsoft JhengHei", 18)
)

pearl_checkbox.pack(pady=5)


pudding_checkbox = ctk.CTkCheckBox(
    window,
    text="布丁",
    variable=pudding_var,
    font=("Microsoft JhengHei", 18)
)

pudding_checkbox.pack(pady=5)


coconut_checkbox = ctk.CTkCheckBox(
    window,
    text="椰果",
    variable=coconut_var,
    font=("Microsoft JhengHei", 18)
)

coconut_checkbox.pack(pady=5)


### 建立確認按鈕

order_button = ctk.CTkButton(
    window,
    text="確認訂單",
    font=("Microsoft JhengHei", 20, "bold"),
    width=220,
    height=50,
    command=order_drink
)

order_button.pack(pady=25)


### 建立結果 Label

result_label = ctk.CTkLabel(
    window,
    text="尚未建立訂單",
    font=("Microsoft JhengHei", 20, "bold"),
    justify="center"
)

result_label.pack(pady=10)


### 啟動視窗

window.mainloop()