# 陣列

## 一維陣列

陣列是 Python 中一種最常見的資料型態，可以儲存多個不同型態的元素，例如數字、字串、布林值等。

### 定義串列

```py
# 定義一個數字串列
james = [23, 19, 22, 31, 18]

# 定義一個字串串列
fruits = ['apple', 'banana', 'orange']

# 混合型態的串列
leits = [3.5, 6.0, 8.5, 'leits']

# 建立一個空串列，之後可以再加入元素
new_list = []

arr = [1, 2, 3]
```

### [讀取陣列元素](./Array_src/讀取陣列元素.py)

透過索引 (index) 來取得串列中的特定元素。索引從 0 開始。

### [更改陣列元素的內容](./Array_src/更改陣列元素的內容.py)

```py
cars = ['Honda', 'Toyota', 'Ford']
print(cars[1])
cars[1] = 'Nissan' # 將索引 1 的元素改成 'Nissan'
print(cars) # 輸出: ['Honda', 'Nissan', 'Ford']
```

### [陣列切片](./Array_src/陣列切片.py)

### [陣列統計函式](./Array_src/陣列統計函式.py)

Python 提供了一些內建函式，可以對串列進行統計。

- max(x)：回傳串列中的最大值
- min(x)：回傳串列中的最小值
- sum(x)：回傳串列中所有元素的總和 (僅限數字串列)
- len(x)：回傳串列中元素的數量

### [增加陣列元素](./Array_src/增加陣列元素.py)

- `append(元素)`：固定加在串列的最後面。
- `insert(索引, 元素)`：可以插隊到指定的位置。

## 刪除元素

- `pop(索引)`：「取出」。會把元素拿出來給你用（預設最後一個）。
- `remove(內容)`：「指名」。直接刪除第一個符合該名稱的元素。
- `del`：「切除」。直接從記憶體中刪除指定索引或一段範圍。

```py
### pop用法
brands = ['Apple', 'Google', 'Meta', 'Amazon', 'Meta', 'Microsoft']
t = brands.pop() # 刪掉Microsoft
print(brands)
print(t)
```

```py
### remove用法
brands = ['Apple', 'Google', 'Meta', 'Amazon', 'Meta', 'Microsoft']
brands.remove('Google')
print(brands)
```

```py
### del用法
brands = ['Apple', 'Google', 'Meta', 'Amazon', 'Meta', 'Microsoft']
del brands
print(brands)
```

### [相加、倍增與空值判斷](./Array_src/相加、倍增與空值判斷.py)

### [陣列的搜尋與統計](./Array_src/陣列的搜尋與統計.py)

當串列資料變多時，我們需要快速找出某個東西的位置，或是算算看它出現了幾次。

- `index(內容)`：告訴你該元素第一次出現的索引（位置）。
- `count(內容)`：統計該元素在串列中總共出現了幾次。

### [陣列排序與反轉](./Array_src/陣列排序與反轉.py)

- `reverse()`：「原地反轉」。單純把順序倒過來，不看大小。
- `sort()`：「原地排序」。會直接打掉原本的順序，重新排列。
    - `reverse=True`：可以讓排序變成從大到小（降序）。
- `sorted()`：「產生副本」。原本的名單不動，另外給你一份排好的新名單。

### [一維陣列練習](./Array_practices/一維陣列練習.ipynb)

## 二維陣列

二維陣列可以想像成一個二維空間，就像一個表格或一張棋盤。它是由多個「串列」所組成的「串列」。也就是說，它的每個元素本身又是一個串列。

![upgit_20260421_1776782936.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/04/upgit_20260421_1776782936.png)

### [範例：成績系統](./Array_src/成績系統.py)

用一個陣列sc表示每個學生的\[姓名、國文、英文、數學、總分\]

| 姓名    | 國文 | 英文 | 數學 | 總分 |
| ------- | ---- | ---- | ---- | ---- |
| 建富1號 | 80   | 95   | 88   | 263  |
| 建富2號 | 98   | 97   | 96   | 291  |
| 建富3號 | 91   | 93   | 95   | 279  |
| 建富4號 | 92   | 94   | 90   | 276  |
| 建富5號 | 92   | 97   | 80   | 269  |

### [二維陣列練習](./Array_practices/二維陣列練習.ipynb)

## 字串陣列

![upgit_20260421_1776783144.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/04/upgit_20260421_1776783144.png)

```py
s = "apple"
print(s[0])
print(s[1])
print(s[-1])
```

### [字串切片](./Array_src/字串切片.py)

### [字串大小寫判斷與處理](./Array_src/字串大小寫判斷與處理.py)

### [字串切割與重組](./Array_src/字串切割與重組.py)

### [子字串搜尋與索引](./Array_src/子字串搜尋與索引.py)

- find()：回傳子字串第一次出現的位置，找不到時回傳-1
- index()：回傳子字串第一次出現的位置，找不到時回傳ValueError

### [in 和 not in 運算式](./Array_src/in和not_in運算式.py)

in 和 not in 運算式主要用於判斷一個元素（物件）是否屬於另一個複合型物件。
例如字串（string）、串列（list）、元組（tuple）或字典（dict）。

- obj in A：如果 obj 在物件 A 中，會回傳 True。
- obj not in A：如果 obj 不在物件 A 中，會回傳 True

### enumerate() 物件

- 在迴圈中同時取得「索引」和「值」。
- 把一個可迭代物件（list、tuple、string…）的元素，和它的索引值（位置）配對。
- 不是直接回傳 list，而是一個 enumerate 物件（一種特殊的迭代器）。

```py
obj = enumerate(iterable, start=0)
# iterable：你要處理的可迭代物件，例如一個串列或元組。
# start：可選參數，用來指定索引的起始值。如果沒有設定，預設會從 0 開始。
```

```py
# enumerate 物件的本質
fruits = ["apple", "banana", "cherry"]
e = enumerate(fruits)

print(e)
# <enumerate object at 0x...>   ← 這就是「enumerate 物件」
```

```py
# 一般迴圈
fruits = ["apple", "banana", "cherry"]

for i in range(len(fruits)):
    print(i, fruits[i])
```

```py
# 使用 enumerate()
fruits = ["apple", "banana", "cherry"]

for index, value in enumerate(fruits):
    print(index, value)
```

### [字串陣列練習](./Array_practices/字串陣列練習.ipynb)
