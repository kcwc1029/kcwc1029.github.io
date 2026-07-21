# 元組

如果串列（List）是你的「隨身背包」，可以隨時放入或取出東西；那麼元組（Tuple）就像是一個「密封保險箱」。一旦物品放入並上鎖，內容就固定不變了。

- 不可變性 (Immutability)：這是元組最重要的特徵。這讓元組在多執行緒環境下是安全的，也能作為字典（Dictionary）的鍵（Key）。
- 效能優勢：處理相同數量的資料時，元組的建立速度與讀取速度通常優於串列。

```python
# 語法
my_tuple = (1, 2, 'a', 'b')
# 只有一個元素的元組： 必須在元素後加上一個逗號，否則它會被視為普通變數。
# 正確： my_tuple = (1,)
# 錯誤： my_tuple = (1)
```

```python
# 定義一個元組
numbers = (1, 2, 3, 4, 5)

# 定義一個包含不同類型元素的元組
fruits = ("apple", "orange")

# 使用 type() 函數檢查變數類型
print(type(numbers))   # 輸出: <class 'tuple'>
print(type(fruits))    # 輸出: <class 'tuple'>
```

## 讀取元組(與list相同)

```python
fruits = (90, 85, 70, 60, 50)
print(fruits[0:2])  # 讀取第一個元素
print(fruits[:3])  # 讀取第二個元素
```

## 遍歷所有元組元素(與list相同)

可使用 for 迴圈來遍歷元組中的所有元素。

```python
keys = ('magic', 'xaab', 9099)
for key in keys:
  print(key)
```

## 元組切片 (Tuple Slices) (與list相同)

切片的語法與列表相似：`my_tuple[start:end]`

```python
fruits = ('apple', 'orange')
print(fruits[0])  # 讀取第一個元素
print(fruits[1])  # 讀取第二個元素
```

## 元組的功能

- 更安全的保護資料：當你確定某些資料永遠不應被更改時（例如，圖像的長寬、某個像素的顏色值），將其儲存在元組中可以防止意外修改，使程式碼更穩定、更安全。
- 儲存不可變的數據集。例如圓周率 pi、自然常數 e、黃金比例等科學常數。
  `constants = (3.14159, 2.71828, 1.61803)`
- 儲存大量座標數據：座標數據通常是不可變的，每個點可以儲存在一個元組中，然後將多個元組儲存在一個列表中。
  `coordinates_list = [(x, y) for x in range(100) for y in range(100)]
`
- 函數返回多個值：函數可以只用一個 return 語句返回多個值，此時 Python 會自動將這些值打包成一個元組。

```python
def get_min_max(numbers):
  return min(numbers), max(numbers)

min_value, max_value = get_min_max([1, 5, 9, 3, 7, 6])
print(f'Min: {min_value}, Max: {max_value}') # 輸出: Min: 1, Max: 9
```

## Unpacking

可以一次將元組的值賦予多個變數

```python
# 基礎拆箱
point = (10, 20)
x, y = point

# 進階：使用 * 收集剩餘元素
scores = (90, 85, 70, 60, 50)
high_score, *others, low_score = scores
print(high_score) # 90
print(others)     # [85, 70, 60] (會變成 list)
print(low_score)  # 50
```

## 元組的內建方法 (只有兩個！)

因為元組不可變，它沒有 `.append()` 或 `.sort()`。它只有兩個唯讀方法：

1.  **`count(value)`**：計算某個值出現的次數
2.  **`index(value)`**：尋找某個值第一次出現的索引位置。

```python
t = (1, 2, 3, 2, 4, 2)
print(t.count(2)) # 輸出: 3
print(t.index(3)) # 輸出: 2
```

## 修改元組內容會產生錯誤

這是tuple與list最大的不同點，tuple的內容是不可變的。嘗試修改、增加或刪除元組的元素都會導致錯誤。

```python
fruits = ('apple', 'orange')

# 嘗試修改元組的元素
fruits[0] = 'watermelon'
# TypeError: 'tuple' object does not support item assignment
```

雖然元組本身不能修改，但如果你確實需要修改內容，你可以變通地創建一個新的元組。

### 方法一： 將tuple轉換成list，修改列表，再將列表轉換回元組。

```python
original_tuple = (10, 20, 30)
temp_list = list(original_tuple) # 轉換成 list
temp_list[1] = 99 # 修改 list 中的元素
modified_tuple = tuple(temp_list) # 再轉回 tuple
```

### 方法二： 創建一個新的tuple，將舊tuple的元素和新元素合併。

```python
original_tuple = (1, 2, 3)
new_element = 4 # 新元素
new_tuple = original_tuple + (new_element,) # 合併成新的元組
print(new_tuple)
```

## 元組的不可變性「例外」

這是一個常見的面試題：如果元組裡面放了一個串列，會發生什麼事？

```python
# 元組本身不可變，但裡面的「物件」如果是可變的，其內容可以改
tricky_tuple = (1, 2, [3, 4])
tricky_tuple[2][0] = 99
print(tricky_tuple) # 輸出: (1, 2, [99, 4])
```

### [練習](./Tuplt_practices/元組練習題目.ipynb)

### [實作：基於gradio實作看不見全貌的二維網格地圖](./Tuple_src/基於gradio實作看不見全貌的二維網格地圖.py)

玩家在一個看不見全貌的二維網格地圖上探險。地圖上有固定的寶藏座標，也有絕對不能踩到的陷阱座標。玩家每次輸入上下左右移動，程式會計算並回報玩家與寶藏之間的距離，直到玩家準確走到寶藏位置為止。
