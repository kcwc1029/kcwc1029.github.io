# 電影院等待時間計算
start_hour = 19
start_min = 30
now_hour = 18
now_min = 20

# 換成總分鐘計算
start_total = start_hour * 60 + start_min
now_total = now_hour * 60 + now_min

wait_time = start_total - now_total
print("還要等", wait_time, "分鐘")

# 買飲料花了 12 分鐘
wait_time_after_drink = wait_time - 12
print("買飲料回來後還要等", wait_time_after_drink, "分鐘")
