# file_name: 07_ai_finger_rehab_system.py

import math
import cv2
import mediapipe as mp


# 食指關節點
INDEX_MCP = 5   # 食指根部
INDEX_PIP = 6   # 食指第一關節
INDEX_TIP = 8   # 食指指尖


def calculate_angle(a, b, c):
    """
    計算三個點形成的角度
    b 是中間點
    """

    ab_x = a.x - b.x
    ab_y = a.y - b.y

    cb_x = c.x - b.x
    cb_y = c.y - b.y

    dot = ab_x * cb_x + ab_y * cb_y

    ab_length = math.hypot(ab_x, ab_y)
    cb_length = math.hypot(cb_x, cb_y)

    if ab_length == 0 or cb_length == 0:
        return 0

    cos_value = dot / (ab_length * cb_length)
    cos_value = max(-1, min(1, cos_value))

    angle = math.degrees(math.acos(cos_value))

    return angle


def landmark_to_pixel(landmark, width, height):
    x = int(landmark.x * width)
    y = int(landmark.y * height)
    return x, y


def main():
    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    rehab_count = 0
    was_bent = False

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as hands:

        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("讀不到 Webcam 畫面")
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            status = "No Hand"
            angle_text = "Angle: --"

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                landmarks = hand.landmark

                mcp = landmarks[INDEX_MCP]
                pip = landmarks[INDEX_PIP]
                tip = landmarks[INDEX_TIP]

                angle = calculate_angle(mcp, pip, tip)

                angle_text = f"Index Angle: {angle:.1f}"

                # 角度越小，代表手指越彎
                if angle < 120:
                    status = "Finger Bent"
                    was_bent = True

                # 從彎曲恢復到伸直，算一次復健動作
                elif angle > 160:
                    status = "Finger Straight"

                    if was_bent:
                        rehab_count += 1
                        was_bent = False

                else:
                    status = "Moving"

                mp_drawing.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                # 轉成畫面座標
                mcp_xy = landmark_to_pixel(mcp, width, height)
                pip_xy = landmark_to_pixel(pip, width, height)
                tip_xy = landmark_to_pixel(tip, width, height)

                # 強調食指三個關節點
                cv2.circle(frame, mcp_xy, 8, (0, 255, 0), -1)
                cv2.circle(frame, pip_xy, 8, (0, 255, 255), -1)
                cv2.circle(frame, tip_xy, 8, (0, 255, 0), -1)

                # 畫出食指骨架線
                cv2.line(frame, mcp_xy, pip_xy, (255, 0, 0), 3)
                cv2.line(frame, pip_xy, tip_xy, (255, 0, 0), 3)

                # 在關節旁顯示角度
                cv2.putText(
                    frame,
                    f"{angle:.1f}",
                    (pip_xy[0] + 10, pip_xy[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

            cv2.putText(
                frame,
                status,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                angle_text,
                (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Rehab Count: {rehab_count}",
                (30, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                "AI Finger Rehab System - Press q to quit",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()