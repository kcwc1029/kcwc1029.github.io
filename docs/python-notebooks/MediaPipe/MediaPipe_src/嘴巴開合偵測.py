# FaceMesh偷講話偵測
# file_name: 05_talking_detector.py

import math
import cv2
import mediapipe as mp


# 嘴巴 landmark 點
MOUTH_TOP = 13
MOUTH_BOTTOM = 14
MOUTH_LEFT = 78
MOUTH_RIGHT = 308


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def mouth_open_ratio(landmarks):
    vertical = distance(landmarks[MOUTH_TOP], landmarks[MOUTH_BOTTOM])
    horizontal = distance(landmarks[MOUTH_LEFT], landmarks[MOUTH_RIGHT])

    return vertical / horizontal


def draw_mouth_points(frame, landmarks):
    h, w, _ = frame.shape

    point_ids = [
        MOUTH_TOP,
        MOUTH_BOTTOM,
        MOUTH_LEFT,
        MOUTH_RIGHT
    ]

    points = {}

    for point_id in point_ids:
        x = int(landmarks[point_id].x * w)
        y = int(landmarks[point_id].y * h)

        points[point_id] = (x, y)

        cv2.circle(
            frame,
            (x, y),
            5,
            (0, 255, 0),
            -1
        )

    # 嘴巴上下距離
    cv2.line(
        frame,
        points[MOUTH_TOP],
        points[MOUTH_BOTTOM],
        (255, 0, 0),
        2
    )

    # 嘴巴左右寬度
    cv2.line(
        frame,
        points[MOUTH_LEFT],
        points[MOUTH_RIGHT],
        (0, 0, 255),
        2
    )


def main():
    cap = cv2.VideoCapture(0)

    mp_face_mesh = mp.solutions.face_mesh

    talking_frames = 0

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("讀不到 Webcam 畫面")
                break

            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = face_mesh.process(rgb)

            status = "No Face"
            color = (0, 0, 255)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark

                draw_mouth_points(frame, landmarks)

                ratio = mouth_open_ratio(landmarks)

                if ratio > 0.08:
                    talking_frames += 1
                else:
                    talking_frames = 0

                if talking_frames > 5:
                    status = "Talking Detected"
                    color = (0, 0, 255)
                else:
                    status = f"Mouth Ratio: {ratio:.2f}"
                    color = (0, 255, 0)

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
                "Talking Detector - Press q to quit",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()