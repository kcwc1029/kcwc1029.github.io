import os
import cv2
import math
import time
import requests
from dotenv import load_dotenv
from ultralytics import YOLO


# =========================
# 讀取 .env
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
# 模型設定
# =========================

object_model = YOLO("yolov8n.pt")
pose_model = YOLO("yolov8n-pose.pt")


# =========================
# 參數設定
# =========================

CAMERA_INDEX = 0

DANGEROUS_CLASSES = {
    43: "knife",
    76: "scissors",
}

WRIST_DISTANCE_THRESHOLD = 100
OBJECT_CONFIDENCE = 0.15
POSE_CONFIDENCE = 0.35

ALERT_COOLDOWN = 10
last_alert_time = 0


# =========================
# 工具函式
# =========================

def distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def get_box_center(box):
    x1, y1, x2, y2 = box
    return (
        int((x1 + x2) / 2),
        int((y1 + y2) / 2)
    )


def draw_text(frame, text, position, color=(0, 0, 255)):
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )


# =========================
# 開啟攝影機
# =========================

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError("無法開啟攝影機，請把 CAMERA_INDEX 改成 1 試試看。")


while True:

    success, frame = cap.read()

    if not success:
        break

    dangerous_items = []
    holding_dangerous_object = False
    attack_pose = False
    detected_label = ""

    # =========================
    # YOLOv8 偵測危險物品
    # =========================

    object_results = object_model(
        frame,
        conf=OBJECT_CONFIDENCE,
        verbose=False
    )

    for box in object_results[0].boxes:

        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if cls_id in DANGEROUS_CLASSES:

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            dangerous_items.append({
                "box": [x1, y1, x2, y2],
                "label": DANGEROUS_CLASSES[cls_id],
                "conf": conf,
            })

    # =========================
    # YOLOv8-Pose 偵測人體姿態
    # =========================

    pose_results = pose_model(
        frame,
        conf=POSE_CONFIDENCE,
        verbose=False
    )

    annotated_frame = pose_results[0].plot()

    # =========================
    # 畫出危險物品框
    # =========================

    for item in dangerous_items:

        x1, y1, x2, y2 = item["box"]
        label = item["label"]
        conf = item["conf"]

        cv2.rectangle(
            annotated_frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 0, 255),
            3
        )

        draw_text(
            annotated_frame,
            f"{label} {conf:.2f}",
            (int(x1), int(y1) - 10),
            (0, 0, 255)
        )

    # =========================
    # 判斷是否持有危險物品、攻擊姿勢
    # =========================

    if pose_results[0].keypoints is not None:

        keypoints_data = pose_results[0].keypoints.xy

        for person_keypoints in keypoints_data:

            person_keypoints = person_keypoints.cpu().numpy()

            left_shoulder = person_keypoints[5]
            right_shoulder = person_keypoints[6]
            left_elbow = person_keypoints[7]
            right_elbow = person_keypoints[8]
            left_wrist = person_keypoints[9]
            right_wrist = person_keypoints[10]

            wrists = [
                ("left", left_wrist, left_shoulder, left_elbow),
                ("right", right_wrist, right_shoulder, right_elbow),
            ]

            for item in dangerous_items:

                dangerous_box = item["box"]
                dangerous_label = item["label"]
                dangerous_center = get_box_center(dangerous_box)

                for side, wrist, shoulder, elbow in wrists:

                    wrist_point = (
                        int(wrist[0]),
                        int(wrist[1])
                    )

                    shoulder_point = (
                        int(shoulder[0]),
                        int(shoulder[1])
                    )

                    elbow_point = (
                        int(elbow[0]),
                        int(elbow[1])
                    )

                    if wrist_point == (0, 0):
                        continue

                    wrist_distance = distance(
                        dangerous_center,
                        wrist_point
                    )

                    if wrist_distance < WRIST_DISTANCE_THRESHOLD:

                        holding_dangerous_object = True
                        detected_label = dangerous_label

                        cv2.line(
                            annotated_frame,
                            dangerous_center,
                            wrist_point,
                            (0, 0, 255),
                            3
                        )

                        draw_text(
                            annotated_frame,
                            f"Holding {dangerous_label}",
                            (30, 50),
                            (0, 0, 255)
                        )

                        # 手腕高於肩膀，疑似舉起危險物品
                        if wrist_point[1] < shoulder_point[1]:
                            attack_pose = True

                        # 手臂接近伸直，疑似刺擊
                        arm_length = distance(
                            shoulder_point,
                            wrist_point
                        )

                        forearm_length = distance(
                            elbow_point,
                            wrist_point
                        )

                        upper_arm_length = distance(
                            shoulder_point,
                            elbow_point
                        )

                        if arm_length > (forearm_length + upper_arm_length) * 0.75:
                            attack_pose = True

    # =========================
    # 顯示危險等級
    # =========================

    if len(dangerous_items) > 0:
        draw_text(
            annotated_frame,
            "Level 1: Dangerous Object Detected",
            (30, 90),
            (0, 165, 255)
        )

    if holding_dangerous_object:
        draw_text(
            annotated_frame,
            "Level 2: Person Holding Dangerous Object",
            (30, 130),
            (0, 0, 255)
        )

    if attack_pose:
        draw_text(
            annotated_frame,
            "Level 3: Attack Pose Warning",
            (30, 170),
            (0, 0, 255)
        )

        now = time.time()

        if now - last_alert_time > ALERT_COOLDOWN:

            warning_text = f"警告：偵測到疑似持有 {detected_label}，並出現攻擊姿勢。"

            print(warning_text)

            cv2.imwrite(
                "dangerous_object_warning.jpg",
                annotated_frame
            )

            send_line_message(warning_text)

            last_alert_time = now

    # =========================
    # 顯示畫面
    # =========================

    cv2.imshow(
        "YOLOv8 Dangerous Object + Pose + LINE",
        annotated_frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()