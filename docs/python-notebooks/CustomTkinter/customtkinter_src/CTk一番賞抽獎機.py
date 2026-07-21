import random
from io import BytesIO

import customtkinter as ctk
import requests
from PIL import Image


# -----------------------------
# 基本視窗設定
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("一番賞抽獎機")
window.geometry("520x720")


# -----------------------------
# 下載圖片
# -----------------------------
image_url = "https://i.pinimg.com/1200x/3e/7b/01/3e7b015f62fa554f250fdfde139cc290.jpg"

response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
image = image.resize((320, 320))

ctk_image = ctk.CTkImage(
    light_image=image,
    dark_image=image,
    size=(320, 320)
)


# -----------------------------
# 一番賞獎池
# -----------------------------
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


# -----------------------------
# 抽獎函式
# -----------------------------
def draw_prize():
    prize = random.choice(prizes)

    result_label.configure(
        text=f"抽獎結果\n\n恭喜抽中：\n{prize}"
    )


# -----------------------------
# 標題 Label
# -----------------------------
title_label = ctk.CTkLabel(
    window,
    text="一番賞抽獎機",
    font=("Microsoft JhengHei", 30, "bold")
)
title_label.pack(pady=(20, 10))


# -----------------------------
# 圖片 Label
# -----------------------------
image_label = ctk.CTkLabel(
    window,
    text="",
    image=ctk_image
)
image_label.pack(pady=10)


# -----------------------------
# 說明 Label
# -----------------------------
hint_label = ctk.CTkLabel(
    window,
    text="按下按鈕，看看你抽到哪一賞！",
    font=("Microsoft JhengHei", 20)
)
hint_label.pack(pady=10)


# -----------------------------
# 結果 Label
# -----------------------------
result_label = ctk.CTkLabel(
    window,
    text="尚未抽獎\n\n準備好就按下去！",
    font=("Microsoft JhengHei", 24, "bold"),
    justify="center"
)
result_label.pack(pady=25)


# -----------------------------
# 抽獎按鈕
# -----------------------------
draw_button = ctk.CTkButton(
    window,
    text="開始抽獎",
    font=("Microsoft JhengHei", 22, "bold"),
    width=220,
    height=55,
    command=draw_prize
)
draw_button.pack(pady=15)


# -----------------------------
# 啟動視窗
# -----------------------------
window.mainloop()