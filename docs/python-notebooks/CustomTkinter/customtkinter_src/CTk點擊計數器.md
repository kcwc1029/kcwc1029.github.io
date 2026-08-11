```py
import customtkinter as ctk
import requests

from io import BytesIO
from PIL import Image


### 基本視窗設定
ctk.set_appearance_mode("dark") # 設定外觀模式為深色模式
ctk.set_default_color_theme("blue") # 設定 CustomTkinter 預設主題顏色為藍色

window = ctk.CTk() # 建立 CustomTkinter 主視窗
window.title("做功德") # 設定視窗標題
window.geometry("500x650") # 設定視窗大小，寬 500、高 650


### 設定計數變數
count = 15 # 設定計數器初始值為 15


### 按鈕事件函式
def add_count():
    global count # 宣告使用外部的全域變數 count
    count += 1 # 每按一次按鈕，就將 count 加 1
    count_label.configure(text=f"目前點擊次數：{count}") # 更新 Label 顯示的點擊次數


### 下載圖片
image_url = "https://i.pinimg.com/736x/c4/88/ff/c488ff6a0062b80ddfdcd404c3f282fa.jpg" # 設定網路圖片網址

response = requests.get(image_url) # 從指定網址下載圖片
image_data = BytesIO(response.content) # 將下載的二進位資料轉成記憶體檔案
image = Image.open(image_data) # 使用 PIL 開啟圖片


### 調整圖片大小
image = image.resize((300, 300)) # 將圖片調整為寬 300、高 300


### 轉成 CTkImage
ctk_image = ctk.CTkImage(
    light_image=image, # Light 模式使用的圖片
    dark_image=image, # Dark 模式使用的圖片
    size=(300, 300) # 設定圖片顯示大小，寬 300、高 300
)


### 建立標題 Label
title_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="點擊計數器", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 28, "bold") # 設定字型、字體大小與粗體
)

title_label.pack(pady=(20, 10)) # 上方增加 20、下方增加 10 像素的間距


### 建立圖片 Label
image_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text="", # 清空文字，只顯示圖片
    image=ctk_image # 設定 Label 顯示的圖片
)

image_label.pack(pady=10) # 將圖片 Label 放入視窗，上下增加 10 像素的間距


### 建立顯示次數 Label
count_label = ctk.CTkLabel(
    window, # 指定 Label 放在主視窗 window 裡面
    text=f"目前點擊次數：{count}", # 顯示目前的 count 數值
    font=("Microsoft JhengHei", 22) # 設定字型與字體大小
)

count_label.pack(pady=20) # 將 Label 放入視窗，上下增加 20 像素的間距


### 建立 +1 按鈕
add_button = ctk.CTkButton(
    window, # 指定 Button 放在主視窗 window 裡面
    text="按我 +1", # 設定按鈕顯示的文字
    font=("Microsoft JhengHei", 20, "bold"), # 設定字型、字體大小與粗體
    width=180, # 設定按鈕寬度
    height=50, # 設定按鈕高度
    command=add_count # 按下按鈕時執行 add_count 函式
)

add_button.pack(pady=20) # 將按鈕放入視窗，上下增加 20 像素的間距


### 啟動視窗
window.mainloop() # 啟動事件迴圈，讓視窗持續顯示並等待使用者操作
```
