import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("假登入系統")
app.geometry("420x380")


title_label = ctk.CTkLabel(
    app,
    text="會員登入系統",
    font=("Microsoft JhengHei", 30, "bold")
)
title_label.pack(pady=(40, 25))


username_entry = ctk.CTkEntry(
    app,
    placeholder_text="請輸入帳號",
    font=("Microsoft JhengHei", 18),
    width=260
)
username_entry.pack(pady=10)


password_entry = ctk.CTkEntry(
    app,
    placeholder_text="請輸入密碼",
    font=("Microsoft JhengHei", 18),
    width=260,
    show="*"
)
password_entry.pack(pady=10)


result_label = ctk.CTkLabel(
    app,
    text="",
    font=("Microsoft JhengHei", 20)
)
result_label.pack(pady=20)


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":
        result_label.configure(text="登入成功")
    else:
        result_label.configure(text="密碼錯誤")


login_button = ctk.CTkButton(
    app,
    text="登入",
    font=("Microsoft JhengHei", 20),
    width=180,
    command=login
)
login_button.pack(pady=10)


app.mainloop()