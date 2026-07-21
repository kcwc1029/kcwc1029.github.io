# file_name: hand_screenshot.py

import cv2
import math
from pathlib import Path
from datetime import datetime

import mediapipe as mp


# =========================
# 截圖資料夾
# =========================
SAVE_DIR = Path("screenshots")
SAVE_DIR.mkdir(exist_ok=True)


# =========================
# MediaPipe Hands
# =========================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def distance(p1, p2):
    """計算兩點距離"""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    screenshot_count = 0
    is_pinching = False

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        while True:
            ret, frame = cap.read()

            if not ret:
                print("讀取畫面失敗")
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:

                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

                    # 大拇指指尖：4
                    thumb_tip = hand_landmarks.landmark[4]

                    # 食指指尖：8
                    index_tip = hand_landmarks.landmark[8]

                    thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
                    index_pos = (int(index_tip.x * w), int(index_tip.y * h))

                    d = distance(thumb_pos, index_pos)

                    cv2.circle(frame, thumb_pos, 8, (0, 0, 255), -1)
                    cv2.circle(frame, index_pos, 8, (0, 0, 255), -1)
                    cv2.line(frame, thumb_pos, index_pos, (0, 255, 0), 3)

                    cv2.putText(
                        frame,
                        f"{int(d)} px",
                        (index_pos[0] + 10, index_pos[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

                    # =========================
                    # 手指捏合觸發截圖
                    # =========================
                    if d < 35 and not is_pinching:
                        screenshot_count += 1

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        save_path = SAVE_DIR / f"screenshot_{timestamp}.png"

                        cv2.imwrite(str(save_path), frame)
                        print(f"已截圖：{save_path}")

                        is_pinching = True

                    # 手指放開後，才能再次截圖
                    if d >= 45:
                        is_pinching = False

            cv2.putText(
                frame,
                f"Screenshots: {screenshot_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.imshow("Hand Screenshot - press q to quit", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()