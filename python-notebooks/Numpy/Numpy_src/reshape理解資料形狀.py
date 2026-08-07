import numpy as np

# 12 天的每日銷售杯數，先想成一條長長的收據。
daily_cups = np.array([12, 15, 18, 13, 20, 26, 24, 16, 19, 21, 18, 23])

print("原本形狀:", daily_cups.shape)
print(daily_cups)

# 改成 3 列 4 欄，可以想成 3 週，每週記 4 天。
weekly_table = daily_cups.reshape(3, 4)

print("改成 3x4 表格:")
print(weekly_table)
print("每週總杯數:", weekly_table.sum(axis=1))
print("每個觀察日的平均杯數:", weekly_table.mean(axis=0))

