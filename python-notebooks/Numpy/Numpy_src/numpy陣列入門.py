import numpy as np

# Python list 像一排置物籃，每格可以放不同東西。
scores_list = [78, 85, 92, 66, 88]

# NumPy array 像規格一致的倉庫貨架，適合大量數字一起計算。
scores = np.array(scores_list)

print("原本的 Python list:", scores_list)
print("NumPy array:", scores)
print("資料型態:", scores.dtype)
print("維度數量:", scores.ndim)
print("形狀 shape:", scores.shape)
print("全部加 5 分:", scores + 5)
print("是否及格:", scores >= 60)

# 原本的 Python list: [78, 85, 92, 66, 88]
# NumPy array: [78 85 92 66 88]
# 資料型態: int64
# 維度數量: 1
# 形狀 shape: (5,)
# 全部加 5 分: [83 90 97 71 93]
# 是否及格: [ True  True  True  True  True]