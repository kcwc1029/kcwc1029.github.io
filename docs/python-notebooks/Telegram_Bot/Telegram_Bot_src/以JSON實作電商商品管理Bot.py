from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv

import json
import os


load_dotenv() # 載入 .env 檔案
BOT_TOKEN = os.getenv("BOT_TOKEN") # 讀取 Bot Token

DATA_FILE = "./telegram_bot_datasets/products.json" # 商品資料檔案

# 讀取 JSON 商品資料
def load_data() -> dict:

    # 檔案不存在時回傳空字典
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# 儲存 JSON 商品資料
def save_data(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False, # 正常顯示中文
            indent=2 # 美化 JSON 排版
        )


# /help 使用說明
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "電商商品管理 Bot 使用流程：\n\n"
        "1. 使用 /add 商品名稱 價格 新增商品\n"
        "2. 使用 /list 查看商品清單\n"
        "3. 使用 /sold 編號 將商品標記為已售出\n"
        "4. 使用 /delete 編號 刪除商品\n\n"
        "範例：\n"
        "/add 無線滑鼠 399\n"
        "/add 藍牙耳機 1290\n"
        "/list\n"
        "/sold 1\n"
        "/delete 2\n\n"
        "指令列表：\n"
        "/help - 查看使用說明\n"
        "/add - 新增商品\n"
        "/list - 查看商品清單\n"
        "/sold - 標記商品已售出\n"
        "/delete - 刪除商品"
    )


# /add 新增商品
async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # 檢查參數數量
    if len(context.args) < 2:
        await update.message.reply_text(
            "用法：/add 商品名稱 價格\n"
            "例如：/add 無線滑鼠 399"
        )
        return

    price_text = context.args[-1] # 最後一個參數當價格
    product_name = " ".join(context.args[:-1]) # 組合商品名稱

    # 驗證價格是否為整數
    if not price_text.isdigit():
        await update.message.reply_text(
            "價格必須是整數。\n"
            "例如：/add 無線滑鼠 399"
        )
        return

    price = int(price_text)

    user_id = str(update.effective_user.id)

    data = load_data() # 讀取商品資料

    # 建立使用者商品清單
    data.setdefault(user_id, [])

    # 新增商品
    data[user_id].append(
        {
            "name": product_name,
            "price": price,
            "sold": False
        }
    )

    save_data(data) # 儲存資料

    await update.message.reply_text(
        f"已新增商品：{product_name}\n"
        f"價格：{price} 元"
    )


# /list 查看商品清單
async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)

    items = load_data().get(user_id, []) # 取得商品清單

    if not items:
        await update.message.reply_text(
            "目前沒有商品資料。"
        )
        return

    lines = ["商品清單："]

    for index, item in enumerate(items, start=1):
        status = "已售出" if item["sold"] else "販售中"

        lines.append(
            f"{index}. [{status}] {item['name']} - {item['price']} 元"
        )

    await update.message.reply_text(
        "\n".join(lines)
    )


# /sold 標記商品已售出
async def sold_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # 檢查商品編號
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "用法：/sold 編號，例如：/sold 1"
        )
        return

    user_id = str(update.effective_user.id)

    data = load_data()
    items = data.get(user_id, [])

    index = int(context.args[0]) - 1 # 轉成索引

    # 檢查索引範圍
    if index < 0 or index >= len(items):
        await update.message.reply_text(
            "找不到這個商品編號。"
        )
        return

    items[index]["sold"] = True # 標記已售出

    save_data(data)

    await update.message.reply_text(
        f"已將商品標記為已售出：{items[index]['name']}"
    )


# /delete 刪除商品
async def delete_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # 檢查商品編號
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "用法：/delete 編號，例如：/delete 1"
        )
        return

    user_id = str(update.effective_user.id)

    data = load_data()
    items = data.get(user_id, [])

    index = int(context.args[0]) - 1 # 轉成索引

    # 檢查索引範圍
    if index < 0 or index >= len(items):
        await update.message.reply_text(
            "找不到這個商品編號。"
        )
        return

    removed = items.pop(index) # 刪除商品

    save_data(data)

    await update.message.reply_text(
        f"已刪除商品：{removed['name']}"
    )


# 主程式
def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/help指令")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build() # 建立 Bot

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_product))
    app.add_handler(CommandHandler("list", list_products))
    app.add_handler(CommandHandler("sold", sold_product))
    app.add_handler(CommandHandler("delete", delete_product))

    app.run_polling() # 啟動 Bot


if __name__ == "__main__":
    main()