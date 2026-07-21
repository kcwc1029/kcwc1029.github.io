import customtkinter as ctk

app = ctk.CTk()
app.title("Label 範例 A")
app.geometry("350x200")

# 大標題
title_label = ctk.CTkLabel(app,
                            text="歡迎使用本系統",
                            font=("微軟正黑體", 24, "bold"),
                            text_color="#DBDDDF")
title_label.pack(pady=20)

# 說明文字
sub_label = ctk.CTkLabel(app,
                          text="請先登入帳號後繼續",
                          font=("微軟正黑體", 14),
                          text_color="gray")
sub_label.pack()

app.mainloop()