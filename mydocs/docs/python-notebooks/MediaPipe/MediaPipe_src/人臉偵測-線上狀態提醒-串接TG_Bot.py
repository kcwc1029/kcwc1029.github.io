# file_name: 02_face_detection_tg_notify.py

import os
import json
import threading

import cv2
import requests
import mediapipe as mp

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)


# =========================
# 基本設定
# =========================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUBSCRIBERS_FILE = "subscribers.json"

camera_thread = None
camera_running = False


# =========================
# 訂閱者資料處理
# =========================

def load_subscribers():

    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {
            "chat_ids": []
        }


def save_subscribers(data):

    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


def add_subscriber(chat_id):

    data = load_subscribers()

    if chat_id not in data["chat_ids"]:
        data["chat_ids"].append(chat_id)
        save_subscribers(data)


# =========================
# Telegram 發送通知
# =========================

def send_telegram_message(text):

    data = load_subscribers()

    for chat_id in data["chat_ids"]:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        try:
            requests.post(
                url,
                data=payload,
                timeout=5
            )

            print(f"已發送通知給：{chat_id}")

        except Exception as e:
            print("TG 通知失敗：", e)


# =========================
# MediaPipe 人臉偵測
# =========================

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def face_detection_loop():

    global camera_running

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("無法開啟 Webcam")
        camera_running = False
        return

    notified = False

    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.6,
    ) as face_detection:

        while camera_running:

            success, frame = cap.read()

            if not success:
                print("讀不到 Webcam 畫面")
                break

            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = face_detection.process(rgb)

            status_text = "Waiting..."
            status_color = (0, 0, 255)

            if results.detections:

                status_text = "Student Online"
                status_color = (0, 255, 0)

                for detection in results.detections:
                    mp_drawing.draw_detection(
                        frame,
                        detection
                    )

                if not notified:

                    send_telegram_message(
                        "📢 學生已上線！"
                    )

                    notified = True

            else:
                notified = False

            cv2.putText(
                frame,
                status_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                status_color,
                2
            )

            cv2.imshow(
                "AI Face Detection - Press q to quit",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                camera_running = False
                break

    cap.release()
    cv2.destroyAllWindows()
    camera_running = False


# =========================
# Telegram 指令
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    global camera_thread
    global camera_running

    chat_id = update.effective_chat.id

    add_subscriber(chat_id)

    await update.message.reply_text(
        "已開啟學生上線通知。\n"
        "現在開始偵測 Webcam，偵測到人臉時會通知你。"
    )

    if not camera_running:

        camera_running = True

        camera_thread = threading.Thread(
            target=face_detection_loop,
            daemon=True
        )

        camera_thread.start()

    else:
        await update.message.reply_text(
            "Webcam 偵測已經在執行中。"
        )


async def stop(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    global camera_running

    camera_running = False

    await update.message.reply_text(
        "已停止 Webcam 偵測。"
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    await update.message.reply_text(
        "可用指令：\n\n"
        "/start 開始偵測並接收通知\n"
        "/stop 停止 Webcam 偵測\n"
        "/help 查看說明"
    )


# =========================
# 主程式
# =========================

def main():

    if BOT_TOKEN is None:
        raise ValueError("找不到 BOT_TOKEN，請確認 .env 是否設定完成。")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("help", help_command))

    print("Telegram Bot 已啟動")
    app.run_polling()


if __name__ == "__main__":
    main()