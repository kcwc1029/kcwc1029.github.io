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

DB_FILE = "./telegram_bot_datasets/daily_summary.db" # SQLite 資料庫檔案


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
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit() # 儲存變更
    conn.close() # 關閉連線


# 新增今日支出
def add_expense(
    user_id: str,
    amount: float,
    category: str
) -> None:

    conn = sqlite3.connect(DB_FILE)

    conn.execute(
        """
        INSERT INTO expenses
        (user_id, amount, category, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            amount,
            category,
            str(date.today()) # 今日日期
        ),
    )

    conn.commit()
    conn.close()


# 查詢今日摘要
def summary_today(
    user_id: str
) -> tuple[float, list[tuple]]:

    today = str(date.today()) # 取得今天日期

    conn = sqlite3.connect(DB_FILE)

    # 查詢今日總支出
    total = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id=? AND created_at=?
        """,
        (user_id, today),
    ).fetchone()[0]

    # 查詢分類統計
    rows = conn.execute(
        """
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=? AND created_at=?
        GROUP BY category
        """,
        (user_id, today),
    ).fetchall()

    conn.close()

    return total, rows


# /help 使用說明
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "每日支出統計 Bot 使用流程：\n\n"
        "1. 使用 /add 金額 分類 新增今日支出\n"
        "2. 使用 /summary 查看今天的支出總額與分類統計\n\n"
        "範例：\n"
        "/add 80 午餐\n"
        "/add 35 交通\n"
        "/summary\n\n"
        "指令列表：\n"
        "/help：查看使用說明\n"
        "/add：新增今日支出\n"
        "/summary：查看今日支出摘要"
    )


# /add 新增支出
async def add(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # 檢查參數數量
    if len(context.args) < 2:
        await update.message.reply_text(
            "用法：/add 金額 分類"
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

    # 新增資料到 SQLite
    add_expense(
        str(update.effective_user.id),
        amount,
        category
    )

    await update.message.reply_text(
        "已新增今日支出。"
    )


# /summary 今日摘要
async def summary(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    total, rows = summary_today(
        str(update.effective_user.id)
    )

    lines = [f"今天總支出：${total:.0f}"]

    # 有支出資料時顯示分類統計
    if rows:
        lines.append("")
        lines.append("分類統計：")

        for category, amount in rows:
            lines.append(
                f"{category}：${amount:.0f}"
            )

    # 沒有資料時顯示提示
    else:
        lines.append(
            "目前今天還沒有支出紀錄。"
        )

    await update.message.reply_text(
        "\n".join(lines)
    )


# 主程式
def main() -> None:

    init_db() # 啟動前初始化資料庫
    print("機器人啟用中")
    print("可以先輸出/help指令")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("summary", summary))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()