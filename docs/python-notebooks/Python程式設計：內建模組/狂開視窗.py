import os
import random
import ctypes
import subprocess

# 1. 取得螢幕解析度
user32 = ctypes.windll.user32
sw = user32.GetSystemMetrics(0)
sh = user32.GetSystemMetrics(1)

# 2. 設定參數
filename = "launch_prank.bat"
colors = ["4f", "1f", "e0", "2f", "5f", "cf"]  # 背景色：紅、藍、黃、綠、紫、紅
num_windows = 10

# 3. 產生成千上萬（好啦 50 個）指令
with open(filename, "w", encoding="cp950") as f:
    f.write("@echo off\n")
    for i in range(num_windows):
        c = random.choice(colors)
        # 這裡利用 mode 指令縮小視窗，並用 start 的特性讓它們重疊
        # 雖然 bat 不能精確座標，但我們可以透過隨機的 mode 大小讓它們看起來很亂
        cols = random.randint(30, 230)
        lines = random.randint(10, 120)
        f.write(f'start "{i}" cmd /c "mode {cols},{lines} && color {c} && echo ERROR 0x000{i} && timeout 10"\n')
    
    # 10 秒後集體自殺
    f.write("timeout /t 10 >nul\n")
    f.write("taskkill /f /im cmd.exe\n")
    f.write(f'del "{filename}"\n') # 執行完後把這個暫存檔刪掉，毀屍滅跡

# 4. 執行生成的批次檔
subprocess.Popen(filename, shell=True)
print("噴射啟動！")