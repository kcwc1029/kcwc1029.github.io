import customtkinter as ctk

app = ctk.CTk() # 建立一個視窗的原件
app.geometry("300x200")

text = """我不知道我怎麼了我還在期待
能和你有未來

你怎麼忘了 你先說的愛我
抽屜裡放著 你送的音樂盒
是不是快樂 全被你帶走了
還是 習慣 孤獨 一個人的生活
"""
# 建立一個標籤元件
my_label = ctk.CTkLabel(app, text=text) # 建立一個標籤元件
my_label.pack()  # 放在 app（主視窗）裡面

app.mainloop()