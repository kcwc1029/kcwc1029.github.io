```py
import customtkinter as ctk


### 基本視窗設定
ctk.set_appearance_mode("dark") # 設定外觀模式為深色模式
ctk.set_default_color_theme("blue") # 設定 CustomTkinter 預設主題顏色為藍色

window = ctk.CTk() # 建立 CustomTkinter 主視窗
window.title("飲料點餐機") # 設定視窗標題
window.geometry("520x720") # 設定視窗大小，寬 520、高 720


### 建立變數
drink_var = ctk.StringVar(value="紅茶") # 儲存目前選擇的飲料，預設為紅茶
size_var = ctk.StringVar(value="中杯") # 儲存目前選擇的杯型，預設為中杯

pearl_var = ctk.BooleanVar(value=False) # 儲存是否選擇珍珠，預設為未選取
pudding_var = ctk.BooleanVar(value=False) # 儲存是否選擇布丁，預設為未選取
coconut_var = ctk.BooleanVar(value=False) # 儲存是否選擇椰果，預設為未選取


### 飲料選擇函式
def on_drink_select(choice):
    print("目前選擇：", choice) # 顯示使用者從 OptionMenu 選擇的飲料


### 確認訂單函式
def order_drink():
    drink = drink_var.get() # 取得目前選擇的飲料
    size = size_var.get() # 取得目前選擇的杯型

    toppings = [] # 建立空串列，用來儲存使用者選擇的加料項目

    if pearl_var.get():
        toppings.append("珍珠") # 如果珍珠被勾選，就加入 toppings 串列

    if pudding_var.get():
        toppings.append("布丁") # 如果布丁被勾選，就加入 toppings 串列

    if coconut_var.get():
        toppings.append("椰果") # 如果椰果被勾選，就加入 toppings 串列


    ### 判斷是否有加料
    if len(toppings) == 0:
        topping_text = "不加料" # 如果 toppings 沒有任何內容，就顯示不加料
    else:
        topping_text = "、".join(toppings) # 將多個加料項目使用「、」連接成一段文字


    ### 顯示訂單結果
    result_label.configure(
        text=f"你的訂單\n\n"
             f"飲料：{drink}\n"
             f"杯型：{size}\n"
             f"加料：{topping_text}" # 更新 Label 顯示完整訂單內容
    )


### 建立標題 Label
title_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="飲料點餐機", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 30, "bold") # 設定字型、字體大小與粗體
)

title_label.pack(pady=(25, 15)) # 上方增加 25、下方增加 15 像素的間距


### 建立飲料品項標題
drink_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="選擇飲料", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 20, "bold") # 設定字型、字體大小與粗體
)

drink_label.pack(pady=(10, 5)) # 上方增加 10、下方增加 5 像素的間距


### 建立 OptionMenu
drink_menu = ctk.CTkOptionMenu(
    window, # 指定 OptionMenu 放在主視窗 window 裡面
    values=[
        "紅茶",
        "綠茶",
        "奶茶",
        "烏龍茶",
        "水果茶"
    ], # 設定下拉選單可以選擇的飲料項目
    variable=drink_var, # 將目前選擇的飲料儲存在 drink_var
    command=on_drink_select, # 每次選擇飲料時執行 on_drink_select 函式
    width=220, # 設定下拉選單寬度
    height=40, # 設定下拉選單高度
    font=("Microsoft JhengHei", 18) # 設定字型與字體大小
)

drink_menu.pack(pady=10) # 將 OptionMenu 放入視窗


### 建立杯型標題
size_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="選擇杯型", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 20, "bold") # 設定字型、字體大小與粗體
)

size_label.pack(pady=(20, 10)) # 上方增加 20、下方增加 10 像素的間距


### 建立中杯 RadioButton
medium_radio = ctk.CTkRadioButton(
    window, # 指定 RadioButton 放在主視窗 window 裡面
    text="中杯", # 設定選項顯示的文字
    variable=size_var, # 將選擇結果儲存在 size_var
    value="中杯", # 選取這個按鈕時，將 size_var 設定為「中杯」
    font=("Microsoft JhengHei", 18) # 設定字型與字體大小
)

medium_radio.pack(pady=5) # 將中杯 RadioButton 放入視窗


### 建立大杯 RadioButton
large_radio = ctk.CTkRadioButton(
    window, # 指定 RadioButton 放在主視窗 window 裡面
    text="大杯", # 設定選項顯示的文字
    variable=size_var, # 與中杯共用同一個 size_var，因此兩者只能選一個
    value="大杯", # 選取這個按鈕時，將 size_var 設定為「大杯」
    font=("Microsoft JhengHei", 18) # 設定字型與字體大小
)

large_radio.pack(pady=5) # 將大杯 RadioButton 放入視窗


### 建立加料標題
topping_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="選擇加料", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 20, "bold") # 設定字型、字體大小與粗體
)

topping_label.pack(pady=(20, 10)) # 上方增加 20、下方增加 10 像素的間距


### 建立珍珠 CheckBox
pearl_checkbox = ctk.CTkCheckBox(
    window, # 指定 CheckBox 放在主視窗 window 裡面
    text="珍珠", # 設定選項顯示的文字
    variable=pearl_var, # 將是否勾選的狀態儲存在 pearl_var
    font=("Microsoft JhengHei", 18) # 設定字型與字體大小
)

pearl_checkbox.pack(pady=5) # 將珍珠 CheckBox 放入視窗


### 建立布丁 CheckBox
pudding_checkbox = ctk.CTkCheckBox(
    window, # 指定 CheckBox 放在主視窗 window 裡面
    text="布丁", # 設定選項顯示的文字
    variable=pudding_var, # 將是否勾選的狀態儲存在 pudding_var
    font=("Microsoft JhengHei", 18) # 設定字型與字體大小
)

pudding_checkbox.pack(pady=5) # 將布丁 CheckBox 放入視窗


### 建立椰果 CheckBox
coconut_checkbox = ctk.CTkCheckBox(
    window, # 指定 CheckBox 放在主視窗 window 裡面
    text="椰果", # 設定選項顯示的文字
    variable=coconut_var, # 將是否勾選的狀態儲存在 coconut_var
    font=("Microsoft JhengHei", 18) # 設定字型與字體大小
)

coconut_checkbox.pack(pady=5) # 將椰果 CheckBox 放入視窗


### 建立確認按鈕
order_button = ctk.CTkButton(
    window, # 指定 Button 放在主視窗 window 裡面
    text="確認訂單", # 設定按鈕顯示的文字
    font=("Microsoft JhengHei", 20, "bold"), # 設定字型、字體大小與粗體
    width=220, # 設定按鈕寬度
    height=50, # 設定按鈕高度
    command=order_drink # 按下按鈕時執行 order_drink 函式
)

order_button.pack(pady=25) # 將確認訂單按鈕放入視窗


### 建立結果 Label
result_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="尚未建立訂單", # 設定訂單尚未送出時的預設文字
    font=("Microsoft JhengHei", 20, "bold"), # 設定字型、字體大小與粗體
    justify="center" # 設定多行文字置中對齊
)

result_label.pack(pady=10) # 將結果 Label 放入視窗


### 啟動視窗
window.mainloop() # 啟動事件迴圈，讓視窗持續顯示並等待使用者操作
```
