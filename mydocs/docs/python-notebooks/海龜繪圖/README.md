# Python程式設計：海龜繪圖

海龜繪圖模組 (turtle) 是 Python 內建的，不需要額外安裝，可以直接使用 import turtle 來匯入。
:::danger
伽碩的學生，若電腦版IDE無法執行的話，就用線上網頁的方式完成
https://www.w3cschool.cn/tools/index?name=pythonturtle
:::
![image](https://hackmd.io/_uploads/SkLTcxTple.png)

海龜繪圖的核心是

- 位置與坐標：以 (0, 0) 為中心，向右為 x 軸正向，向上為 y 軸正向 。
- 畫筆屬性：可以設定畫筆的顏色、粗細、填充顏色等 。
- 方向與狀態：海龜有方向性，可以前進、後退、轉彎，畫筆可以放下或抬起

## 建立畫布與海龜

t = turtle.Pen() 可以建立一個海龜，並自動生成一個畫布。

| 指令             | 說明                   |
| ---------------- | ---------------------- |
| left(angle)      | 向左轉動指定角度       |
| right(angle)     | 向右轉動指定角度       |
| forward(number)  | 向前移動指定距離       |
| backward(number) | 向後移動指定距離       |
| penup()          | 抬起畫筆，移動時不繪圖 |
| pendown()        | 放下畫筆，開始繪圖     |
| goto(x, y)       | 移動到指定座標 (x, y)  |
| speed(n)         | 設定海龜速度，0 為最快 |

### 範例：畫正方形

```python=
import turtle
# import time

t = turtle.Turtle()
t.forward(100)
# time.sleep(2)
t.left(90)
t.forward(100)
# time.sleep(2)
t.left(90)
t.forward(100)
# time.sleep(2)
t.left(90)
t.forward(100)
t.left(90)
turtle.done() # 結束後停住
```

![image](https://hackmd.io/_uploads/By3H2e6pgl.png)

![image](https://hackmd.io/_uploads/S1JO2gapee.png)

### 補充：內角和與外角和

![image](https://hackmd.io/_uploads/r1VUy-apgx.png)

### 範例：畫五邊形

```python=
import turtle

t = turtle.Turtle()
sides = 5
for x in range(sides):
    t.forward(100)
    t.right(360/sides)
turtle.done()  # 保持視窗開啟
```

## 練習

### Problom. 請用海龜畫一個三角形

> Tips.
> 三角形有 3 個邊，所以我們的迴圈要讓海龜重複做 3 次動作。
> 畫三角形時，海龜每次往前走完，請讓牠「向左轉 120 度」（使用 t.left(120)）。

<!--
```python=
import turtle
t = turtle.Pen()

# 建立一個重複 3 次的迴圈
for x in range(3):
    t.forward(100)  # 海龜往前走 100 步
    t.left(120)     # 海龜向左轉 120 度

turtle.done()       # 畫完後讓視窗停住，不要馬上關閉
```
-->

### Problom. 請用海龜畫一個星星

> Tips.
> 經典的星星有 5 個尖角，所以我們要讓迴圈重複執行 5 次
> 畫星星的專屬祕方是「向右轉 144 度」（使用 t.right(144)），因為海龜需要轉比較大的彎才能畫出交叉的星星線條。

<!--
```python=
import turtle
t = turtle.Pen()

# 建立一個重複 5 次的迴圈
for i in range(5):
    t.forward(100)  # 海龜往前走 100 步
    t.right(144)    # 海龜專屬的星星魔法角度：向右轉 144 度

turtle.done()       # 畫完後讓視窗停住，不要馬上關閉
```
-->

### Problom. 繪製一個長方形

請建立一個海龜畫筆 t，繪製一個長方形。設定寬度變數 width 為 150，高度變數 height 為 80。海龜需要前進 width 步，轉彎 90 度，再前進 height 步，重複兩次完成。

<!--
```python=
import turtle
t = turtle.Pen()
width = 150
height = 80
for i in range(2):
    t.forward(width)
    t.left(90)
    t.forward(height)
    t.left(90)
turtle.done()
```
-->

### Problom. 繪製正六邊形

請使用迴圈繪製一個正六邊形。定義邊長變數 side 為 70。利用正多邊形外角公式（360/邊數），計算出海龜每次轉動的角度為 60 度。

<!--
```python=
import turtle
t = turtle.Pen()
side = 70
for i in range(6):
    t.forward(side)
    t.left(60)
turtle.done()
```
-->

### Problom. 繪製虛線段

請繪製一段由 5 個小線段組成的虛線。設定變數 step_length 為 20。海龜先放下畫筆前進 step_length，再抬起畫筆（penup）前進 10 步，重複 5 次。

<!--
```python=
import turtle
t = turtle.Pen()
step_length = 20
for i in range(5):
    t.pendown()
    t.forward(step_length)
    t.penup()
    t.forward(10)
turtle.done()
```
-->

## 控制畫筆顏色與線條粗細

| 指令                        | 解釋                                |
| --------------------------- | ----------------------------------- |
| pencolor(color_string)      | 選擇畫筆顏色，例如 "red" 或 "green" |
| pencolor(r, g, b)           | 使用 RGB 值設定顏色                 |
| pensize(size) / width(size) | 設定畫筆粗細                        |

```python=
import turtle
t = turtle.Pen()
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'purple', 'violet']
t.width(1)# 初始畫筆寬度設為 1
t.speed(10)    # 設定畫筆速度為 10（接近最快）
for x in range(41):
    t.pencolor(colors[x % 8])     # 循環選擇顏色（x % 8 讓顏色重複使用）
    t.circle(x * 3)               # 畫一個半徑為 x*3 的圓
    t.width(x * 1)             # 隨著迴圈增加畫筆寬度，讓線條漸粗
    t.left(90)                    # 每次畫完圓向左轉 90 度，產生旋轉效果
turtle.done()  # 保持視窗開啟直到手動關閉
```

![image](https://hackmd.io/_uploads/rJj-ZZppee.png)

### 範例：畫一個由藍色漸變到紅色的星型曲線

![image](https://hackmd.io/_uploads/HyAJjZTpgg.png =80%x)

要將顏色從藍色漸變成紅色，我們需要調整 t.color() 函式中的紅、綠、藍 (RGB) 分量

目前的顏色設定是 t.color(0.5, 1, colorValue)，其中：

- 紅色 (R) 固定為 0.5。
- 綠色 (G) 固定為 1 (最大值)。
- 藍色 (B) 由 colorValue 控制，從 1.0 遞減。

漸變控制：

- 為了從藍色到紅色，藍色分量需要從高值（例如 1.0）遞減到低值（例如 0.0）。
- 紅色分量需要從低值（例如 0.0）遞增到高值（例如 1.0）。
- 綠色分量可以保持固定在 0，或者給予少量值以調整色調。

```python=
import turtle

t = turtle.Pen()
t.pensize(5) # 設定畫筆的粗細為 5

# 設定迴圈次數與步長。
NUM_STEPS = 40  # 迴圈從 0 開始，執行 40 次。
COLOR_STEP = 1.0 / NUM_STEPS # 顏色步長，確保從 1.0 到 0.0 或 0.0 到 1.0 剛好在 40 步內完成。

for i in range(NUM_STEPS):
    blue_value = 1.0 - i * COLOR_STEP # 1. 藍色分量 (B): 從 1.0 遞減到 0.0
    red_value = i * COLOR_STEP # 2. 紅色分量 (R): 從 0.0 遞增到 1.0
    # 3. 綠色分量 (G) 固定為 0。

    t.color(red_value, 0, blue_value) # 設定畫筆顏色 (R, G, B)
    t.forward(100)
    t.left(100)

turtle.done()
```

### 範例：畫一個八邊形螺旋結構

![image](https://hackmd.io/_uploads/HyzZ2ba6ee.png)

<!--
```python=
import turtle

t = turtle.Pen()
colorsList = ['red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'purple', 'violet']
tWidth = 1      # 最初畫筆寬度
for x in range(1, 41):
    t.color(colorsList[x % 8])  # 選擇畫筆顏色
    t.forward(2 + x * 5)        # 每次移動距離
    t.right(45)                 # 每次旋轉角度
    tWidth += x * 0.05          # 每次畫筆寬度遞增
    t.width(tWidth)
```
-->

## (補充)填滿顏色

| 指令                    | 解釋                                  |
| ----------------------- | ------------------------------------- |
| begin_fill()            | 開始記錄繪製路徑以準備填色            |
| end_fill()              | 填滿路徑內的區域                      |
| fillcolor(color_string) | 設定填滿的顏色，例如 "red" 或 "green" |
| fillcolor(r, g, b)      | 使用 RGB 值設定填滿顏色               |

### 範例：繪製一個填滿顏色的五角形星星

![image](https://hackmd.io/_uploads/H1MyR-aple.png)

```python=
import turtle
t = turtle.Pen()
t.color('blue', 'yellow') # 設定畫筆和填色顏色
t.begin_fill() # 開始記錄繪製路徑以準備填色
for i in range(5):
    t.forward(100)
    t.right(144) # 720/5 (720是因為海龜在畫五角星時，需要繞著圖形的中心旋轉兩圈才能完成圖形。)
t.end_fill() # 填滿路徑內的區域
turtle.done()
```

## 繪製圓弧形

| 指令                        | 解釋                                   |
| --------------------------- | -------------------------------------- |
| circle(radius, extend=None) | radius 為半徑，extend 為繪製圓弧的角度 |

### 範例：畫四個圓

![image](https://hackmd.io/_uploads/SyHGxf66ll.png)

```python=
import turtle

t = turtle.Pen()
t.color('blue')

t.circle(50)
t.circle(-50)
t.forward(100)
t.circle(50)
t.circle(-50)
turtle.done()
```

### Problom. 繪製同心圓

請繪製 3 個同心圓。設定一個列表 radii 包含 [30, 60, 90]。海龜每次畫完一個圓後，需要移動位置以確保下一個圓的中心點一致，或者單純在原點畫出不同大小的圓。

<!--
```python=
import turtle
t = turtle.Pen()
radii = [30, 60, 90]
for r in radii:
    t.circle(r)
    # 調整起始點讓圓心對齊 (可選)
    t.penup()
    t.sety(t.ycor() - 30)
    t.pendown()
turtle.done()
```
-->

### Problom. 繪製正方形螺旋

請繪製一個逐漸層展開的螺旋。使用迴圈 range(1, 31)，每次移動的距離為 i \* 5，轉彎角度固定為 90 度。這會讓正方形看起來像螺旋一樣往外擴散。

<!--
```python=
import turtle
t = turtle.Pen()
for i in range(1, 31):
    t.forward(i * 5)
    t.left(90)
turtle.done()
```
-->

### Problom. 繪製十字架形狀

請利用海龜畫出一個「+」字形。設定每一條分支的長度 length 為 50。海龜從中心出發，前進後再後退回原點，轉 90 度後重複，共執行 4 次。

<!--
```python=
import turtle
t = turtle.Pen()
length = 50
for i in range(4):
    t.forward(length)
    t.backward(length)
    t.left(90)
turtle.done()
```
-->

### Problom. 繪製簡易小房子

請結合兩個圖形繪製一間房子。下方為一個邊長 100 的正方形（牆壁），上方為一個邊長 100 的三角形（屋頂）。提示：畫完正方形後，海龜需要移動到正方形的上方邊緣再開始畫三角形。

<!--
```python=
import turtle
t = turtle.Pen()

# 畫牆壁 (正方形)
for i in range(4):
    t.forward(100)
    t.left(90)

# 移動到屋頂起始位置
t.left(90)
t.forward(100)
t.right(90)

# 畫屋頂 (三角形)
for i in range(3):
    t.forward(100)
    t.left(120)

turtle.done()
```
-->

## (補充)螢幕與海龜控制

| 指令                         | 解釋               |
| ---------------------------- | ------------------ |
| screen.title(string)         | 設定視窗標題       |
| screen.bgcolor(color_string) | 設定背景顏色       |
| screen.setup(width, height)  | 設定視窗寬度和高度 |
| t.hideturtle()               | 隱藏海龜           |
| t.showturtle()               | 顯示海龜           |

### 範例：繪製一個藍色天空下的五角形星星

![image](https://hackmd.io/_uploads/H18IGf66ge.png)

```python=
import turtle
t = turtle.Pen()
turtle.Screen().bgcolor('blue') # 設定背景顏色為藍色
t.color('yellow')
t.begin_fill()
for i in range(5):
    t.forward(100)
    t.right(144)
t.end_fill()
turtle.done()
```

## 停止追蹤

```python=
turtle.tracer(0,0) # 可以停止動畫，一次顯現出來
```

### 範例：多邊形螺旋

利用turtle.tracer一次畫好

![image](https://hackmd.io/_uploads/BJDnzGp6xg.png)

```python=
import turtle

turtle.tracer(0,0)

t = turtle.Pen()

colorsList = ['red', 'green', 'blue']
for line in range(400):
    t.color(colorsList[line % 3])
    t.forward(line)
    # 三角形是120度，這邊故意少一度，讓他可以重疊去畫出來
    t.right(119)

turtle.done()
```

## 實作

- 星星：https://drive.google.com/file/d/1rGhv3OCfZ8we6uYBCLuIJrN04Aml7-9V/view?usp=sharing
- 蛇蛇追月亮：https://drive.google.com/file/d/19_MTdfuoRXafnnCSCtGWbDryhmTRMnux/view?usp=sharing
- 環狀樹枝：https://drive.google.com/file/d/1ido1cMyqHEfTQ27pWkOwsQR9L1Yv2G9T/view?usp=sharing
- 謝爾賓斯基三角形：https://drive.google.com/file/d/1Iq7vZThvVnanHdjmm-TjdevN84dh_Fxl/view?usp=sharing
- 科赫雪花：https://drive.google.com/file/d/1wSrRpcTM-RUusAQozJ3OUlVNR0dyJ3KQ/view?usp=sharing
- 小樹吃點點：https://drive.google.com/file/d/1_F1I3CHEuXZXvcP-I0Zr8yHiv5FatM0o/view?usp=sharing

## (補充)Reeborg's world：練習控制機器人走動

- https://reurl.cc/DOkEOO
  ![image](https://hackmd.io/_uploads/rkQt3HbS-l.png =60%x)

### Home 1/Home 2

```python=
move()
move()
```

### Home 3

```python=
move()
move()

turn_left()
move()
```

### Home 4

```python=
def turn_right():
    turn_left()
    turn_left()
    turn_left()

for _ in range(4): # 我們將重複以上所有步驟共4次。
    move()
    move()
    move()
    turn_left()
    move()
    move()
    move()
    if at_goal(): done()
    else:
        turn_right()
        move()
        turn_right()
```

### Around 1/Around 1 - Variable

```python=
# 這會將一個標記放置在機器人目前所在的位置，該標記稍後會使用。
put()
# 這樣就迫使機器人向前移動一格，以免干擾下面的程式碼。
move()
while True: # 我們在這裡開始一個無限迴圈。
    if object_here(): done()
    elif front_is_clear(): move()
    else: turn_left()
```

### Around 1 - Apple

```python=
move()
while True: # 我們在這裡開始一個無限迴圈。
    if object_here(): take()
    elif at_goal(): done()
    elif front_is_clear(): move()
    else: turn_left()
```

### Around 2

```python=
put()
move()
while True:
    if object_here(): done()
    elif right_is_clear():
        turn_left()
        turn_left()
        turn_left()
        move()
    elif wall_in_front(): turn_left()
    else: move()
```

### Around 3

```python=
put()
turn_left() # 這裡我們強制機器人先向左轉，然後再向前移動。
move()
while True:
    if object_here(): done()
    elif right_is_clear():
        turn_left()
        turn_left()
        turn_left()
        move()
    elif wall_in_front(): turn_left()
    else: move()
```

### Around 4

```python=
put()
turn_left() # 我們在這裡再加一個左轉。
turn_left()
move()
while True:
    if object_here(): done()
    elif right_is_clear():
        turn_left()
        turn_left()
        turn_left()
        move()
    elif wall_in_front(): turn_left()
    else: move()
```

### Center 1

```python=
step = 0

while front_is_clear():
    step+=1
    move()
turn_left()
turn_left()
for i in range(step//2):
    move()
put()
```

### Center 2

```python=
step = 0

while front_is_clear():
    step+=1
    move()
turn_left()
turn_left()
for i in range(step//2):
    move()

turn_left()

while front_is_clear():
    step+=1
    move()
turn_left()
turn_left()
for i in range(step//2):
    move()

put()
```

### Harvest 1/ Harvest 2

```python=
# 定義右轉，讓程式碼更好讀
def turn_right():
    for _ in range(3):
        turn_left()

# 定義「撿起這格所有東西並往前走」
def pick_and_move():
    while object_here():
        take()
    if front_is_clear():
        move()

# 定義「收割完一整行」
def harvest_row():
    while front_is_clear():
        pick_and_move()
    # 處理最後一格（因為 front_is_clear 停止時，機器人還站在最後一格）
    while object_here():
        take()

# 主程式邏輯
for _ in range(4): # 根據地圖範圍重複次數
    harvest_row()
    turn_left()
    move()
    turn_left()

    harvest_row()
    turn_right()
    if front_is_clear(): # 避免最後一行撞牆
        move()
        turn_right()
```

### Harvest 3

```python=
# 定義右轉，讓路徑轉向更直覺
def turn_right():
    for _ in range(3):
        turn_left()

# 定義「修正單一格子」：清空並補上一顆
def fix_spot():
    while object_here():
        take()
    put()

# 定義「處理一整行」：每行 6 格，移動 5 次
def fix_one_row():
    for _ in range(5):
        fix_spot()
        move()
    fix_spot()

# 1. 前往花園起點 (3, 3)
# 機器人從 (1, 1) 出發，面向東方
for _ in range(2):
    move()
turn_left()
for _ in range(2):
    move()
turn_right()

# 2. 以「之字形」方式處理 6 行花園
# 總共 6 行，我們每兩行為一組處理（一去一回）
for i in range(3):
    # 向東處理一行
    fix_one_row()
    turn_left()
    move()
    turn_left()

    # 向西處理下一行
    fix_one_row()

    # 判斷是否還有下一組要處理，避免在最後一行撞牆
    if i < 2:
        turn_right()
        move()
        turn_right()
```

### Hurdle 1/Hurdle 2/Hurdle 3/Hurdle 4

```python=
while not at_goal(): # while 迴圈將無限期地持續下去，直到達到目標為止。

    if right_is_clear(): # 這裡偵測是否需要右轉，如果需要，則右轉。
        for _ in range(3):
            turn_left()
        move()

    elif wall_in_front(): # 這裡檢測是否需要左轉，如果需要，則左轉。
        turn_left()

    else: # 如果不需要轉彎，這裡會讓機器人往前走。
        move()
```

<p style="text-align: center;">Copyright © 2026 Alen</p>
