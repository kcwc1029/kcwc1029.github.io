# 直接用大括號建立集合，元素重複時會自動移除
A = {'Python', 'Java', 'C', 'Python'}
print(A)

# 用 set() 函數將列表轉換為集合，同樣會移除重複元素
my_list = [1, 2, 3, 4, 3, 2, 1]
B = set(my_list)
print(B)

# 建立一個空集合，必須使用 set()
# 如果用 {} 建立，會變成一個空字典！
empty_set = set()
empty_dict = {}

print(f"empty_set 的型態是: {type(empty_set)}")
print(f"empty_dict 的型態是: {type(empty_dict)}")
