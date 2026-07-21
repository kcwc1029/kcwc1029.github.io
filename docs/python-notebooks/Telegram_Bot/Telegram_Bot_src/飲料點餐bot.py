"""製作 tg bot，使用 Inline Keyboard 製作飲料點餐 Bot"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from dotenv import load_dotenv
import os


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


# 飲料資料
DRINK_MENU = {
    "green_tea": {
        "name": "綠茶",
        "items": {
            "jasmine_green": {"name": "茉莉綠", "M": 25, "L": 30},
            "four_seasons": {"name": "四季春", "M": 30, "L": 35},
            "jade_green": {"name": "玉露綠", "M": 35, "L": 40},
        },
    },
    "black_tea": {
        "name": "紅茶",
        "items": {
            "assam_black": {"name": "阿薩姆紅茶", "M": 25, "L": 30},
            "earl_grey": {"name": "伯爵紅茶", "M": 30, "L": 35},
            "honey_black": {"name": "蜂蜜紅茶", "M": 35, "L": 40},
        },
    },
    "oolong_tea": {
        "name": "青茶",
        "items": {
            "qing_tea": {"name": "高山青茶", "M": 30, "L": 35},
            "osmanthus_oolong": {"name": "桂花青茶", "M": 35, "L": 40},
            "milk_oolong": {"name": "奶香青茶", "M": 40, "L": 45},
        },
    },
}


# 建立茶類選單
def build_category_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🟢 綠茶", callback_data="category:green_tea"),
            InlineKeyboardButton("🔴 紅茶", callback_data="category:black_tea"),
        ],
        [
            InlineKeyboardButton("🟡 青茶", callback_data="category:oolong_tea"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# 建立飲料品項選單
def build_drink_keyboard(category_key: str) -> InlineKeyboardMarkup:
    category = DRINK_MENU[category_key]
    keyboard = []

    for drink_key, drink_info in category["items"].items():
        keyboard.append([
            InlineKeyboardButton(
                drink_info["name"],
                callback_data=f"drink:{category_key}:{drink_key}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅️ 回到茶類選單", callback_data="back:category")
    ])

    return InlineKeyboardMarkup(keyboard)


# 建立尺寸選單
def build_size_keyboard(category_key: str, drink_key: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("M 杯", callback_data=f"size:{category_key}:{drink_key}:M"),
            InlineKeyboardButton("L 杯", callback_data=f"size:{category_key}:{drink_key}:L"),
        ],
        [
            InlineKeyboardButton("⬅️ 回到飲料選單", callback_data=f"back:drink:{category_key}")
        ],
        [
            InlineKeyboardButton("🏠 回到茶類選單", callback_data="back:category")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用飲料點餐 Bot。\n\n"
        "請輸入 /drink 開始點飲料。"
    )


# /drink 指令
async def drink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "請選擇茶類：",
        reply_markup=build_category_keyboard()
    )


# /help 指令
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "使用說明：\n\n"
        "/start - 開始使用 Bot\n"
        "/drink - 開始點飲料\n"
        "/help - 查看使用說明\n\n"
        "這個範例會使用 Inline Keyboard。\n"
        "按鈕會直接附在訊息下方，點擊後透過 callback_data 判斷使用者選了什麼。"
    )


# 處理 Inline Keyboard 按鈕點擊
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    # 告訴 Telegram：我已經收到這次按鈕點擊
    await query.answer()

    data = query.data

    # 點選茶類
    if data.startswith("category:"):
        category_key = data.split(":")[1]
        category_name = DRINK_MENU[category_key]["name"]

        await query.edit_message_text(
            text=f"你選擇了：{category_name}\n\n請選擇飲料品項：",
            reply_markup=build_drink_keyboard(category_key)
        )
        return

    # 點選飲料
    if data.startswith("drink:"):
        parts = data.split(":")
        category_key = parts[1]
        drink_key = parts[2]

        drink_info = DRINK_MENU[category_key]["items"][drink_key]

        await query.edit_message_text(
            text=(
                f"你選擇了：{drink_info['name']}\n\n"
                f"M 杯：{drink_info['M']} 元\n"
                f"L 杯：{drink_info['L']} 元\n\n"
                "請選擇尺寸："
            ),
            reply_markup=build_size_keyboard(category_key, drink_key)
        )
        return

    # 點選尺寸
    if data.startswith("size:"):
        parts = data.split(":")
        category_key = parts[1]
        drink_key = parts[2]
        size = parts[3]

        drink_info = DRINK_MENU[category_key]["items"][drink_key]
        price = drink_info[size]

        await query.edit_message_text(
            text=(
                "✅ 點餐完成\n\n"
                f"飲料：{drink_info['name']}\n"
                f"尺寸：{size} 杯\n"
                f"價格：{price} 元\n\n"
                "想再點一杯，可以輸入 /drink。"
            )
        )
        return

    # 回到茶類選單
    if data == "back:category":
        await query.edit_message_text(
            text="請選擇茶類：",
            reply_markup=build_category_keyboard()
        )
        return

    # 回到某個茶類的飲料選單
    if data.startswith("back:drink:"):
        category_key = data.split(":")[2]
        category_name = DRINK_MENU[category_key]["name"]

        await query.edit_message_text(
            text=f"你選擇了：{category_name}\n\n請選擇飲料品項：",
            reply_markup=build_drink_keyboard(category_key)
        )
        return


# 主程式
def main() -> None:
    print("飲料點餐 Inline Keyboard Bot 啟用中")
    print("可以輸入 /help")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("drink", drink))
    app.add_handler(CommandHandler("help", help_command))

    # 接收 Inline Keyboard 的 callback_data
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()


if __name__ == "__main__":
    main()