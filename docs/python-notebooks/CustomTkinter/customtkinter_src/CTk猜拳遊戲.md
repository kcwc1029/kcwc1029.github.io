```py
import random
from io import BytesIO

import customtkinter as ctk
import requests
from PIL import Image


### 基本視窗設定
ctk.set_appearance_mode("dark") # 設定外觀模式為深色模式
ctk.set_default_color_theme("blue") # 設定 CustomTkinter 預設主題顏色為藍色

window = ctk.CTk() # 建立 CustomTkinter 主視窗
window.title("猜拳遊戲") # 設定視窗標題
window.geometry("500x700") # 設定視窗大小，寬 500、高 700


### 下載圖片
image_url = "https://i.pinimg.com/736x/e9/70/42/e970420a723a7dc47f5342556a9d0661.jpg" # 設定網路圖片網址

response = requests.get(image_url) # 從指定網址下載圖片
image_data = BytesIO(response.content) # 將下載的二進位資料轉成記憶體檔案
image = Image.open(image_data) # 使用 PIL 開啟圖片
image = image.resize((320, 320)) # 將圖片調整為寬 320、高 320


### 轉成 CTkImage
ctk_image = ctk.CTkImage(
    light_image=image, # Light 模式使用的圖片
    dark_image=image, # Dark 模式使用的圖片
    size=(320, 320) # 設定圖片顯示大小，寬 320、高 320
)


### 猜拳判斷函式
def play_game(user_choice):
    choices = ["石頭", "剪刀", "布"] # 建立電腦可以選擇的猜拳內容
    computer_choice = random.choice(choices) # 隨機選擇石頭、剪刀或布

    if user_choice == computer_choice:
        result = "平手" # 玩家與電腦出一樣的拳時為平手

    elif user_choice == "石頭" and computer_choice == "剪刀":
        result = "你贏了" # 石頭贏剪刀

    elif user_choice == "剪刀" and computer_choice == "布":
        result = "你贏了" # 剪刀贏布

    elif user_choice == "布" and computer_choice == "石頭":
        result = "你贏了" # 布贏石頭

    else:
        result = "你輸了" # 其他情況代表電腦獲勝

    result_label.configure(
        text=f"你出：{user_choice}\n電腦出：{computer_choice}\n{result}" # 更新猜拳結果文字
    )


### 建立標題 Label
title_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="猜拳遊戲", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 30, "bold") # 設定字型、字體大小與粗體
)

title_label.pack(pady=(20, 10)) # 上方增加 20、下方增加 10 像素的間距


### 建立圖片 Label
image_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="", # 清空文字，只顯示圖片
    image=ctk_image # 設定 Label 顯示的圖片
)

image_label.pack(pady=10) # 將圖片 Label 放入視窗，上下增加 10 像素的間距


### 建立說明 Label
hint_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="請選擇你要出的拳", # 顯示操作提示文字
    font=("Microsoft JhengHei", 20) # 設定字型與字體大小
)

hint_label.pack(pady=10) # 將 Label 放入視窗，上下增加 10 像素的間距


### 建立結果 Label
result_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="你出：尚未選擇\n電腦出：尚未選擇\n等待開始", # 設定遊戲尚未開始時的預設文字
    font=("Microsoft JhengHei", 22), # 設定字型與字體大小
    justify="left" # 設定多行文字靠左對齊
)

result_label.pack(pady=20) # 將 Label 放入視窗，上下增加 20 像素的間距


### 建立按鈕區塊
button_frame = ctk.CTkFrame(window) # 建立 Frame，用來集中放置三個猜拳按鈕
button_frame.pack(pady=10) # 將 Frame 放入視窗，上下增加 10 像素的間距


### 建立石頭按鈕
rock_button = ctk.CTkButton(
    button_frame, # 指定 Button 放在 button_frame 裡面
    text="石頭", # 設定按鈕文字
    font=("Microsoft JhengHei", 18, "bold"), # 設定字型、字體大小與粗體
    width=120, # 設定按鈕寬度
    height=45, # 設定按鈕高度
    command=lambda: play_game("石頭") # 按下按鈕時呼叫 play_game，並傳入「石頭」
)

rock_button.grid(row=0, column=0, padx=8) # 將按鈕放在第 0 列、第 0 欄，左右增加 8 像素間距


### 建立剪刀按鈕
scissors_button = ctk.CTkButton(
    button_frame, # 指定 Button 放在 button_frame 裡面
    text="剪刀", # 設定按鈕文字
    font=("Microsoft JhengHei", 18, "bold"), # 設定字型、字體大小與粗體
    width=120, # 設定按鈕寬度
    height=45, # 設定按鈕高度
    command=lambda: play_game("剪刀") # 按下按鈕時呼叫 play_game，並傳入「剪刀」
)

scissors_button.grid(row=0, column=1, padx=8) # 將按鈕放在第 0 列、第 1 欄


### 建立布按鈕
paper_button = ctk.CTkButton(
    button_frame, # 指定 Button 放在 button_frame 裡面
    text="布", # 設定按鈕文字
    font=("Microsoft JhengHei", 18, "bold"), # 設定字型、字體大小與粗體
    width=120, # 設定按鈕寬度
    height=45, # 設定按鈕高度
    command=lambda: play_game("布") # 按下按鈕時呼叫 play_game，並傳入「布」
)

paper_button.grid(row=0, column=2, padx=8) # 將按鈕放在第 0 列、第 2 欄


### 啟動視窗
window.mainloop() # 啟動事件迴圈，讓視窗持續顯示並等待使用者操作
```
