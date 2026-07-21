# 差集會返回在第一個集合中但不在第二個集合中的元素。
math = {'Kevin', 'Peter', 'Eric'}
physics = {'Kevin', 'Eric', 'Tim'}
difference_set = math.difference(physics)
print(f"差集 (math - physics): {difference_set}")

# 你也可以使用 - 運算符
difference_set_op = math - physics
print(f"差集 (運算符): {difference_set_op}")