### union() 或 |：聯集
# 聯集會返回包含兩個集合中所有元素的新集合。
math = {'Kevin', 'Peter'}
physics = {'Eric', 'Tim'}
union_set = math.union(physics)
print(f"聯集: {union_set}")

# 你也可以使用 | 運算符
union_set_op = math | physics
print(f"聯集 (運算符): {union_set_op}")