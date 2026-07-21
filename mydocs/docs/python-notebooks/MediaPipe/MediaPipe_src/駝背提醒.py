# file_name: 06_standing_posture_checker.py

import cv2
import mediapipe as mp


LEFT_EAR = 7
LEFT_SHOULDER = 11
LEFT_HIP = 23


def to_pixel(landmark, width, height):
    x = int(landmark.x * width)
    y = int(landmark.y * height)
    return x, y


def main():
    cap = cv2.VideoCapture(0)

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as pose:

        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("讀不到 Webcam 畫面")
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            status = "No Body"
            color = (0, 0, 255)

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark

                ear = lm[LEFT_EAR]
                shoulder = lm[LEFT_SHOULDER]
                hip = lm[LEFT_HIP]

                ear_xy = to_pixel(ear, width, height)
                shoulder_xy = to_pixel(shoulder, width, height)
                hip_xy = to_pixel(hip, width, height)

                # 耳朵如果比肩膀往前太多，代表可能有駝背或頭前傾
                forward_distance = abs(ear_xy[0] - shoulder_xy[0])

                if forward_distance > 45:
                    status = "Bad Posture"
                    color = (0, 0, 255)
                else:
                    status = "Good Posture"
                    color = (0, 255, 0)

                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

                # 強調耳朵、肩膀、髖部三個點
                cv2.circle(frame, ear_xy, 8, (0, 255, 255), -1)
                cv2.circle(frame, shoulder_xy, 8, (0, 255, 0), -1)
                cv2.circle(frame, hip_xy, 8, (255, 0, 0), -1)

                # 畫出姿勢參考線
                cv2.line(frame, ear_xy, shoulder_xy, color, 3)
                cv2.line(frame, shoulder_xy, hip_xy, color, 3)

                cv2.putText(
                    frame,
                    f"Forward: {forward_distance}px",
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

            cv2.putText(
                frame,
                status,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

            cv2.imshow(
                "AI Standing Posture Checker - Press q to quit",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()