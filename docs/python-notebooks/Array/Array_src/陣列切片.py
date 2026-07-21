warriors = ['Curry', 'Durant', 'Iguodala', 'Bell', 'Thompson']

# 取得索引 0 到 3 (不包含) 的元素
print(warriors[0:3]) # 輸出: ['Curry', 'Durant', 'Iguodala']

# 取得索引 2 到最後的元素
print(warriors[2:]) # 輸出: ['Iguodala', 'Bell', 'Thompson']

# 取得所有元素
print(warriors[:]) # 輸出: ['Curry', 'Durant', 'Iguodala', 'Bell', 'Thompson']

# 從頭到尾，每隔一個元素取一個
print(warriors[::2]) # 輸出: ['Curry', 'Iguodala', 'Thompson']

# 反轉串列
print(warriors[::-1]) # 輸出: ['Thompson', 'Bell', 'Iguodala', 'Durant', 'Curry']