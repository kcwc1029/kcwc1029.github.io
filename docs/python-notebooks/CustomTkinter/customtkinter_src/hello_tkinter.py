import tkinter as tk


# 按下按鈕後執行
def say_hello():
    label.config(text="哈囉！你按下按鈕了")


# 建立主視窗
window = tk.Tk()

# 視窗標題
window.title("Tkinter 第一個程式")

# 視窗大小
window.geometry("400x200")


# 文字標籤
label = tk.Label(
    window,
    text="歡迎來到 Tkinter",
    font=("Arial", 20)
)

label.pack(pady=30)


# 按鈕
button = tk.Button(
    window,
    text="點我",
    font=("Arial", 16),
    command=say_hello
)

button.pack()


# 啟動視窗
window.mainloop()