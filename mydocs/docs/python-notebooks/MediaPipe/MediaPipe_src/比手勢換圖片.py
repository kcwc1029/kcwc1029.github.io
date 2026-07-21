# file_name: 02_gesture_five_board.py

from pathlib import Path
from collections import Counter, deque
import math
import requests

import cv2
import mediapipe as mp
import numpy as np


# =========================
# 圖片設定
# =========================

ASSETS_DIR = Path("hand_assets")
ASSETS_DIR.mkdir(exist_ok=True)

IMAGE_URLS = {
    "open_hand": "https://i.pinimg.com/736x/50/40/d3/5040d3cb865815175124ab08e8127bca.jpg",  # 張開手掌
    "thumbs_up": "https://i.pinimg.com/736x/22/6f/e9/226fe91e4b33666f893d08522a26ee51.jpg",  # 比讚
    "peace": "https://i.pinimg.com/736x/d0/ce/1c/d0ce1c23661ba9d05358422bd4f9771a.jpg",  # YA
    "gun": "https://i.pinimg.com/736x/5f/43/ca/5f43ca6677720fad65e923104606955a.jpg",  # 手槍
    "double_fist": "https://i.pinimg.com/736x/13/44/e2/1344e2da13d50152ec80faf7afdf5da4.jpg",  # 雙拳頭
}

IMAGE_FILES = {
    key: ASSETS_DIR / f"{key}.jpg"
    for key in IMAGE_URLS
}


def create_placeholder(text):
    image = np.full((480, 640, 3), 240, dtype=np.uint8)

    cv2.putText(
        image,
        text,
        (50, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.4,
        (0, 0, 0),
        4,
    )

    return image


def download_images():
    for key, url in IMAGE_URLS.items():
        path = IMAGE_FILES[key]

        if path.exists() and path.stat().st_size > 0:
            continue

        try:
            print(f"下載圖片：{key}")

            response = requests.get(
                url,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "https://www.pinterest.com/",
                },
            )

            response.raise_for_status()

            path.write_bytes(response.content)

        except Exception as e:
            print(f"圖片下載失敗，改用替代圖：{key}")
            print(f"錯誤原因：{e}")

            placeholder = create_placeholder(key.upper())
            cv2.imwrite(str(path), placeholder)


def resize_to_panel(image, width=640, height=480):
    return cv2.resize(image, (width, height))


def load_images():
    images = {}

    for key, path in IMAGE_FILES.items():
        image = cv2.imread(str(path))

        if image is None:
            image = create_placeholder(key.upper())

        images[key] = resize_to_panel(image)

    return images


# =========================
# 手部座標與角度計算
# =========================

def get_point(hand_landmarks, index):
    point = hand_landmarks.landmark[index]
    return np.array([point.x, point.y], dtype=np.float32)


def angle_between(a, b, c):
    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (
        (np.linalg.norm(ba) * np.linalg.norm(bc)) + 1e-6
    )

    cosine = np.clip(cosine, -1.0, 1.0)

    return math.degrees(math.acos(cosine))


def is_finger_straight(hand_landmarks, mcp_id, pip_id, dip_id, tip_id):
    mcp = get_point(hand_landmarks, mcp_id)
    pip = get_point(hand_landmarks, pip_id)
    dip = get_point(hand_landmarks, dip_id)
    tip = get_point(hand_landmarks, tip_id)
    wrist = get_point(hand_landmarks, 0)

    pip_angle = angle_between(mcp, pip, dip)
    dip_angle = angle_between(pip, dip, tip)

    tip_farther_than_pip = (
        np.linalg.norm(tip - wrist) > np.linalg.norm(pip - wrist)
    )

    return pip_angle > 145 and dip_angle > 145 and tip_farther_than_pip


