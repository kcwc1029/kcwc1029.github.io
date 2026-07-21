import cv2
import mediapipe as mp

TIP_IDS = [4, 8, 12, 16, 20]
FINGER_NAMES = ["Thumb", "Index", "Middle", "Ring", "Pinky"]


def get_finger_status(hand_landmarks, handedness_label):
    """
    取得每根手指的狀態：1 代表伸直，0 代表彎曲
    回傳格式例如：[1, 1, 0, 0, 0] (大拇指和食指伸直)
    """
    landmarks = hand_landmarks.landmark
    fingers = []

    # 大拇指：左右手方向不同，分開判斷
    if handedness_label == "Right":
        thumb_is_up = landmarks[4].x < landmarks[3].x
    else:
        thumb_is_up = landmarks[4].x > landmarks[3].x
    fingers.append(1 if thumb_is_up else 0)

    # 其他四根手指：指尖 y 比第二關節 y 更上方，代表伸出
    for tip_id in [8, 12, 16, 20]:
        finger_is_up = landmarks[tip_id].y < landmarks[tip_id - 2].y
        fingers.append(1 if finger_is_up else 0)

    return fingers


def recognize_taiwan_single_hand(fingers):
    """
    台式單手數字 1 ~ 10 辨識邏輯
    """
    # 1. 先判斷特殊手勢 (6, 7, 8, 9, 10)
    if fingers == [0, 0, 0, 0, 0]:
        return "10"                      # 握拳代表 10
        
    elif fingers == [1, 0, 0, 0, 1]:
        return "6"                      # 大拇指 + 小拇指 (打電話)
        
    elif fingers == [1, 1, 1, 0, 0]:
        return "8"                      # 大拇指 + 食指 + 中指
        
    elif fingers == [1, 1, 0, 0, 0]:
        return "7"                      # 大拇指 + 食指 (比槍)
        
    elif fingers == [1, 1, 1, 1, 0]:
        return "9"                      # 大拇指彎曲，其餘四指伸直
        
    # 2. 基礎手勢 (1 ~ 5) -> 直接看伸出幾根手指
    total = sum(fingers)
    if total <= 5 and total > 0:
        return str(total)

    return "Unknown"


def main():
    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # 設定最多支援 2 隻手
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

            number_text = "No Hand"
            
            # 用來儲存每隻手的詳細資料
            detected_hands_data = []

            if results.multi_hand_landmarks and results.multi_handedness:
                # 1. 蒐集當前畫面中所有手的狀態
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    handedness_label = handedness.classification[0].label
                    fingers = get_finger_status(hand_landmarks, handedness_label)
                    
                    # 記錄這隻手的骨架、手指狀態、以及伸直總數
                    detected_hands_data.append({
                        "landmarks": hand_landmarks,
                        "label": handedness_label,
                        "fingers": fingers,
                        "count": sum(fingers)
                    })

                    # 繪製單手骨架
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 2. 根據偵測到的「手部數量」執行不同的辨識邏輯
                num_hands = len(detected_hands_data)

                if num_hands == 1:
                    # 【單手模式】：採用台式 1-10 手勢
                    hand = detected_hands_data[0]
                    number_text = recognize_taiwan_single_hand(hand["fingers"])
                    
                    # 在手掌上方顯示這隻手目前的狀態 (如 [1, 0, 0, 0, 1])
                    cx = int(hand["landmarks"].landmark[9].x * w)
                    cy = int(hand["landmarks"].landmark[9].y * h)
                    cv2.putText(frame, f"Single ({hand['label']})", (cx - 40, cy - 60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                elif num_hands == 2:
                    # 【雙手模式】：採用雙手手指加總 (0-10)
                    total_sum = detected_hands_data[0]["count"] + detected_hands_data[1]["count"]
                    number_text = str(total_sum)

                    # 分別在兩隻手上標示各自貢獻了幾根手指
                    for hand in detected_hands_data:
                        cx = int(hand["landmarks"].landmark[9].x * w)
                        cy = int(hand["landmarks"].landmark[9].y * h)
                        cv2.putText(frame, f"Count: {hand['count']}", (cx - 40, cy - 60), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            # 3. 顯示最終辨識的數字結果
            cv2.putText(
                frame,
                f"Number: {number_text}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )

            cv2.imshow(
                "AI Ultimate Hand Recognition (1-10) - Press q to quit",
                frame
            )

            # 確保 break 在 while 迴圈內
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()