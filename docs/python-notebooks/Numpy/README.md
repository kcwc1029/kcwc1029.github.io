# NumPy

NumPy 是 Python 做「大量數字運算」時最常用的基礎套件。

如果用生活化的講法：

- Python list 像「一排置物籃」，每格可以放不同東西，例如數字、文字、甚至另一個 list。
- NumPy array 像「規格一致的倉庫貨架」，每格通常放同一種資料，所以電腦可以一次搬一整排、一次算一整批。

![](./Numpy_assets/介紹Numpy.png)

## 為什麼不是只用 list？

先看一個情境：全班 5 位學生的成績，每個人都加 5 分。

```py
# Python list 寫法：
scores = [78, 85, 92, 66, 88]

new_scores = []
for score in scores:
    new_scores.append(score + 5)

print(new_scores)
```

這段程式的意思很清楚：一個一個拿出來加 5 分。

但是如果有 5 萬筆、50 萬筆、500 萬筆資料呢？我們希望程式能像 Excel 一樣，一整欄直接運算。

```py
# NumPy 寫法：
import numpy as np

scores = np.array([78, 85, 92, 66, 88])
print(scores + 5)
```

> list 比較像日常收納箱，很彈性；NumPy array 比較像工廠輸送帶，比較規矩，但是大量處理時非常有效率。

- [範例：numpy陣列入門.py](./Numpy_src/numpy陣列入門.py)

## ndarray：NumPy 的主角

NumPy 最核心的資料結構叫 `ndarray`，可以先把它想成「多維度陣列」。

- [範例：ndarray做一維陣列](./Numpy_src/ndarray做一維陣列.py)
- [範例：ndarray做二維陣列](./Numpy_src/ndarray做二維陣列.py)

### 三個很重要的屬性

```py
print(scores.ndim)
print(scores.shape)
print(scores.dtype)
```

| 屬性    | 意思     | 白話解釋                   |
| ------- | -------- | -------------------------- |
| `ndim`  | 維度數   | 是一排、表格、還是更高維？ |
| `shape` | 形狀     | 有幾列幾欄？               |
| `dtype` | 資料型態 | 裡面放整數、小數、文字？   |

## 陣列運算：一次處理一整批

NumPy 最有感的地方，就是不用自己寫迴圈也能批次運算。

```py
import numpy as np

prices = np.array([45, 55, 65, 75])

print(prices + 10)
print(prices * 0.9)
print(prices >= 60)
```

### 統計函式：平均、最大、最小、總和

常用統計函式：

| 函式       | 意思         | 例子                   |
| ---------- | ------------ | ---------------------- |
| `sum()`    | 總和         | 總營收、總杯數         |
| `mean()`   | 平均         | 平均成績、平均等待時間 |
| `max()`    | 最大值       | 最高分、最高單筆消費   |
| `min()`    | 最小值       | 最低分、最短等待       |
| `argmax()` | 最大值的位置 | 找出第一名的位置       |
| `argmin()` | 最小值的位置 | 找出最低的位置         |

- [範例：成績統計.py](./Numpy_src/成績統計.py)

### axis 是什麼？

用表格想比較容易：

```py
scores = np.array([
    [82, 76, 90],
    [68, 88, 72],
    [95, 91, 84],
])
```

表格長這樣：

```text
        Python  SQL  Excel
學生 A     82   76    90
學生 B     68   88    72
學生 C     95   91    84
```

```py
scores.mean(axis=0)
# `axis=0`：往下算，每一欄算出一個結果 -> 直向統計。

scores.mean(axis=1)
# `axis=1`：往旁邊算，每一列算出一個結果 -> 橫向統計。
```

## 讀取 CSV：用真實一點的資料練習

- [資料集：飲料店一週訂單.csv](./Numpy_datasets/飲料店一週訂單.csv)
- [範例：飲料店讀取csv.py](./Numpy_src/飲料店讀取csv.py)

資料共有 72 筆，欄位如下：

| 欄位     | 說明                       |
| -------- | -------------------------- |
| 訂單編號 | 每筆訂單的代號             |
| 日期     | 訂單日期                   |
| 時段     | 早班、午班、晚班           |
| 門市     | 台北車站店、西門店、板橋店 |
| 飲品     | 商品名稱                   |
| 尺寸     | 中杯、大杯                 |
| 甜度     | 無糖、微糖、半糖、正常糖   |
| 冰塊     | 去冰、微冰、少冰、正常冰   |
| 數量     | 買幾杯                     |
| 單價     | 每杯價格                   |
| 等待分鐘 | 客人等多久                 |
| 評分     | 1 到 5 分                  |

## 布林篩選：像 Excel 篩選，但更可程式化

布林值就是 `True` / `False`。

```py
prices = np.array([45, 55, 65, 75])
print(prices >= 60)
# 結果：[False False  True  True]
```

- [範例：布林篩選找出高價與久等訂單.py](./Numpy_src/布林篩選找出高價與久等訂單.py)

## 多條件篩選

NumPy 的多條件要特別注意：

- Python 的 `and` 比較適合單一 True/False。
- NumPy array 裡面是一整排 True/False，要用 `&`。
- 每個條件要加括號，避免運算順序出錯。

```py
# 正確寫法
mask = (revenue >= 150) & (wait_minutes >= 10)

# 錯誤寫法
mask = revenue >= 150 and wait_minutes >= 10
```

常用符號：

| 符號 | 意思   |
| ---- | ------ | ---- |
| `&`  | 而且   |
| `    | `      | 或者 |
| `~`  | 反過來 |

## 排序與排名

- `sort()` 是把人照身高排好。
- `argsort()` 是告訴你排好後，每個人原本坐在哪個座位。

```py
# 如果只想排序數字：
scores = np.array([78, 85, 92, 66, 88])
print(np.sort(scores))
```

```py
# 如果想知道排序後「原本的位置」，要用 `argsort()`。
index = np.argsort(scores)
print(index)
```

- [範例：排序找熱賣飲品.py](./Numpy_src/排序找熱賣飲品.py)

## reshape：資料形狀改變，資料內容不變

`reshape` 可以改變陣列形狀。

```py
daily_cups = np.array([12, 15, 18, 13, 20, 26, 24, 16, 19, 21, 18, 23])
weekly_table = daily_cups.reshape(3, 4)
```

```text
# 原本是一條：
[12 15 18 13 20 26 24 16 19 21 18 23]

# 改成：
[[12 15 18 13]
 [20 26 24 16]
 [19 21 18 23]]
```

- [範例：reshape理解資料形狀.py](./Numpy_src/reshape理解資料形狀.py)

## 課堂練習

### [Problem. 建立等差陣列](./Numpy_exercise/建立等差陣列.py)

### [Problem. 建立英文字母陣列](./Numpy_exercise/建立英文字母陣列.py)

### [Problem. 建立全零陣列](./Numpy_exercise/建立全零陣列.py)

### [Problem. 建立全一陣列](./Numpy_exercise/建立全一陣列.py)

### [Problem. 產生亂數整數](./Numpy_exercise/產生亂數整數.py)

建立：

- 10個數字
- 範圍 1~5

### [Problem. 產生亂數小數](./Numpy_exercise/產生亂數小數.py)
