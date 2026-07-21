scores = [85, 92, 78, 95, 88]
for score in scores:
    if score > 90:
        print(f"找到第一個超過 90 分的成績：{score}")
        break # 找到後立即終止迴圈