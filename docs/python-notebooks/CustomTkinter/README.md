## 為什麼要學 GUI？

你到目前為止寫的 Python 程式，執行結果都是出現在黑色的終端機視窗裡，對嗎？
這種方式稱為 命令列介面（CLI），對工程師來說很方便，但如果你想把程式分享給朋友、家人或同事，他們通常不知道怎麼開終端機、輸入指令。
這就是 圖形使用者介面（GUI） 存在的原因——讓程式有按鈕、輸入框、視窗，讓任何人都能輕鬆使用。

- [What's the difference between a GUI and a CLI?](https://www.youtube.com/watch?v=w9u0d4C95Zs)
- [一口气看懂GUI如何把电脑从“天书”变日常【GUI发展史｜仿生之旅】](https://www.youtube.com/watch?v=GdrEkSmItB4)
- [整理下Python常用的GUI模块](https://www.youtube.com/watch?v=w3GFf2ULdUo&t=1s)
- [範例：使用tkinter](./customtkinter_src/hello_tkinter.py)

## 使用理由

Python 有很多 GUI 套件，但這門課選擇 **CustomTkinter（簡稱 ctk）** 有幾個理由：

| 優點         | 說明                                     |
| ------------ | ---------------------------------------- |
| 安裝簡單     | 一行指令搞定                             |
| 現代外觀     | 內建深色模式、圓角、漸變動畫             |
| 學習曲線平緩 | 基於 Python 內建的 tkinter，網路資源豐富 |
| 適合製作工具 | 很多工程師拿來做自己用的小程式           |

- [CustomTkinter文件](https://customtkinter.tomschimansky.com/)

## 安裝套件

```bash
# !pip install customtkinter -q

uv add customtkinter -q
```

## [建立你的第一個視窗](./customtkinter_src/create_window.py)

在學第一個範例之前，有一個觀念很重要：

- 你以前寫的程式，都是「從上到下執行完就結束」。但 GUI 程式不一樣，它需要一直等著，等你點按鈕、輸入文字、關閉視窗，然後才對應地執行某段程式碼。
- 這種模式叫做「事件驅動」，程式靠 `mainloop()` 來維持這個「持續等待」的狀態。

### (補充)視窗的常用設定

```python
window.resizable(True, True)          # 允許使用者縮放（寬, 高）
window.maxsize(width=800, height=600) # 最大不超過這個尺寸
window.minsize(width=300, height=200) # 最小不得小於這個尺寸
```

## CTkLabel — 在視窗上顯示文字

Label（標籤）就像貼在視窗上的告示牌——它只負責顯示文字或圖片，使用者無法直接點它、編輯它。
每個你看到的 GUI 程式，標題、說明文字、狀態提示，幾乎都是用 Label 做的。

建立任何元件，格式都是一樣的：

```python=
元件 = ctk.CTk元件名稱(放在哪裡, 參數1=值, 參數2=值, ...)
元件.pack()  ← 一定要呼叫排版方法，元件才會顯示出來
```

### 常用參數

| 參數               | 用途                                                   | 範例值                       |
| ------------------ | ------------------------------------------------------ | ---------------------------- |
| `text`             | 要顯示的文字，`\n` 可換行                              | `"歡迎使用本系統"`           |
| `font`             | 字型：`(字體名稱, 大小)` 或 `(字體名稱, 大小, "bold")` | `("微軟正黑體", 18, "bold")` |
| `text_color`       | 文字顏色，色碼或顏色名稱                               | `"#3498DB"` 或 `"red"`       |
| `fg_color`         | 標籤背景色；不設定則預設**透明**                       | `"#2ECC71"`                  |
| `corner_radius`    | 圓角程度（需有背景色才看得出來）                       | `10`                         |
| `width` / `height` | 固定尺寸（像素）；不設定則自動縮放                     | `200`, `60`                  |

- [範例：建立一個 Ctk Label](./customtkinter_src/建立一個Ctk_Label.py)
- [範例：基礎文字與字型設定](./customtkinter_src/基礎文字與字型設定.py)

## CTkImage：在 GUI 中顯示圖片

CTkImage 是 CustomTkinter 專門用來處理圖片的元件。

```py
圖片變數 = ctk.CTkImage(
    light_image=Image.open("圖片路徑"),
    dark_image=Image.open("圖片路徑"),
    size=(寬度, 高度)
)

# 再搭配：
label = ctk.CTkLabel(app, image=圖片變數, text="")
label.pack()
```

- [範例：顯示圖片](./customtkinter_src/顯示圖片.py)

## CTkButton：按鈕

按鈕是 GUI 程式的靈魂。但按鈕本身不做任何事，它只負責在被點擊時通知某個函式去執行。

這個「通知某個函式」的動作，叫做綁定事件（Binding）。寫法是在 `command` 參數裡填入函式的名稱：

```python=
def 我的函式():
    print("按鈕被點到了！")

按鈕 = ctk.CTkButton(app, text="點我", command=我的函式)  # ← 填函式名稱，不加括號
```

### 常用參數

| 參數               | 用途                                       |
| ------------------ | ------------------------------------------ |
| `text`             | 按鈕上的文字                               |
| `command`          | 點擊時執行的函式（**不加括號**）           |
| `fg_color`         | 按鈕平時的顏色                             |
| `hover_color`      | 滑鼠移上去時的顏色（通常設深一點）         |
| `corner_radius`    | 圓角；設 `0` 為直角矩形                    |
| `state`            | `"normal"` 可點；`"disabled"` 變灰色且無效 |
| `width` / `height` | 按鈕尺寸                                   |

- [範例：CTk點擊計數器](./customtkinter_src/CTk點擊計數器.py)
- [範例：猜拳遊戲](./customtkinter_src/CTk猜拳遊戲.py)
- [範例：CTk一番賞抽獎機](./customtkinter_src/CTk一番賞抽獎機.py)

## CTkEntry：接收使用者輸入

Entry（輸入框）是讓使用者打字的地方。像登入頁面的帳號欄、搜尋框、表單的姓名欄，都是輸入框。

CTK 的 Entry 有個傳統 tkinter 沒有的功能：placeholder_text（提示文字），當輸入框是空的時會顯示灰色提示，一點擊就自動消失，不需要你另外寫程式碼。

```python=
# 輸入框裡的文字要靠 `.get()` 方法取出來：
user_input = my_entry.get()  # 取得目前輸入的字串
```

```python
# 清空輸入框
my_entry.delete(0, "end")  # 從第 0 個字元刪到最後
```

### 常用參數

| 參數 / 方法         | 用途                                 |
| ------------------- | ------------------------------------ |
| `placeholder_text`  | 提示文字，輸入框空時顯示，點擊後消失 |
| `show="*"`          | 密碼遮罩，輸入內容全部顯示為 `*`     |
| `width` / `height`  | 輸入框大小                           |
| `font`              | 輸入文字的字型                       |
| `.get()`            | 取得目前輸入的字串                   |
| `.delete(0, "end")` | 清空輸入框                           |

- [範例：假登入系統](./customtkinter_src/CTk假登入系統.py)
- [範例：通靈翻譯](./customtkinter_src/CTk通靈翻譯.py)

## CTkTextbox — 多行文字區域

Entry 只能輸入一行文字。當你需要讓使用者輸入或顯示**多行**文字（像記事本、日誌視窗、程式輸出區），就要用 CTkTextbox。

CTK 的 Textbox 與傳統 tkinter 最大的差別是內建捲軸，文字多了會自動出現捲軸，不用另外設定。

## CTkCheckBox（核取方塊）

每個 CheckBox 都綁定自己的 `BooleanVar`，勾選時變數為 `True`，取消為 `False`。

| 參數       | 說明                              |
| ---------- | --------------------------------- |
| `text`     | 勾選框旁邊的說明文字              |
| `variable` | 綁定 `ctk.BooleanVar()`，記錄狀態 |
| `command`  | 狀態改變時觸發的函式              |

## CTkRadioButton（單選按鈕）

同一組的所有 RadioButton 必須共用同一個變數（`variable`），但各自設定不同的 `value`。CTK 會自動處理互斥邏輯（選了 A，B 自動取消）。

```python
var = ctk.StringVar(value="預設值")

ctk.CTkRadioButton(app, text="選項 A", variable=var, value="A")
ctk.CTkRadioButton(app, text="選項 B", variable=var, value="B")

print(var.get())  # 取得目前選中的值："A" 或 "B"
```

## CTkOptionMenu（下拉選單）

當選項有很多個（超過 3–4 個），用 RadioButton 會佔太多空間，改用下拉選單更合適。

重要細節：綁定在 `command` 上的函式，CTK 會**自動把選中的字串作為參數傳入**：

```python
def on_select(choice):   # choice 是 CTK 自動傳入的選中值
    print(choice)
```

## 實作：

- [實作：番茄計時器](./customtkinter_projects/實作：番茄計時器.py)
- [實作：簡易計算機](./customtkinter_projects/實作：簡易計算機.py)
- [實作：圖片批量修改程式](./customtkinter_projects/實作：圖片批量修改程式.py)
- [實作：POS系統](./customtkinter_projects/實作：POS系統.py)
