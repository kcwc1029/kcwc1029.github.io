### 範例：只列印偶數
for i in range(10):
    if i % 2 != 0:
        continue # 如果是奇數，跳過本次迴圈
    print(i)