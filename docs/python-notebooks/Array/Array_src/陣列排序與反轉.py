# 1. reverse() 與 sort()：會改變原本的串列
scores = [70, 90, 80]
scores.reverse()
print(f"反轉後：{scores}") # [80, 90, 70]

scores.sort()
print(f"升序排序：{scores}") # [70, 80, 90]

# 2. sorted()：原本的串列保持不變
nums = [5, 2, 8]
new_nums = sorted(nums)
print(f"原串列不動：{nums}") # [5, 2, 8]
print(f"新生成的串列：{new_nums}") # [2, 5, 8]