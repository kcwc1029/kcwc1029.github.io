### 範例：九九乘法表
for i in range(1, 10):
    for j in range(1, 10):
        result = i * j
        print(f"{i}*{j}={result}", end='\t') # 使用 `end='\t'` 讓輸出在同一行，並以 tab 分隔
    print() # 內層迴圈結束後，換行