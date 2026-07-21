"""製作 tg bot，使用 Reply Keyboard 管理待辦事項"""

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from dotenv import load_dotenv
import os


load_dotenv() # 載入 .env 檔案
BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token


# 建立待辦主選單
def build_todo_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        ["新增待辦", "查看待辦"],
        ["完成待辦", "清空待辦"],
        ["使用說明", "關閉選單"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True, # 自動調整鍵盤大小
        one_time_keyboard=False # 保持選單顯示
    )


# /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用 Todo Reply Keyboard Bot。\n\n"
        "你可以輸入 /todo_reply_bot 開啟待辦選單，\n"
        "或輸入 /help 查看使用說明。"
    )


# /todo_reply_bot 指令
async def todo_reply_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "請從下方選單選擇待辦功能：",
        reply_markup=build_todo_keyboard()
    )


# /help 指令
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "使用說明：\n\n"
        "/start - 開始使用 Bot\n"
        "/todo_reply_bot - 開啟待辦選單\n"
        "/close - 關閉待辦選單\n\n"
        "新增待辦：先點「新增待辦」，再輸入待辦內容。\n"
        "查看待辦：顯示目前所有待辦事項。\n"
        "完成待辦：先點「完成待辦」，再輸入待辦編號。\n"
        "清空待辦：刪除所有待辦事項。"
    )


# /close 指令
async def close_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "已關閉待辦選單。",
        reply_markup=ReplyKeyboardRemove()
    )


# 取得使用者待辦清單
def get_user_todos(context: ContextTypes.DEFAULT_TYPE) -> list:
    if "todos" not in context.user_data:
        context.user_data["todos"] = []

    return context.user_data["todos"]


# 顯示待辦清單文字
def format_todos(todos: list) -> str:
    if not todos:
        return "目前沒有待辦事項。"

    todo_text = "目前待辦事項：\n\n"

    for index, todo in enumerate(todos, start=1):
        todo_text += f"{index}. {todo}\n"

    return todo_text


# 處理 Reply Keyboard 傳來的文字
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip() # 去除前後空白
    todos = get_user_todos(context) # 取得待辦清單

    if text == "新增待辦":
        context.user_data["mode"] = "add" # 切換成新增模式
        await update.message.reply_text("請輸入要新增的待辦內容：")
        return

    elif text == "查看待辦":
        await update.message.reply_text(format_todos(todos))
        return

    elif text == "完成待辦":
        context.user_data["mode"] = "done" # 切換成完成模式
        await update.message.reply_text(
            format_todos(todos) + "\n請輸入要完成的待辦編號："
        )
        return

    elif text == "清空待辦":
        todos.clear() # 清空待辦清單
        await update.message.reply_text("已清空所有待辦事項。")
        return

    elif text == "使用說明":
        await help_command(update, context)
        return

    elif text == "關閉選單":
        await close_menu(update, context)
        return

    mode = context.user_data.get("mode") # 取得目前操作模式

    if mode == "add":
        todos.append(text) # 加入待辦內容
        context.user_data["mode"] = None # 清除操作模式
        await update.message.reply_text(f"已新增待辦：{text}")
        return

    elif mode == "done":
        if not text.isdigit():
            await update.message.reply_text("請輸入正確的待辦編號。")
            return

        todo_index = int(text) - 1 # 轉成清單索引

        if todo_index < 0 or todo_index >= len(todos):
            await update.message.reply_text("找不到這個待辦編號。")
            return

        done_todo = todos.pop(todo_index) # 移除完成項目
        context.user_data["mode"] = None # 清除操作模式
        await update.message.reply_text(f"已完成待辦：{done_todo}")
        return

    await update.message.reply_text(
        "目前沒有這個選項。\n\n"
        "請點選下方選單，或輸入 /todo_reply_bot 開啟選單。"
    )


# 主程式
def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/help指令跳出選單")

    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("start", start)) # 註冊 /start
    app.add_handler(CommandHandler("help", help_command)) # 註冊 /help
    app.add_handler(CommandHandler("todo_reply_bot", todo_reply_bot)) # 註冊 /todo_reply_bot
    app.add_handler(CommandHandler("close", close_menu)) # 註冊 /close

    # 接收一般文字，不處理指令
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()