def is_thumb_open(hand_landmarks):
    thumb_cmc = get_point(hand_landmarks, 1)
    thumb_mcp = get_point(hand_landmarks, 2)
    thumb_ip = get_point(hand_landmarks, 3)
    thumb_tip = get_point(hand_landmarks, 4)

    index_mcp = get_point(hand_landmarks, 5)

    thumb_angle = angle_between(thumb_cmc, thumb_mcp, thumb_ip)
    thumb_ip_angle = angle_between(thumb_mcp, thumb_ip, thumb_tip)

    thumb_is_straight = thumb_angle > 125 and thumb_ip_angle > 125
    thumb_away_from_palm = abs(thumb_tip[0] - index_mcp[0]) > 0.06

    return thumb_is_straight and thumb_away_from_palm


def get_finger_status(hand_landmarks):
    return {
        "thumb": is_thumb_open(hand_landmarks),
        "index": is_finger_straight(hand_landmarks, 5, 6, 7, 8),
        "middle": is_finger_straight(hand_landmarks, 9, 10, 11, 12),
        "ring": is_finger_straight(hand_landmarks, 13, 14, 15, 16),
        "pinky": is_finger_straight(hand_landmarks, 17, 18, 19, 20),
    }


# =========================
# 手勢判斷
# =========================

def recognize_one_hand(fingers):
    thumb = fingers["thumb"]
    index = fingers["index"]
    middle = fingers["middle"]
    ring = fingers["ring"]
    pinky = fingers["pinky"]

    up_count = sum([index, middle, ring, pinky])

    if up_count >= 4:
        return "open_hand"

    if thumb and up_count == 0:
        return "thumbs_up"

    if index and middle and not ring and not pinky:
        return "peace"

    if thumb and index and not middle and not ring and not pinky:
        return "gun"

    if not thumb and up_count == 0:
        return "fist"

    return "unknown"


def recognize_gesture(all_fingers):
    gestures = [
        recognize_one_hand(fingers)
        for fingers in all_fingers
    ]

    if len(gestures) >= 2 and gestures[0] == "fist" and gestures[1] == "fist":
        return "double_fist"

    if gestures:
        gesture = gestures[0]

        if gesture != "fist":
            return gesture

    return "unknown"


def get_stable_gesture(history, current_gesture):
    if current_gesture != "unknown":
        history.append(current_gesture)

    if not history:
        return "open_hand"

    gesture, count = Counter(history).most_common(1)[0]

    if count >= 4:
        return gesture

    return history[-1]


# =========================
# 主程式
# =========================

def main():
    download_images()
    gesture_images = load_images()

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("無法開啟 Webcam，請確認鏡頭是否被其他程式占用。")
        return

    gesture_history = deque(maxlen=8)

    gesture_text = {
        "open_hand": "OPEN HAND",
        "thumbs_up": "THUMBS UP",
        "peace": "PEACE",
        "gun": "GUN",
        "double_fist": "DOUBLE FIST",
        "unknown": "UNKNOWN",
    }

    while True:
        success, frame = cap.read()

        if not success:
            print("讀取 Webcam 失敗")
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        current_gesture = "unknown"
        all_fingers = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                )

                fingers = get_finger_status(hand_landmarks)
                all_fingers.append(fingers)

            current_gesture = recognize_gesture(all_fingers)

            first_fingers = all_fingers[0]

            debug_text = (
                f"T:{int(first_fingers['thumb'])} "
                f"I:{int(first_fingers['index'])} "
                f"M:{int(first_fingers['middle'])} "
                f"R:{int(first_fingers['ring'])} "
                f"P:{int(first_fingers['pinky'])}"
            )

            cv2.putText(
                frame,
                debug_text,
                (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2,
            )

        stable_gesture = get_stable_gesture(
            gesture_history,
            current_gesture,
        )

        right_panel = gesture_images.get(
            stable_gesture,
            gesture_images["open_hand"],
        ).copy()

        cv2.putText(
            frame,
            f"Gesture: {gesture_text.get(stable_gesture, 'UNKNOWN')}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3,
        )

        cv2.putText(
            right_panel,
            gesture_text.get(stable_gesture, "UNKNOWN"),
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 255),
            3,
        )

        output = np.hstack([frame, right_panel])

        cv2.imshow("Gesture Five Board", output)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()