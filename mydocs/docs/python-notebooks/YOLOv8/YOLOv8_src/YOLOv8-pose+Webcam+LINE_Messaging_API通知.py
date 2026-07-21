import os
import time
from datetime import datetime

import cv2
import requests
from dotenv import load_dotenv
from ultralytics import YOLO


# =========================
# 讀取 LINE 設定
# =========================

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")


# =========================
# LINE 推播函式
# =========================

def send_line_message(text):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    }

    data = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": text,
            }
        ],
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("LINE 訊息已送出")
    else:
        print("LINE 發送失敗：", response.status_code)
        print(response.text)


# =========================
# 判斷手是否舉起
# =========================

def detect_raise_hand(person_keypoints):
    """
    YOLOv8-pose keypoints:
    5  = left shoulder
    6  = right shoulder
    9  = left wrist
    10 = right wrist

    y 座標越小，代表位置越高
    """

    left_shoulder = person_keypoints[5]
    right_shoulder = person_keypoints[6]
    left_wrist = person_keypoints[9]
    right_wrist = person_keypoints[10]

    left_hand_up = left_wrist[1] < left_shoulder[1]
    right_hand_up = right_wrist[1] < right_shoulder[1]

    if left_hand_up and right_hand_up:
        return "雙手舉起"

    if left_hand_up:
        return "左手舉起"

    if right_hand_up:
        return "右手舉起"

    return None


# =========================
# 主程式
# =========================

def main():
    model = YOLO("yolov8n-pose.pt")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("無法開啟攝影機，請檢查 USB CAM 或改成 VideoCapture(1)")
        return

    last_alert_time = 0
    alert_cooldown = 5

    print("YOLOv8 Pose + LINE 通知系統啟動")
    print("按 q 離開")

    while True:
        success, frame = cap.read()

        if not success:
            print("讀取攝影機失敗")
            break

        start_time = time.time()

        results = model.predict(
            frame,
            conf=0.5,
            verbose=False
        )

        result = results[0]
        annotated_frame = result.plot()

        people_count = 0

        if result.keypoints is not None:
            keypoints = result.keypoints.xy

            people_count = len(keypoints)

            for index, person in enumerate(keypoints):
                person_keypoints = person.cpu().numpy()

                raise_status = detect_raise_hand(person_keypoints)

                if raise_status:
                    cv2.putText(
                        annotated_frame,
                        f"Person {index + 1}: {raise_status}",
                        (30, 120 + index * 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                    now = time.time()

                    if now - last_alert_time > alert_cooldown:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        message = (
                            f"🚨 {raise_status}檢測\n"
                            f"👤 人員 #{index + 1}\n"
                            f"⏱ 時間: {current_time}\n"
                            f"🤚 {raise_status}"
                        )

                        send_line_message(message)

                        last_alert_time = now

        end_time = time.time()
        fps = 1 / (end_time - start_time)

        cv2.putText(
            annotated_frame,
            f"FPS: {int(fps)}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            annotated_frame,
            f"People: {people_count}",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("YOLOv8 Hand Raise Detection - LINE", annotated_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()