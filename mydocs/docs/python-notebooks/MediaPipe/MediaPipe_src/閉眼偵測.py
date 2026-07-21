import math

import cv2
import mediapipe as mp


LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
LEFT_EYE_LEFT = 33
LEFT_EYE_RIGHT = 133


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def eye_open_ratio(landmarks):
    vertical = distance(
        landmarks[LEFT_EYE_TOP],
        landmarks[LEFT_EYE_BOTTOM]
    )

    horizontal = distance(
        landmarks[LEFT_EYE_LEFT],
        landmarks[LEFT_EYE_RIGHT]
    )

    return vertical / horizontal


def draw_eye_points(frame, landmarks):

    h, w, _ = frame.shape

    eye_points = [
        LEFT_EYE_TOP,
        LEFT_EYE_BOTTOM,
        LEFT_EYE_LEFT,
        LEFT_EYE_RIGHT
    ]

    points = {}

    # 畫出眼睛關鍵點
    for idx in eye_points:

        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)

        points[idx] = (x, y)

        cv2.circle(
            frame,
            (x, y),
            5,
            (0, 255, 0),
            -1
        )

    # 畫垂直線
    cv2.line(
        frame,
        points[LEFT_EYE_TOP],
        points[LEFT_EYE_BOTTOM],
        (255, 0, 0),
        2
    )

    # 畫水平線
    cv2.line(
        frame,
        points[LEFT_EYE_LEFT],
        points[LEFT_EYE_RIGHT],
        (0, 0, 255),
        2
    )


def main():

    cap = cv2.VideoCapture(0)

    mp_face_mesh = mp.solutions.face_mesh

    tired_frames = 0

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                break

            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = face_mesh.process(rgb)

            status = "No face"


            if results.multi_face_landmarks:

                landmarks = (
                    results
                    .multi_face_landmarks[0]
                    .landmark
                )

                # 畫眼睛點
                draw_eye_points(frame, landmarks)

                ratio = eye_open_ratio(landmarks)

                # 閉眼判斷
                if ratio < 0.18:
                    tired_frames += 1
                else:
                    tired_frames = 0

                # 疲勞提醒
                if tired_frames > 20:
                    status = "Fatigue Warning"
                else:
                    status = f"Eye Ratio: {ratio:.2f}"


            cv2.putText(
                frame,
                status,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            cv2.imshow(
                "AI Fatigue Warning System",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()