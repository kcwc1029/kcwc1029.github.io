from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv

from datetime import date

import os
import sqlite3


load_dotenv() # 載入 .env 檔案
BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token

DB_FILE = "./telegram_bot_datasets/expenses.db" # SQLite 資料庫檔案


# 初始化 SQLite 資料庫
def init_db() -> None:
    conn = sqlite3.connect(DB_FILE) # 連線資料庫

    # 建立 expenses 資料表
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit() # 儲存變更
    conn.close() # 關閉連線


# 新增支出資料
def add_expense(
    user_id: str,
    amount: float,
    category: str,
    note: str
) -> None:

    conn = sqlite3.connect(DB_FILE)

    conn.execute(
        """
        INSERT INTO expenses
        (user_id, amount, category, note, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            amount,
            category,
            note,
            str(date.today()) # 今日日期
        ),
    )

    conn.commit()
    conn.close()


# 查詢最近 10 筆支出
def list_expenses(user_id: str) -> list[tuple]:
    conn = sqlite3.connect(DB_FILE)

    rows = conn.execute(
        """
        SELECT id, amount, category, note, created_at
        FROM expenses
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 10
        """,
        (user_id,),
    ).fetchall()

    conn.close()

    return rows


# /help 使用說明
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "記帳 Bot 使用流程：\n\n"
        "1. 使用 /add 金額 分類 備註 新增一筆支出\n"
        "2. 使用 /list 查看最近 10 筆支出\n\n"
        "範例：\n"
        "/add 80 午餐 便當\n"
        "/add 35 交通 公車\n"
        "/list\n\n"
        "指令列表：\n"
        "/help：查看使用說明\n"
        "/add：新增記帳資料\n"
        "/list：查看最近 10 筆支出"
    )


# /add 新增記帳資料
async def add(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # 檢查參數數量
    if len(context.args) < 2:
        await update.message.reply_text(
            "用法：/add 金額 分類 備註"
        )
        return

    # 驗證金額格式
    try:
        amount = float(context.args[0])

    except ValueError:
        await update.message.reply_text(
            "金額必須是數字。"
        )
        return

    category = context.args[1] # 取得分類

    # 組合備註內容
    note = (
        " ".join(context.args[2:])
        if len(context.args) > 2
        else ""
    )

    # 新增資料到 SQLite
    add_expense(
        str(update.effective_user.id),
        amount,
        category,
        note
    )

    await update.message.reply_text(
        "已新增記帳資料。"
    )


# /list 查看最近 10 筆資料
async def list_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    rows = list_expenses(
        str(update.effective_user.id)
    )

    # 沒有資料時
    if not rows:
        await update.message.reply_text(
            "目前沒有記帳資料。"
        )
        return

    lines = ["最近 10 筆支出："]

    for row_id, amount, category, note, created_at in rows:

        line = (
            f"#{row_id} "
            f"{created_at} "
            f"{category} "
            f"${amount:.0f}"
        )

        # 有備註才顯示
        if note:
            line += f" | {note}"

        lines.append(line)

    await update.message.reply_text(
        "\n".join(lines)
    )


# 主程式
def main() -> None:

    init_db() # 啟動前初始化資料庫

    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_cmd))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()