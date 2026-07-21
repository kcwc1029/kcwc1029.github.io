## 先前準備

請同學在自行搭配影片，完成基本建立telegram帳號

- [Telegram完整教學 參考影片](https://www.youtube.com/watch?v=lHLFy25k0tg&list=PLfDClTGqwsBDswM1IvDi_wkcf1Sp6pBkJ&index=1)
- [Telegram完整教學 中文化界面](https://www.pkstep.com/telegram-chinese/)

<div style="display: flex; gap: 10px;">
  <img src="https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/05/upgit_20260506_1778082645.png
" width="45%">
  <img src="https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/05/upgit_20260506_1778082668.png" width="75%">
</div>

## 向 BotFather 申請 Bot

Telegram 官方提供 `BotFather` 來管理你的 Bot。

1. 在 Telegram 搜尋 `BotFather`
2. 輸入 `/newbot`
3. 輸入 Bot 名稱
4. 輸入一個以 `bot` 結尾的使用者名稱
5. 取得一串 Token

這串 Token 很重要，等同於你的 Bot 密碼。

```
類似如下：
8803734531:AAE6xrmqql0YXACaeK3ekwpT6-buIatF8ds
```

![upgit_20260506_1778082753.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/05/upgit_20260506_1778082753.png)
![upgit_20260506_1778082762.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/05/upgit_20260506_1778082762.png)
![upgit_20260506_1778082769.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2026/05/upgit_20260506_1778082769.png)

## 安裝套件

```py
# 安裝套件
uv add python-telegram-bot[job-queue] python-dotenv requests -q
```

### [範例：echo_bot.py](./Telegram_Bot_src/echo_bot.py)

## `CommandHandler` 是什麼

```python
app.add_handler(CommandHandler("start", start))
```

這行的意思是：

- 當使用者輸入 `/start`
- 就呼叫 `start()` 函式

你可以把它理解成「事件與處理函式的對應表」。

### `update` 與 `context`

每個 handler 很常長這樣：

```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...
```

update代表這次事件的內容，常用資訊包括：

```python
update.effective_user.id
update.effective_user.first_name
update.effective_chat.id
update.message.text
```

context代表處理這次事件時可用的上下文資訊，常用內容包括：

```python
context.args
context.user_data
context.chat_data
context.bot
```

### [範例：功能選單：menu_bot.py](./Telegram_Bot_src/menu_bot.py)

## 訊息處理、文字解析與 filters

真實世界的 Bot 不會只有 `/start`、`/help`。很多時候使用者會直接輸入：

- 今天心情不好
- 幫我記一下買牛奶
- 我剛剛午餐花了 120

這時就要學會用 `MessageHandler` 處理一般文字訊息。

```python
# 常見寫法：
MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
# 意思：要是文字，但不能是指令
# 這很重要，否則 `/start` 這種訊息也可能被一般文字 handler 吃掉。
```

### [範例：文字分類--電商FAQ自動回覆Bot](./Telegram_Bot_src/電商FAQ自動回覆Bot.py)

### [範例：文字分類--美食推薦Bot](./Telegram_Bot_src/美食推薦Bot.py)

### 訊息處理順序要注意

如果你有多個 `MessageHandler`，順序就很重要。

例如：

```python
# 錯誤寫法
# 這樣很可能 `handle_text` 先吃掉了訊息，導致後面的 `handle_lunch` 沒機會執行。
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.Regex("^午餐"), handle_lunch))
```

建議：

- 先放更具體的 handler
- 再放通用 fallback handler

### [範例：文字分類--星座查詢bot](./Telegram_Bot_src/星座查詢bot.py)

## 為tg bot增加按鈕

按鈕的好處：

- 降低輸入錯誤
- 讓功能更容易被發現
- 很適合做選單型工具 Bot

可以分為Reply Keyboard 與 Inline Keyboard

### Reply Keyboard：像主選單

- Reply Keyboard 會直接出現在輸入框附近，像是常駐選單

| 很適合：                                      | 不太適合：                                                        |
| --------------------------------------------- | ----------------------------------------------------------------- |
| \- 主選單 <br>\- 常見分類 <br>\- 固定少量選項 | \- 每次內容都不同的資料 <br>\- 需要針對每筆資料生成不同按鈕的情境 |

- [範例：電商互動選單Bot--Reply Keyboard 版](./Telegram_Bot_src/電商互動選單Bot--Reply_Keyboard版.py)
- [範例：待辦清單按鈕Bot--Reply Keyboard 版](./Telegram_Bot_src/待辦清單按鈕Bot--Reply_Keyboard版.py)
- [提示詞]

### Inline Keyboard：像某一則訊息的操作按鈕

Inline Keyboard 是直接附在訊息下方的按鈕，常搭配 `callback_data`。

- [範例：Inline Keyboard--飲料點餐bot](./Telegram_Bot_src/飲料點餐bot.py)
- [提示詞]

## [JobQueue 提醒bot](./Telegram_Bot_src/最小提醒範例.py)

`JobQueue` 讓你可以安排某個函式在未來執行。例如：

- 10 分鐘後提醒我背單字
- 今晚 8 點提醒我交作業
- 每天早上 7 點提醒我起床

### [保存提醒資料](./Telegram_Bot_src/保存提醒資料.py)

如果只會排程，不會管理，就很難做出像樣的應用。常見需求：

- 列出目前有哪些提醒
- 取消某個提醒
- 讓同一個人可以建立多筆提醒

這時就會需要：

- `job.name`
- `context.job_queue.get_jobs_by_name()`
- 額外用字典或資料庫保存資訊

## 資料儲存

如果 Bot 一重開就失憶，那很多功能都只是展示用。

真正有價值的 Bot，通常要能記住：

- 待辦事項
- 記帳資料
- 使用者偏好
- 投票結果

經常搭配的儲存方式，簡單可以分為Json、資料庫(這邊以SQlite為例)。

### JSON 的特點

- 好懂
- 好教
- 適合小型資料
- [範例：以JSON實作電商商品管理Bot](./Telegram_Bot_src/以JSON實作電商商品管理Bot.py)
- [範例：以JSON實作台南旅遊景點推薦Bot](./Telegram_Bot_src/以JSON實作台南旅遊景點推薦Bot.py)
- [範例：以JSON實作打卡簽到Bot](./Telegram_Bot_src/以JSON實作打卡簽到Bot.py)

### SQLite 的特點

- 像真正資料庫
- 可以查詢、排序、篩選
- 比 JSON 更接近正式專案
- [範例：以SQLite實作記帳Bot](./telegram_bot_src/範例：以SQLite實作記帳Bot.py)
- [範例：以SQLite實作每日花費摘要bot](./telegram_bot_src/以SQLite實作每日花費摘要bot.py)

## API 串接與Telegra Bot

只靠本機資料，你能做的事情有限。

一旦會串 API，Bot 就能變成：

- 天氣查詢助手
- 匯率換算工具
- 課程資訊查詢器
- AI 助手

### API 可以怎麼理解

可以把 API 想成「另一個程式提供給你使用的資料入口」。

你的 Bot 發出請求：

```text
請給我台北天氣
```

對方伺服器回傳資料：

```json
{
    "temperature": 27,
    "condition": "Cloudy"
}
```

- [基本requests用法](./Telegram_Bot_src/基本requests用法.py)
- [範例：匯率換算Bot](./Telegram_Bot_src/匯率換算Bot.py)
- [範例：台股查詢與簡易技術分析Bot](./Telegram_Bot_src/台股查詢與簡易技術分析Bot.py)
- [範例：Gemini實作職涯導向輔導bot](./Telegram_Bot_src/Gemini實作職涯導向輔導bot.py)
- [範例：Gemini實作講梗bot](./Telegram_Bot_src/Gemini實作講梗bot.py)
- [範例：Gemini實作超商調酒推薦Bot](./Telegram_Bot_src/Gemini實作超商調酒推薦Bot.py)
