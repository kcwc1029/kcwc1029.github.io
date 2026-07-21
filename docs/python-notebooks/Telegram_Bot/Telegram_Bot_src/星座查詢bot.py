
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from dotenv import load_dotenv
import os


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


ZODIAC_DATA = {
    "牡羊": {
        "性格": "直接、行動力強、喜歡快速做決定，不太愛拖泥帶水。",
        "喜歡": "有活力、有反應、有挑戰感的人與事情。",
        "討厭": "被管太多、被冷處理、遇到猶豫不決的人。",
        "注意": "牡羊容易衝太快，聊天時可以給他明確回應，不要一直吊胃口。"
    },
    "金牛": {
        "性格": "穩定、慢熟、重視安全感，喜歡一步一步確認關係。",
        "喜歡": "真誠、穩定、有生活感的人，也很吃美食與陪伴。",
        "討厭": "忽冷忽熱、太浮誇、說話不算話。",
        "注意": "金牛不一定會馬上熱情，但他願意花時間陪你，通常就是有好感。"
    },
    "雙子": {
        "性格": "聰明、反應快、喜歡聊天，對新鮮事很有興趣。",
        "喜歡": "有趣、會接話、有想法的人。",
        "討厭": "無聊、太黏、一直逼他表態。",
        "注意": "雙子很吃聊天節奏，話題卡住太久，他可能就會慢慢失去興趣。"
    },
    "巨蟹": {
        "性格": "敏感、重感情、很在意安全感，也容易想很多。",
        "喜歡": "溫柔、穩定、會照顧情緒的人。",
        "討厭": "冷漠、敷衍、講話太傷人。",
        "注意": "巨蟹嘴上可能說沒事，但其實很在意細節。回訊息不要太像客服。"
    },
    "獅子": {
        "性格": "自信、愛面子、重視被肯定，也很有保護慾。",
        "喜歡": "欣賞他、給他舞台、願意互相支持的人。",
        "討厭": "被貶低、被忽視、被公開打臉。",
        "注意": "跟獅子相處，不是要一直捧他，而是要讓他覺得你看見他的好。"
    },
    "處女": {
        "性格": "細心、理性、標準高，常常嘴上挑剔但其實是在乎。",
        "喜歡": "乾淨、有條理、做事可靠的人。",
        "討厭": "混亂、隨便、講了不改。",
        "注意": "處女座很看細節，答應的小事最好做到，這比甜言蜜語更有用。"
    },
    "天秤": {
        "性格": "重視相處感、懂社交、喜歡舒服平衡的關係。",
        "喜歡": "有品味、好溝通、情緒穩定的人。",
        "討厭": "壓迫感太強、場面尷尬、情緒勒索。",
        "注意": "天秤容易猶豫，不要逼太快，但也不要完全沒主見。"
    },
    "天蠍": {
        "性格": "深情、敏銳、防備心強，喜歡觀察，不太輕易相信人。",
        "喜歡": "真誠、專一、有深度、能給安全感的人。",
        "討厭": "欺騙、曖昧不清、被背叛。",
        "注意": "天蠍很重視信任。不要玩測試，也不要故意讓他吃醋。"
    },
    "射手": {
        "性格": "自由、樂觀、喜歡探索，不愛被限制。",
        "喜歡": "幽默、有趣、願意一起冒險的人。",
        "討厭": "控制、查勤、太沉重的相處方式。",
        "注意": "射手需要空間。越想抓緊，他越想跑；越自在，他越想靠近。"
    },
    "魔羯": {
        "性格": "務實、慢熱、有責任感，常把感情藏在行動裡。",
        "喜歡": "成熟、穩定、有目標感的人。",
        "討厭": "不負責任、太情緒化、只說不做。",
        "注意": "魔羯不一定會講甜話，但他願意安排時間、解決問題，就是很重要的訊號。"
    },
    "水瓶": {
        "性格": "獨立、有想法、重視精神交流，不喜歡被框住。",
        "喜歡": "特別、有腦袋、能尊重彼此空間的人。",
        "討厭": "黏太緊、管太多、思想太封閉。",
        "注意": "水瓶需要朋友感。太快進入壓迫式關係，他會默默抽離。"
    },
    "雙魚": {
        "性格": "浪漫、感性、共感力強，容易被氣氛和細節打動。",
        "喜歡": "溫柔、體貼、有儀式感的人。",
        "討厭": "冷淡、現實到沒溫度、說話太刺。",
        "注意": "雙魚很吃情緒氛圍。你的一句關心，可能比大道理更有效。"
    },
}


