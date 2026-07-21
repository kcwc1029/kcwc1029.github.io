import cv2
import mediapipe as mp


def main():
    cap = cv2.VideoCapture(0)
    mp_selfie = mp.solutions.selfie_segmentation

    with mp_selfie.SelfieSegmentation(model_selection=1) as segmenter:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = segmenter.process(rgb)
            mask = results.segmentation_mask > 0.5
            blur = cv2.GaussianBlur(frame, (55, 55), 0)
            output = frame.copy()
            output[~mask] = blur[~mask]

            cv2.imshow("AI 視訊美化工具 - 按 q 離開", output)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
