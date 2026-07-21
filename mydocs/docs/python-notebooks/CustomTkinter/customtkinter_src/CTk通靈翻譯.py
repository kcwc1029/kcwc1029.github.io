import random
from io import BytesIO

import customtkinter as ctk
import requests

from PIL import Image


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("社處翻譯機")
app.geometry("620x760")


# -----------------------------
# 下載圖片
# -----------------------------
image_url = "https://i.pinimg.com/1200x/28/23/89/282389c136060ed941985b879cc992ab.jpg"

response = requests.get(image_url)

image = Image.open(BytesIO(response.content))

# 調整大小
image = image.resize((320, 320))

# 轉成 CTkImage
ctk_image = ctk.CTkImage(
    light_image=image,
    dark_image=image,
    size=(320, 320)
)


psychic_replies = [
    "宇宙看完直接回：建議你今天就去死一死比較快",
    "祖先集體搖頭：這輩子已經沒救了，投胎申請已通過",
    "靈魂翻譯：我不是累，我是後悔來當人",
    "水晶球碎裂顯示：你的人生劇本是悲劇，導演已跑路",
    "神明直接把你拉黑：這孩子救不活了，別浪費我時間",
    "通靈結果：你現在最適合的狀態是『腦死但還在呼吸』",
    "你這句話的真實意思是：我想從這該死的人生登出",
    "宇宙冷笑：又來了，這廢物又在裝死",
    "你的氣場現在像一具還在滑手機的浮屍",
    "前世查詢：你上輩子是隻被車輾過的流浪狗，這輩子還是",
    "靈界一致判定：這人已經臭了，可以直接火化",
    "系統提示：你的靈魂剩餘壽命 -7 天，建議直接關機",
    "塔羅牌全抽到死神：恭喜，你的人生已經到底了",
    "祖先傳話：別努力了，反正你也成不了氣候",
    "通靈失敗，因為你的未來一片漆黑什麼都看不到",
    "你現在的能量值：剛好夠去跳樓的高度",
    "神明嘆氣：這孩子每天都在求死，但又不敢真的死",
    "靈魂目前狀態：已黑化，預計三小時後社死",
    "翻譯完成：我好想死，但還要假裝我很愛生活",
    "宇宙直接吐槽：你這種人活著就是在汙染空氣",
    "磁場顯示：你現在只差一瓶安眠藥就能解脫",
    "你的心聲：誰再叫我加油，我就先送他下去陪我",
    "通靈機嚴正警告：再繼續硬撐會直接原地暴斃",
    "你的人生目前像一場永遠關不掉的惡夢",
    "靈界笑死：這廢物還在假裝自己有未來",
    "翻譯結果：我沒有抑鬱，我只是徹底看開想死了",
    "宇宙回覆：已收到你的求死申請，正在審核中",
    "你現在像一隻被拔光羽毛還在唱歌的雞",
    "神明表示：這題我不會，建議你直接重開人生",
    "最後通牒：再不擺爛你就真的要原地去世了"
]


# -----------------------------
# 標題
# -----------------------------
title_label = ctk.CTkLabel(
    app,
    text="社處翻譯機",
    font=("Microsoft JhengHei", 34, "bold")
)
title_label.pack(pady=(25, 10))


# -----------------------------
# 圖片
# -----------------------------
image_label = ctk.CTkLabel(
    app,
    text="",
    image=ctk_image
)
image_label.pack(pady=10)


# -----------------------------
# 提示文字
# -----------------------------
hint_label = ctk.CTkLabel(
    app,
    text="輸入一句正常話，讓程式幫你亂翻",
    font=("Microsoft JhengHei", 18)
)
hint_label.pack(pady=10)


# -----------------------------
# 輸入框
# -----------------------------
user_entry = ctk.CTkEntry(
    app,
    placeholder_text="例如：我今天很累",
    font=("Microsoft JhengHei", 18),
    width=420,
    height=45
)
user_entry.pack(pady=15)


# -----------------------------
# 結果 Label
# -----------------------------
result_label = ctk.CTkLabel(
    app,
    text="等待宇宙訊號中...",
    font=("Microsoft JhengHei", 24),
    wraplength=520,
    justify="center"
)
result_label.pack(pady=35)


# -----------------------------
# 通靈函式
# -----------------------------
def translate_by_spirit():

    user_text = user_entry.get()

    if user_text == "":
        result_label.configure(
            text="宇宙收不到訊號，請先輸入一句話"
        )

    else:
        reply = random.choice(psychic_replies)

        result_label.configure(
            text=reply
        )


# -----------------------------
# 按鈕
# -----------------------------
translate_button = ctk.CTkButton(
    app,
    text="開始通靈",
    font=("Microsoft JhengHei", 22, "bold"),
    width=220,
    height=52,
    command=translate_by_spirit
)
translate_button.pack(pady=10)


app.mainloop()