```py
import customtkinter as ctk


### 基本視窗設定
ctk.set_appearance_mode("dark") # 設定外觀模式為深色模式
ctk.set_default_color_theme("blue") # 設定 CustomTkinter 預設主題顏色為藍色

app = ctk.CTk() # 建立 CustomTkinter 主視窗
app.title("假登入系統") # 設定視窗標題
app.geometry("420x380") # 設定視窗大小，寬 420、高 380


### 建立標題 Label
title_label = ctk.CTkLabel(
    app, # 指定 Label 放在主視窗 app 裡面
    text="會員登入系統", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 30, "bold") # 設定字型、字體大小與粗體
)

title_label.pack(pady=(40, 25)) # 上方增加 40、下方增加 25 像素的間距


### 建立帳號輸入框
username_entry = ctk.CTkEntry(
    app, # 指定 Entry 放在主視窗 app 裡面
    placeholder_text="請輸入帳號", # 設定輸入框尚未輸入內容時的提示文字
    font=("Microsoft JhengHei", 18), # 設定字型與字體大小
    width=260 # 設定輸入框寬度
)

username_entry.pack(pady=10) # 將帳號輸入框放入視窗


### 建立密碼輸入框
password_entry = ctk.CTkEntry(
    app, # 指定 Entry 放在主視窗 app 裡面
    placeholder_text="請輸入密碼", # 設定輸入框尚未輸入內容時的提示文字
    font=("Microsoft JhengHei", 18), # 設定字型與字體大小
    width=260, # 設定輸入框寬度
    show="*" # 將輸入的密碼顯示為 *，避免直接顯示密碼內容
)

password_entry.pack(pady=10) # 將密碼輸入框放入視窗


### 建立結果 Label
result_label = ctk.CTkLabel(
    app, # 指定 Label 放在主視窗 app 裡面
    text="", # 一開始不顯示任何文字
    font=("Microsoft JhengHei", 20) # 設定字型與字體大小
)

result_label.pack(pady=20) # 將結果 Label 放入視窗


### 登入判斷函式
def login():
    username = username_entry.get() # 取得使用者輸入的帳號
    password = password_entry.get() # 取得使用者輸入的密碼

    if username == "admin" and password == "1234":
        result_label.configure(text="登入成功") # 帳號與密碼都正確時顯示登入成功
    else:
        result_label.configure(text="密碼錯誤") # 帳號或密碼任一錯誤時顯示錯誤訊息


### 建立登入按鈕
login_button = ctk.CTkButton(
    app, # 指定 Button 放在主視窗 app 裡面
    text="登入", # 設定按鈕顯示的文字
    font=("Microsoft JhengHei", 20), # 設定字型與字體大小
    width=180, # 設定按鈕寬度
    command=login # 按下按鈕時執行 login 函式
)

login_button.pack(pady=10) # 將登入按鈕放入視窗


### 啟動視窗
app.mainloop() # 啟動事件迴圈，讓視窗持續顯示並等待使用者操作
```
