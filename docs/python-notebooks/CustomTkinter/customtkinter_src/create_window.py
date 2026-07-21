import customtkinter as ctk  # 業界慣例縮寫為 ctk

# 全域設定（建議放在建立視窗之前）
ctk.set_appearance_mode("dark")    # 外觀跟隨系統深淺色 System/ Dark/ Light

# 建立主視窗
window = ctk.CTk()
window.title("我的第一個視窗")  # 視窗標題
window.geometry("400x800")       # 寬 x 高（單位：像素）

# 啟動事件迴圈（一定要放在最後一行）
window.mainloop()

# 執行後你會看到一個空白視窗。試著把 `"400x300"` 改成 `"600x400"`，觀察視窗大小的變化
