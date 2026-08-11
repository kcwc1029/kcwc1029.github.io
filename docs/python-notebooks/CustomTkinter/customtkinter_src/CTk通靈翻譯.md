```py
import random
from io import BytesIO

import customtkinter as ctk
import requests
from PIL import Image


### 基本視窗設定
ctk.set_appearance_mode("dark") # 設定外觀模式為深色模式
ctk.set_default_color_theme("blue") # 設定 CustomTkinter 預設主題顏色為藍色

app = ctk.CTk() # 建立 CustomTkinter 主視窗
app.title("社畜翻譯機") # 設定視窗標題
app.geometry("620x760") # 設定視窗大小，寬 620、高 760


### 下載圖片
image_url = "https://i.pinimg.com/1200x/28/23/89/282389c136060ed941985b879cc992ab.jpg" # 設定網路圖片網址

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


### 建立隨機翻譯內容
psychic_replies = [
    "宇宙看完沉默三秒：你今天還是先躺平吧",
    "祖先集體搖頭：這個班不上也罷",
    "靈魂翻譯：我不是累，我只是對上班失去信仰",
    "水晶球顯示：你的待辦事項正在無限繁殖",
    "神明已讀不回：這個問題祂也處理不了",
    "通靈結果：你的靈魂今天拒絕營業",
    "你這句話的真實意思是：我想下班",
    "宇宙冷笑：你以為今天可以準時走？",
    "你的氣場現在像星期一早上八點半",
    "前世查詢：你上輩子可能欠主管很多錢",
    "靈界一致判定：今天適合摸魚，不宜努力",
    "系統提示：你的工作能量剩餘 1%",
    "塔羅牌顯示：今天最大的敵人是會議",
    "祖先傳話：差不多就好，不要太認真",
    "通靈失敗，因為你的未來被 Excel 擋住了",
    "你現在的能量值：只夠打開公司群組",
    "神明嘆氣：怎麼又是工作上的事情",
    "靈魂目前狀態：人在線上，心已下班",
    "翻譯完成：我看起來很正常，其實只想放假",
    "宇宙直接吐槽：你不是效率低，是事情太多",
    "磁場顯示：附近有主管正在靠近",
    "你的心聲：誰再叫我加油，我就把工作轉給他",
    "通靈機嚴正警告：再開一場會議就要開始擺爛",
    "你的人生目前像一份永遠改不完的簡報",
    "靈界笑翻：你居然還相信今天可以準時下班",
    "翻譯結果：我沒有不開心，我只是不想上班",
    "宇宙回覆：休假申請已收到，主管尚未批准",
    "你現在像一台開了 87 個分頁的電腦",
    "神明表示：這題太難，建議先去買杯飲料",
    "最後通牒：今天再努力五分鐘就可以開始摸魚"
]


### 建立標題 Label
title_label = ctk.CTkLabel(
    app, # 指定 Label 放在主視窗 app 裡面
    text="社畜翻譯機", # 設定 Label 顯示的文字
    font=("Microsoft JhengHei", 34, "bold") # 設定字型、字體大小與粗體
)

title_label.pack(pady=(25, 10)) # 上方增加 25、下方增加 10 像素的間距


### 建立圖片 Label
image_label = ctk.CTkLabel(
    app, # 指定 Label 放在主視窗 app 裡面
    text="", # 清空文字，只顯示圖片
    image=ctk_image # 設定 Label 顯示的圖片
)

image_label.pack(pady=10) # 將圖片 Label 放入視窗


### 建立提示文字 Label
hint_label = ctk.CTkLabel(
    app, # 指定 Label 放在主視窗 app 裡面
    text="輸入一句正常話，讓程式幫你亂翻", # 顯示操作提示
    font=("Microsoft JhengHei", 18) # 設定字型與字體大小
)

hint_label.pack(pady=10) # 將提示 Label 放入視窗


### 建立輸入框
user_entry = ctk.CTkEntry(
    app, # 指定 Entry 放在主視窗 app 裡面
    placeholder_text="例如：我今天很累", # 設定尚未輸入內容時的提示文字
    font=("Microsoft JhengHei", 18), # 設定字型與字體大小
    width=420, # 設定輸入框寬度
    height=45 # 設定輸入框高度
)

user_entry.pack(pady=15) # 將輸入框放入視窗


### 建立結果 Label
result_label = ctk.CTkLabel(
    app, # 指定 Label 放在主視窗 app 裡面
    text="等待宇宙訊號中...", # 設定預設顯示文字
    font=("Microsoft JhengHei", 24), # 設定字型與字體大小
    wraplength=520, # 文字超過 520 像素時自動換行
    justify="center" # 設定多行文字置中對齊
)

result_label.pack(pady=35) # 將結果 Label 放入視窗


### 通靈翻譯函式
def translate_by_spirit():
    user_text = user_entry.get() # 取得使用者輸入的文字

    if user_text == "":
        result_label.configure(
            text="宇宙收不到訊號，請先輸入一句話" # 沒有輸入內容時顯示提示訊息
        )

    else:
        reply = random.choice(psychic_replies) # 從 psychic_replies 隨機選擇一個回覆

        result_label.configure(
            text=reply # 將隨機選到的內容顯示在結果 Label
        )


### 建立通靈按鈕
translate_button = ctk.CTkButton(
    app, # 指定 Button 放在主視窗 app 裡面
    text="開始通靈", # 設定按鈕顯示的文字
    font=("Microsoft JhengHei", 22, "bold"), # 設定字型、字體大小與粗體
    width=220, # 設定按鈕寬度
    height=52, # 設定按鈕高度
    command=translate_by_spirit # 按下按鈕時執行 translate_by_spirit 函式
)

translate_button.pack(pady=10) # 將按鈕放入視窗


### 啟動視窗
app.mainloop() # 啟動事件迴圈，讓視窗持續顯示並等待使用者操作
```
