# 初始資料：一連串的投票紀錄
votes = ['Apple', 'Banana', 'Apple', 'Cherry', 'Apple', 'Banana']

# 1. index()：找出 'Banana' 第一次出現在哪裡
first_banana = votes.index('Banana')
print(f"第一根香蕉在索引：{first_banana}") # 輸出: 1

# 2. count()：統計 'Apple' 總共得到幾票
apple_total = votes.count('Apple')
print(f"蘋果總票數：{apple_total}") # 輸出: 3