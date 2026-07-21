animals = {'dog', 'cat', 'bird'}
animals.remove('cat')
print(animals)

# 如果嘗試刪除不存在的元素，程式會報錯
try:
    animals.remove('fish')
except KeyError:
    print("無法刪除 'fish'，因為它不存在。")