# 迴圈

## for迴圈

for 迴圈用於遍歷任何可迭代物件中的元素。在每次迴圈迭代中，它會將物件中的一個元素指派給一個變數，然後執行迴圈內的程式碼。
![upgit_20260420_1776667664.png|329x184](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/04/upgit_20260420_1776667664.png)

- [範例：for迴圈重複印出內容](./Loop_src/for_loop_basics.py)
- [範例：for迴圈重複印出i](./Loop_src/loop_variable_i.py)

### range()：產生一個整數序列

range() 函式是一種內建的可迭代物件，主要用於產生一個整數序列，通常用於 for 迴圈中以控制迴圈執行的次數。

```py
range(start, stop, step)
# 產生從 start 開始，
# 到 stop-1 結束，
# 每次以 step 為步長的整數序列。step 可以是正數（遞增）或負數（遞減）。
```

```py
for i in range(5):
    print(i)

for i in range(1, 5):
    print(i)

for i in range(1, 10, 2):
    print(i)

for i in range(10, 0, -2):
    print(i)
```

- [範例：倒數計時器](./Loop_src/倒數計時器.py)
- [範例：for迴圈用於陣列點名](./Loop_src/for迴圈用於陣列點名.py)
- [範例：撲滿存錢筒](./Loop_src/撲滿存錢筒.py)
- [範例：字母過濾](./Loop_src/字母過濾.py)

### 雙重for迴圈

- [範例：雙重for迴圈用於疊代兩個陣列](./Loop_src/雙重for迴圈用於疊代兩個陣列.py)
- [範例：雙重for迴圈 九九乘法表](./Loop_src/for_九九乘法表.py.py)

### [break：強制離開 for 迴圈](./Loop_src/break_強制離開for迴圈.py)

### [continue：for迴圈暫停但不終止](./Loop_src/continue_for迴圈暫停但不終止.py)

### [練習：for迴圈練習題目](./Loop_practices/for迴圈練習題目.ipynb)

## while迴圈

![upgit_20260420_1776668317.png|329x184](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/04/upgit_20260420_1776668317.png)

- [範例：使用者輸入q時終止](./Loop_src/使用者輸入q時終止.py)
- [範例：計算使用者輸入數字的總和，輸入 0 終止](./Loop_src/計算使用者輸入數字的總和.py)
- [範例：雙重while迴圈 九九乘法表](./Loop_src/while_九九乘法表.py.py)

## 實作

- [基於gradio實作while迴圈 猜數字遊戲](./Loop_src/基於gradio實作while迴圈_猜數字遊戲.py)
- [基於gradio實作while迴圈 ATM 提款機](./Loop_src/基於gradio實作while迴圈_ATM提款機.py)
- [基於gradio實作while迴圈 石頭剪刀布](./Loop_src/基於gradio實作while迴圈_石頭剪刀布.py)
- [基於gradio實作while迴圈 寵物餵食](./Loop_src/基於gradio實作while迴圈_寵物餵食.py)
- [基於gradio實作while迴圈 打字速度挑戰](./Loop_src/基於gradio實作while迴圈_打字速度挑戰.py)

用gradio for實作

- [基於gradio實作for迴圈 檔名批次改名](./Loop_src/基於gradio實作while迴圈_檔名批次改名.py)
- [基於gradio實作for迴圈 顏色產生](./Loop_src/基於gradio實作while迴圈_顏色產生.py)
