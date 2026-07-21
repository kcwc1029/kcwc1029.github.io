import cv2
import mediapipe as mp

TIP_IDS = [4, 8, 12, 16, 20]
FINGER_NAMES = ["Thumb", "Index", "Middle", "Ring", "Pinky"]


def count_fingers(hand_landmarks, handedness_label):
    landmarks = hand_landmarks.landmark
    fingers = []

    # 大拇指：左右手方向不同，所以要分開判斷
    if handedness_label == "Right":
        thumb_is_up = landmarks[4].x < landmarks[3].x
    else:
        thumb_is_up = landmarks[4].x > landmarks[3].x

    fingers.append(thumb_is_up)

    # 其他四根手指：指尖 y 比第二關節 y 更上方，代表伸出
    for tip_id in [8, 12, 16, 20]:
        finger_is_up = landmarks[tip_id].y < landmarks[tip_id - 2].y
        fingers.append(finger_is_up)

    # 回傳這隻手伸出了幾根手指 (0 ~ 5)
    return sum(fingers)


def main():
    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # 啟用雙手偵測 (max_num_hands=2)
    with mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as hands:

        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("讀不到 Webcam 畫面")
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            total_fingers = 0
            hand_detected = False

            # 如果偵測到手，跑迴圈計算每隻手的手指
            if results.multi_hand_landmarks and results.multi_handedness:
                hand_detected = True
                
                for i, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
                    
                    # 取得這隻手是左手還是右手
                    handedness_label = handedness.classification[0].label
                    
                    # 計算這隻手伸出了幾根手指
                    single_hand_count = count_fingers(hand_landmarks, handedness_label)
                    
                    # 累加到雙手總數
                    total_fingers += single_hand_count

                    # 繪製單手的骨架
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

                    # 將每隻手的偵測結果分別顯示在畫面上
                    cx = int(hand_landmarks.landmark[9].x * w)
                    cy = int(hand_landmarks.landmark[9].y * h)
                    cv2.putText(
                        frame,
                        f"{handedness_label}: {single_hand_count}",
                        (cx - 40, cy - 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 0),
                        2
                    )

            # 顯示最終加總數字
            if hand_detected:
                if total_fingers == 0:
                    number_text = "0"
                elif total_fingers <= 10:
                    number_text = str(total_fingers)
                else:
                    number_text = "Unknown"
            else:
                number_text = "No Hand"

            # 顯示總數字在左上角
            cv2.putText(
                frame,
                f"Number: {number_text}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )

            # 顯示視窗
            cv2.imshow(
                "AI Two Hands Number Recognition (1-10) - Press q to quit",
                frame
            )

            # 核心修正：確保 if 語句縮排與 cv2.imshow 對齊（都在 while 迴圈內）
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break  # 確保 break 被包在 if 與 while 裡面

    # 釋放資源：必須在 with 區塊結束後才執行
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()