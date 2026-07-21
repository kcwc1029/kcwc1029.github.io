import customtkinter as ctk
import requests

from io import BytesIO
from PIL import Image


# -----------------------------
# 基本視窗設定
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("做功德")
window.geometry("500x650")


# -----------------------------
# 計數變數
# -----------------------------
count = 15


# -----------------------------
# 按鈕事件函式
# -----------------------------
def add_count():
    global count
    count += 1
    count_label.configure(text=f"目前點擊次數：{count}")


# -----------------------------
# 下載圖片
# -----------------------------
image_url = "https://i.pinimg.com/736x/c4/88/ff/c488ff6a0062b80ddfdcd404c3f282fa.jpg"

response = requests.get(image_url)

image = Image.open(BytesIO(response.content))

# 調整圖片大小
image = image.resize((300, 300))

# 轉成 CTkImage
ctk_image = ctk.CTkImage(
    light_image=image,
    dark_image=image,
    size=(300, 300)
)


# -----------------------------
# 標題 Label
# -----------------------------
title_label = ctk.CTkLabel(
    window,
    text="點擊計數器",
    font=("Microsoft JhengHei", 28, "bold")
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
# 顯示次數 Label
# -----------------------------
count_label = ctk.CTkLabel(
    window,
    text=f"目前點擊次數：{count}",
    font=("Microsoft JhengHei", 22)
)
count_label.pack(pady=20)


# -----------------------------
# +1 按鈕
# -----------------------------
add_button = ctk.CTkButton(
    window,
    text="按我 +1",
    font=("Microsoft JhengHei", 20, "bold"),
    width=180,
    height=50,
    command=add_count
)
add_button.pack(pady=20)


# -----------------------------
# 啟動視窗
# -----------------------------
window.mainloop()