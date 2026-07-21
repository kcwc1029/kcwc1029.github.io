# 匯入 Telegram Bot 更新物件
from telegram import Update

# 匯入 Telegram Bot 功能模組
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# 匯入讀取 .env 工具
from dotenv import load_dotenv

# 匯入作業系統模組
import os


# 載入 .env 內容
load_dotenv()

# 取得 Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")


# 美食推薦資料
FOOD_RULES = {
    "拉麵": {
        "keywords": ["拉麵", "日式拉麵", "豚骨", "味噌拉麵"],
        "reply": "推薦你試試豚骨拉麵！如果喜歡濃一點，可以點叉燒加糖心蛋。"
    },
    "火鍋": {
        "keywords": ["火鍋", "鍋", "麻辣鍋", "石頭火鍋"],
        "reply": "推薦你吃麻辣鍋或石頭火鍋，適合想吃飽又想慢慢聊天的時候。"
    },
    "牛排": {
        "keywords": ["牛排", "排餐", "鐵板", "肋眼"],
        "reply": "推薦你吃肋眼牛排，油花比較香。如果想省預算，也可以選平價鐵板牛排。"
    },
    "雞排": {
        "keywords": ["雞排", "炸雞排", "鹽酥雞", "炸物"],
        "reply": "推薦你來份炸雞排！想罪惡一點可以加甜不辣、米血跟四季豆。"
    },
    "壽司": {
        "keywords": ["壽司", "生魚片", "握壽司", "炙燒"],
        "reply": "推薦你吃炙燒鮭魚壽司，香氣比較明顯，也很適合第一次嘗試。"
    },
    "義大利麵": {
        "keywords": ["義大利麵", "義麵", "奶油培根", "青醬"],
        "reply": "推薦你吃奶油培根義大利麵，想清爽一點可以選青醬雞肉。"
    },
    "披薩": {
        "keywords": ["披薩", "pizza", "起司", "夏威夷"],
        "reply": "推薦你點起司披薩或瑪格麗特披薩，簡單但不容易出錯。"
    },
    "便當": {
        "keywords": ["便當", "排骨飯", "雞腿飯", "控肉飯"],
        "reply": "推薦你吃雞腿便當，想吃傳統一點可以選控肉飯。"
    },
    "滷肉飯": {
        "keywords": ["滷肉飯", "肉燥飯", "魯肉飯"],
        "reply": "推薦你吃滷肉飯加半熟蛋，再配一碗貢丸湯，很台。"
    },
    "牛肉麵": {
        "keywords": ["牛肉麵", "紅燒牛肉麵", "清燉牛肉麵"],
        "reply": "推薦你吃紅燒牛肉麵，湯頭濃一點會比較有滿足感。"
    },
    "早午餐": {
        "keywords": ["早午餐", "早餐", "蛋餅", "漢堡", "吐司"],
        "reply": "推薦你吃蛋餅加鮮奶茶。如果想拍照，可以找有擺盤的早午餐店。"
    },
    "甜點": {
        "keywords": ["甜點", "蛋糕", "鬆餅", "布丁", "提拉米蘇"],
        "reply": "推薦你吃提拉米蘇或布丁，適合下午想放鬆一下。"
    },
    "飲料": {
        "keywords": ["飲料", "珍奶", "手搖", "奶茶", "果茶"],
        "reply": "推薦你喝珍珠奶茶。如果想清爽一點，可以點檸檬青茶。"
    },
    "咖啡": {
        "keywords": ["咖啡", "拿鐵", "美式", "卡布奇諾"],
        "reply": "推薦你喝拿鐵，想提神就選美式，想舒服一點就選熱拿鐵。"
    },
    "宵夜": {
        "keywords": ["宵夜", "半夜", "晚上餓", "消夜"],
        "reply": "推薦你吃鹽酥雞、滷味或鍋燒意麵。宵夜不要太理性，會失去快樂。"
    },
}


# /start 開始功能
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用美食推薦 Bot！\n\n"
        "你可以直接告訴我你想吃什麼。\n\n"
        "例如：\n"
        "我想吃拉麵\n"
        "今天想吃火鍋\n"
        "有沒有推薦的宵夜\n"
        "我想喝飲料\n\n"
        "也可以輸入 /food 查看目前支援的美食類型。"
    )


# /help 指令說明
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "美食推薦 Bot 指令說明\n\n"
        "/start - 開始使用 Bot\n"
        "/help - 查看指令說明\n"
        "/food - 查看可推薦的美食類型\n\n"
        "除了輸入指令之外，你也可以直接輸入一句話。\n\n"
        "例如：\n"
        "我想吃牛排\n"
        "今天想吃甜點\n"
        "晚上想吃宵夜"
    )


# /food 美食類型清單
async def food(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    food_list = "\n".join([f"{index + 1}. {name}" for index, name in enumerate(FOOD_RULES.keys())])

    await update.message.reply_text(
        "目前支援的美食類型如下：\n\n"
        f"{food_list}\n\n"
        "你可以直接輸入：\n"
        "我想吃拉麵\n"
        "我想吃火鍋\n"
        "今天想喝飲料"
    )


# 一般文字訊息處理
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 取得使用者輸入文字
    text = update.message.text.strip()

    # 預設找不到推薦
    reply = (
        "我目前還沒有找到適合的推薦。\n\n"
        "你可以試著輸入這些關鍵字：\n"
        "拉麵、火鍋、牛排、雞排、壽司、義大利麵、披薩、便當、滷肉飯、牛肉麵、早午餐、甜點、飲料、咖啡、宵夜\n\n"
        "也可以輸入 /food 查看完整類型。"
    )

    # 檢查使用者文字是否包含關鍵字
    for food_name, food_data in FOOD_RULES.items():
        keywords = food_data["keywords"]

        if any(keyword in text for keyword in keywords):
            reply = (
                f"你提到的是：{food_name}\n\n"
                f"{food_data['reply']}"
            )
            break

    # 回覆訊息
    await update.message.reply_text(reply)


# 主程式
def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/help指令")
    # 建立 Bot 應用程式
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 加入指令處理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("food", food))

    # 加入文字訊息處理器
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    # 啟動 Bot
    app.run_polling()


# 程式進入點
if __name__ == "__main__":
    main()