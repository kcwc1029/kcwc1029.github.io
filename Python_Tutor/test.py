num = 0
while num < 10:
    num += 1
    if num % 2 != 0:
        continue # 如果是奇數，跳過本次迴圈
    print(num)