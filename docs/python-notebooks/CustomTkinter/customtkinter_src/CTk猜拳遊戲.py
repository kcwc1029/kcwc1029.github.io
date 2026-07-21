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
window.title("猜拳遊戲")
window.geometry("500x700")


# -----------------------------
# 下載圖片
# -----------------------------
image_url = "https://i.pinimg.com/736x/e9/70/42/e970420a723a7dc47f5342556a9d0661.jpg"

response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
image = image.resize((320, 320))

ctk_image = ctk.CTkImage(
    light_image=image,
    dark_image=image,
    size=(320, 320)
)


# -----------------------------
# 猜拳判斷函式
# -----------------------------
def play_game(user_choice):
    choices = ["石頭", "剪刀", "布"]
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "平手"
    elif user_choice == "石頭" and computer_choice == "剪刀":
        result = "你贏了"
    elif user_choice == "剪刀" and computer_choice == "布":
        result = "你贏了"
    elif user_choice == "布" and computer_choice == "石頭":
        result = "你贏了"
    else:
        result = "你輸了"

    result_label.configure(
        text=f"你出：{user_choice}\n電腦出：{computer_choice}\n{result}"
    )


# -----------------------------
# 標題 Label
# -----------------------------
title_label = ctk.CTkLabel(
    window,
    text="猜拳遊戲",
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
    text="請選擇你要出的拳",
    font=("Microsoft JhengHei", 20)
)
hint_label.pack(pady=10)


# -----------------------------
# 結果 Label
# -----------------------------
result_label = ctk.CTkLabel(
    window,
    text="你出：尚未選擇\n電腦出：尚未選擇\n等待開始",
    font=("Microsoft JhengHei", 22),
    justify="left"
)
result_label.pack(pady=20)


# -----------------------------
# 按鈕區塊
# -----------------------------
button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=10)

rock_button = ctk.CTkButton(
    button_frame,
    text="石頭",
    font=("Microsoft JhengHei", 18, "bold"),
    width=120,
    height=45,
    command=lambda: play_game("石頭")
)
rock_button.grid(row=0, column=0, padx=8)

scissors_button = ctk.CTkButton(
    button_frame,
    text="剪刀",
    font=("Microsoft JhengHei", 18, "bold"),
    width=120,
    height=45,
    command=lambda: play_game("剪刀")
)
scissors_button.grid(row=0, column=1, padx=8)

paper_button = ctk.CTkButton(
    button_frame,
    text="布",
    font=("Microsoft JhengHei", 18, "bold"),
    width=120,
    height=45,
    command=lambda: play_game("布")
)
paper_button.grid(row=0, column=2, padx=8)


# -----------------------------
# 啟動視窗
# -----------------------------
window.mainloop()