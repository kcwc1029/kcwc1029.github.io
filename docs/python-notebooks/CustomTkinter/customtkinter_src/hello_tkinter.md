```py
import tkinter as tk


### 按下按鈕後執行
def say_hello():
    label.config(text="哈囉！你按下按鈕了") # 修改 Label 顯示的文字


### 建立主視窗
window = tk.Tk() # 建立 Tkinter 主視窗
window.title("Tkinter 第一個程式") # 設定視窗標題
window.geometry("400x200") # 設定視窗大小，寬 400、高 200


### 建立文字標籤
label = tk.Label(
    window, # 指定 Label 放在主視窗 window 裡面
    text="歡迎來到 Tkinter", # 設定 Label 顯示的文字
    font=("Arial", 20) # 設定字型為 Arial、字體大小為 20
)

label.pack(pady=30) # 將 Label 放入視窗，上下增加 30 像素的間距


### 建立按鈕
button = tk.Button(
    window, # 指定 Button 放在主視窗 window 裡面
    text="點我", # 設定按鈕顯示的文字
    font=("Arial", 16), # 設定字型為 Arial、字體大小為 16
    command=say_hello # 按下按鈕時執行 say_hello 函式
)

button.pack() # 將 Button 放入視窗


### 啟動視窗
window.mainloop() # 啟動 Tkinter 事件迴圈，讓視窗持續顯示並等待使用者操作
```
