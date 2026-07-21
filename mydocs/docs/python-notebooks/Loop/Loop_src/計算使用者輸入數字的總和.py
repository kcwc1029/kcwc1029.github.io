total = 0
num = int(input("請輸入一個數字（輸入 0 結束）："))

while num != 0:
    total += num
    num = int(input("請輸入一個數字（輸入 0 結束）："))

print(f"總和為: {total}")