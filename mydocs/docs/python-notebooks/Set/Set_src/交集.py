# 交集會返回包含兩個集合中共同元素的新集合。
math = {'Kevin', 'Peter', 'Eric'}
physics = {'Kevin', 'Eric', 'Tim'}
intersection_set = math.intersection(physics)
print(f"交集: {intersection_set}")

# 你也可以使用 & 運算符
intersection_set_op = math & physics
print(f"交集 (運算符): {intersection_set_op}")