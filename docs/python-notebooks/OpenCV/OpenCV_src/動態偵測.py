import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

previous = None

while True:
    ok, frame = cap.read()

    if not ok:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 第一張畫面先存起來
    if previous is None:
        previous = gray
        continue

    # 計算差異
    diff = cv2.absdiff(previous, gray)

    # 二值化
    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # 找輪廓
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # 畫框
    for c in contours:

        # 過濾太小的雜訊
        if cv2.contourArea(c) < 500:
            continue

        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            "MOVEMENT DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    cv2.imshow("motion detector", frame)

    # 更新上一張
    previous = gray

    # 按 q 離開
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()