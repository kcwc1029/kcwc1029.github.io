fruits = ['apple', 'banana', 'cherry', 'date', 'apple'] 
# sort
# sorted

# fruits.sort()

# 排序資料，可是我們不想動到元－本的資料
temp = sorted(fruits)
temp.pop()
temp.pop()
temp.append(10000)

print(temp)
print(fruits)