GENDER_DATA = {
    "男": {
        "補充": "以男生版本來看，他可能比較不會直接說出脆弱面，但行動會透露很多。",
        "相處建議": "不要只聽他說什麼，也要看他願不願意花時間、主動安排、替你處理事情。"
    },
    "女": {
        "補充": "以女生版本來看，她通常更重視相處細節，也會觀察你是不是穩定一致。",
        "相處建議": "不要只用甜言蜜語，記得把小事做好，安全感常常是從細節累積的。"
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用星座查詢 Bot！\n\n"
        "你可以直接輸入：\n"
        "天蠍男\n"
        "魔羯女\n"
        "雙魚女\n"
        "獅子男\n\n"
        "我會回覆這個星座的性格、喜歡什麼、討厭什麼，以及相處時要注意的地方。"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "使用方式很簡單：\n\n"
        "請輸入「星座 + 性別」\n\n"
        "例如：\n"
        "天蠍男\n"
        "魔羯女\n"
        "雙子男\n"
        "巨蟹女\n\n"
        "目前支援 12 星座：\n"
        "牡羊、金牛、雙子、巨蟹、獅子、處女、天秤、天蠍、射手、魔羯、水瓶、雙魚"
    )


async def zodiac_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "目前可以查詢的格式：\n\n"
        "牡羊男、牡羊女\n"
        "金牛男、金牛女\n"
        "雙子男、雙子女\n"
        "巨蟹男、巨蟹女\n"
        "獅子男、獅子女\n"
        "處女男、處女女\n"
        "天秤男、天秤女\n"
        "天蠍男、天蠍女\n"
        "射手男、射手女\n"
        "魔羯男、魔羯女\n"
        "水瓶男、水瓶女\n"
        "雙魚男、雙魚女"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    found_zodiac = None
    found_gender = None

    for zodiac_name in ZODIAC_DATA.keys():
        if zodiac_name in text:
            found_zodiac = zodiac_name
            break

    if "男" in text:
        found_gender = "男"
    elif "女" in text:
        found_gender = "女"

    if found_zodiac and found_gender:
        zodiac_info = ZODIAC_DATA[found_zodiac]
        gender_info = GENDER_DATA[found_gender]

        reply = (
            f"{found_zodiac}{found_gender} 星座分析\n\n"
            f"性格：\n{zodiac_info['性格']}\n\n"
            f"喜歡：\n{zodiac_info['喜歡']}\n\n"
            f"討厭：\n{zodiac_info['討厭']}\n\n"
            f"相處注意：\n{zodiac_info['注意']}\n\n"
            f"{found_gender}生補充：\n{gender_info['補充']}\n\n"
            f"建議：\n{gender_info['相處建議']}"
        )

    elif found_zodiac and not found_gender:
        reply = (
            f"我有看到你輸入「{found_zodiac}」，但還缺少性別。\n\n"
            f"請輸入像這樣的格式：\n"
            f"{found_zodiac}男\n"
            f"{found_zodiac}女"
        )

    elif found_gender and not found_zodiac:
        reply = (
            "我有看到性別，但還沒看到星座。\n\n"
            "請輸入像這樣的格式：\n"
            "天蠍男\n"
            "魔羯女\n"
            "雙魚女"
        )

    else:
        reply = (
            "我目前還看不懂這個格式。\n\n"
            "請輸入「星座 + 性別」。\n\n"
            "例如：\n"
            "天蠍男\n"
            "魔羯女\n"
            "雙魚女\n\n"
            "可輸入 /zodiac 查看支援清單。"
        )

    await update.message.reply_text(reply)


def main() -> None:
    print("機器人啟用中")
    print("可以先輸出/help指令")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("zodiac", zodiac_list))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()