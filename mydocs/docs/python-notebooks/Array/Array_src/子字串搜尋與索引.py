text = "hello world"

# 使用 find()
print(text.find("o"))      # 4
print(text.find("world"))  # 6
print(text.find("x"))      # -1（找不到）

# 使用 index()
print(text.index("o"))     # 4
print(text.index("world")) # 6
# print(text.index("x"))   # ValueError: substring not found

# 可選參數
print(text.find("o", 5))       # 7（從 index 5 開始找）
print(text.index("o", 5, 9))   # 7（只在 index 5 到 8 之間找）