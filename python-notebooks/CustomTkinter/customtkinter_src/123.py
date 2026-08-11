import random
from io import BytesIO

import customtkinter as ctk
import requests
from PIL import Image


### 基本視窗設定
ctk.set_appearance_mode("dark") # 設定外觀模式為深色模式
ctk.set_default_color_theme("blue") # 設定 CustomTkinter 預設主題顏色為藍色

window = ctk.CTk() # 建立 CustomTkinter 主視窗
window.title("一番賞抽獎機") # 設定視窗標題
window.geometry("520x720") # 設定視窗大小，寬 520、高 720


### 下載圖片
image_url = "https://i.pinimg.com/1200x/3e/7b/01/3e7b015f62fa554f250fdfde139cc290.jpg" # 設定網路圖片網址

response = requests.get(image_url) # 從指定網址下載圖片
image_data = BytesIO(response.content) # 將下載的二進位圖片資料轉成記憶體檔案
image = Image.open(image_data) # 使用 PIL 開啟圖片
image = image.resize((320, 320)) # 將圖片調整為寬 320、高 320


### 轉成 CTkImage
ctk_image = ctk.CTkImage(
    light_image=image, # Light 模式使用的圖片
    dark_image=image, # Dark 模式使用的圖片
    size=(320, 320) # 設定圖片顯示大小，寬 320、高 320
)


### 建立一番賞獎池
prizes = [
    "A賞：超大角色公仔",
    "B賞：精緻角色立牌",
    "C賞：角色抱枕",
    "D賞：造型馬克杯",
    "E賞：壓克力吊飾",
    "F賞：收藏卡片",
    "G賞：小貼紙組",
    "LAST賞：隱藏版限定公仔"
]


### 抽獎函式
def draw_prize():
    prize = random.choice(prizes) # 從 prizes 獎池中隨機抽出一個獎品

    result_label.configure(
        text=f"抽獎結果\n\n恭喜抽中：\n{prize}" # 更新 Label，顯示本次抽獎結果
    )


### 建立標題 Label
title_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="一番賞抽獎機", # 設定 Label 顯示的文字
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
    text="按下按鈕，看看你抽到哪一賞！", # 顯示操作提示文字
    font=("Microsoft JhengHei", 20) # 設定字型與字體大小
)

hint_label.pack(pady=10) # 將 Label 放入視窗，上下增加 10 像素的間距


### 建立結果 Label
result_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="尚未抽獎\n\n準備好就按下去！", # 設定尚未抽獎時的預設文字
    font=("Microsoft JhengHei", 24, "bold"), # 設定字型、字體大小與粗體
    justify="center" # 設定多行文字置中對齊
)

result_label.pack(pady=25) # 將 Label 放入視窗，上下增加 25 像素的間距


### 建立抽獎按鈕
draw_button = ctk.CTkButton(
    window, # 指定 Button 放在主視窗 window 裡面
    text="開始抽獎", # 設定按鈕顯示的文字
    font=("Microsoft JhengHei", 22, "bold"), # 設定字型、字體大小與粗體
    width=220, # 設定按鈕寬度
    height=55, # 設定按鈕高度
    command=draw_prize # 按下按鈕時執行 draw_prize 函式
)

draw_button.pack(pady=15) # 將按鈕放入視窗，上下增加 15 像素的間距


### 啟動視窗
window.mainloop() # 啟動事件迴圈，讓視窗持續顯示並等待使用者操作