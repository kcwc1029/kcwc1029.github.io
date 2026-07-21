
# 這是 for 迴圈最常見的用法：把一個列表（List）裡面的東西，依序拿出來處理。
students = ["小明", "小華", "小美", "阿強"]

print("開始點名：")
# "student" 只是一個暫時的代名詞，代表每次拿出來的那個人
for student in students:
    print(f"{student} 到了！")
    
print("點名結束。")