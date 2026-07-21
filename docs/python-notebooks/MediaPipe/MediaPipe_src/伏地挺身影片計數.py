# file_name: 03_pushup_counter_video.py

import math
import cv2
import mediapipe as mp


VIDEO_PATH = "../MediaPipe_dataset/pushup_demo.mp4"

LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15


def angle(a, b, c):
    ab = (a.x - b.x, a.y - b.y)
    cb = (c.x - b.x, c.y - b.y)

    dot = ab[0] * cb[0] + ab[1] * cb[1]

    mag_ab = math.hypot(*ab)
    mag_cb = math.hypot(*cb)

    cosine = dot / (mag_ab * mag_cb + 1e-8)
    cosine = max(min(cosine, 1), -1)

    return math.degrees(math.acos(cosine))


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("無法讀取影片，請確認影片路徑是否正確：", VIDEO_PATH)
        return

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    count = 0
    is_down = False

    with mp_pose.Pose(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as pose:

        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("影片播放結束")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark

                elbow_angle = angle(
                    lm[LEFT_SHOULDER],
                    lm[LEFT_ELBOW],
                    lm[LEFT_WRIST]
                )

                if elbow_angle < 90:
                    is_down = True

                if is_down and elbow_angle > 150:
                    count += 1
                    is_down = False

                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

                cv2.putText(
                    frame,
                    f"Push-up: {count}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Elbow Angle: {elbow_angle:.0f}",
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

            display_frame = cv2.resize(frame, (960, 540))

            cv2.imshow(
                "AI Push-up Counter From Video - Press q to quit",
                display_frame
            )

            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()