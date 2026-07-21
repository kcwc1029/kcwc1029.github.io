import cv2
import csv
import time
from pathlib import Path

import mediapipe as mp


# =========================
# CSV 設定
# =========================
CSV_PATH = Path("finger_tap_records.csv")


# =========================
# MediaPipe Hands
# =========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


# =========================
# 按鈕設定
# =========================
buttons = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["CLR", "0", "DEL"],
    ["ENT"],
]

button_w = 90
button_h = 70
gap = 10

start_x = 340
start_y = 120


# =========================
# 狀態變數
# =========================
input_text = ""
history = []
last_pressed = None
last_press_time = 0
press_cooldown = 0.45


def save_to_csv(value):
    """把輸入結果存成 CSV"""
    is_new_file = not CSV_PATH.exists()

    with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        if is_new_file:
            writer.writerow(["value", "time"])

        writer.writerow([
            value,
            time.strftime("%Y-%m-%d %H:%M:%S")
        ])


def draw_button(frame, text, x, y, w, h, active=False):
    """畫出單顆按鈕"""
    if active:
        color = (80, 180, 80)
        border = (80, 255, 80)
    else:
        color = (45, 35, 40)
        border = (120, 100, 110)

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
    cv2.rectangle(frame, (x, y), (x + w, y + h), border, 2)

    font_scale = 1.0 if len(text) <= 3 else 0.8
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]

    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2

    cv2.putText(
        frame,
        text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (240, 240, 240),
        2,
    )


def build_button_positions():
    """建立每個按鈕的位置"""
    positions = []

    y = start_y

    for row in buttons:
        if len(row) == 1:
            # ENT 橫跨三格
            x = start_x
            w = button_w * 3 + gap * 2
            positions.append({
                "text": row[0],
                "x": x,
                "y": y,
                "w": w,
                "h": button_h,
            })
        else:
            for col, text in enumerate(row):
                x = start_x + col * (button_w + gap)
                positions.append({
                    "text": text,
                    "x": x,
                    "y": y,
                    "w": button_w,
                    "h": button_h,
                })

        y += button_h + gap

    return positions


def is_point_inside(px, py, button):
    """判斷手指是否碰到按鈕"""
    return (
        button["x"] <= px <= button["x"] + button["w"]
        and button["y"] <= py <= button["y"] + button["h"]
    )


def handle_press(text):
    """處理按鈕邏輯"""
    global input_text, history

    if text.isdigit():
        input_text += text

    elif text == "CLR":
        input_text = ""

    elif text == "DEL":
        input_text = input_text[:-1]

    elif text == "ENT":
        if input_text.strip():
            history.append(input_text)
            save_to_csv(input_text)
            input_text = ""


def main():
    global last_pressed, last_press_time

    button_positions = build_button_positions()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("無法開啟攝影機，請檢查 webcam 或把 VideoCapture(0) 改成 1")

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    ) as hands:

        while True:
            success, frame = cap.read()

            if not success:
                print("讀取攝影機失敗")
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            active_button = None
            index_x, index_y = None, None

            # =========================
            # 偵測食指位置
            # =========================
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                    )

                    # 食指指尖 landmark 8
                    index_tip = hand_landmarks.landmark[8]
                    index_x = int(index_tip.x * w)
                    index_y = int(index_tip.y * h)

                    cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), -1)

                    for button in button_positions:
                        if is_point_inside(index_x, index_y, button):
                            active_button = button
                            break

            # =========================
            # 按鍵觸發
            # =========================
            current_time = time.time()

            if active_button is not None:
                text = active_button["text"]

                if (
                    text != last_pressed
                    or current_time - last_press_time > press_cooldown
                ):
                    handle_press(text)
                    last_pressed = text
                    last_press_time = current_time
            else:
                last_pressed = None

            # =========================
            # 畫面 UI
            # =========================
            cv2.putText(
                frame,
                "FINGER TAP PAD",
                (40, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 220, 255),
                3,
            )

            cv2.line(frame, (40, 80), (310, 80), (0, 180, 255), 2)

            # 輸入框
            cv2.rectangle(frame, (40, 100), (320, 160), (50, 35, 35), -1)
            cv2.rectangle(frame, (40, 100), (320, 160), (0, 180, 255), 2)

            cv2.putText(
                frame,
                input_text if input_text else "Input...",
                (55, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 255, 255),
                2,
            )

            # History
            cv2.putText(
                frame,
                "History:",
                (40, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (180, 180, 180),
                2,
            )

            for i, item in enumerate(history[-5:]):
                cv2.putText(
                    frame,
                    item,
                    (60, 235 + i * 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (180, 255, 180),
                    2,
                )

            # 按鈕區
            for button in button_positions:
                is_active = active_button == button
                draw_button(
                    frame,
                    button["text"],
                    button["x"],
                    button["y"],
                    button["w"],
                    button["h"],
                    active=is_active,
                )

            cv2.putText(
                frame,
                "Press q to quit",
                (40, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (180, 180, 180),
                2,
            )

            cv2.imshow("MediaPipe Finger Tap Pad", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()