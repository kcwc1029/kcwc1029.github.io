### 撲滿存錢筒 (累加器 / Accumulation)
# 這是初學者一定要學會的經典技巧：在迴圈外面準備一個「空箱子（變數 = 0）」，然後用迴圈把東西一直加進去。
# 假設這是一週每天存下的零用錢
savings = [50, 100, 30, 20, 150, 0, 200]

# 準備一個變數當作撲滿，初始值為 0
total_money = 0

for money in savings:
    # 每次迴圈執行時，把當天的錢加到撲滿裡
    total_money = total_money + money  # 也可以簡寫成 total_money += money
    print(f"今天存了 {money} 元，撲滿裡有 {total_money} 元了。")

print(f"這禮拜總共存了：{total_money} 元！")