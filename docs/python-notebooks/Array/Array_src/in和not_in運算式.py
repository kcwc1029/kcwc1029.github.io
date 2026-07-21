fruits = ["apple", "banana", "cherry", "date"]

# 檢查 'cherry' 是否在串列中
if "cherry" in fruits:
    index = fruits.index("cherry")
    print(f"'cherry' 的索引是: {index}") # 輸出: 'cherry' 的索引是: 2

# 檢查 'grape' 是否不在串列中
if "grape" not in fruits:
    print("串列中沒有 'grape'") # 輸出: 串列中沒有 'grape'