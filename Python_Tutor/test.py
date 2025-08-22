drinks = ('coffee', 'tea', 'wine')
enumerate_drinks = enumerate(drinks) # 使用 enumerate() 函數
print(enumerate_drinks)  # 打印 enumerate 物件，會顯示其記憶體位置

# 將 enumerate 物件轉為列表，方便查看內容
print(list(enumerate_drinks)) # 輸出: [(0, 'coffee'), (1, 'tea'), (2, 'wine')]
