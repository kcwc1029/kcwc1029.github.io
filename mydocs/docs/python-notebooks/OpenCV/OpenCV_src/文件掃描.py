import cv2
import numpy as np
from pathlib import Path


points = []


def read_image(image_path):
    return cv2.imdecode(
        np.fromfile(str(image_path), dtype=np.uint8),
        cv2.IMREAD_COLOR
    )


def mouse_callback(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            print(f"第 {len(points)} 個點：({x}, {y})")


def order_points(points):
    points = np.array(points, dtype="float32")

    rect = np.zeros((4, 2), dtype="float32")

    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]

    return rect


def four_point_transform(image, points):
    rect = order_points(points)

    tl, tr, br, bl = rect

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = int(max(width_a, width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = int(max(height_a, height_b))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(
        image,
        matrix,
        (max_width, max_height)
    )

    return warped


current_file = Path(__file__).resolve()

image_path = (
    current_file.parent.parent
    / "OpenCV_datasets"
    / "Receipt.png"
)

image = read_image(image_path)

# 縮放比例
scale = 0.6

image = cv2.resize(
    image,
    None,
    fx=scale,
    fy=scale
)

if image is None:
    print("圖片讀取失敗")
    print(image_path)
    raise SystemExit


display = image.copy()

print("\n" + "=" * 50)
print("文件掃描器(Document Scanner)")
print("=" * 50)

print("\n操作說明：")
print("1. 依序點選文件的四個角")
print("2. 點選順序建議：")
print("   左上 → 右上 → 右下 → 左下")
print("3. 點滿四個角後按 Enter")
print("4. 按 ESC 可以離開程式")

print("\n快捷鍵：")
print("Enter -> 開始掃描")
print("ESC   -> 結束程式")

print("\n等待使用者點選四個角...")
print("-" * 50)

cv2.namedWindow("Click 4 corners")
cv2.setMouseCallback("Click 4 corners", mouse_callback)


while True:
    preview = display.copy()

    for index, point in enumerate(points):
        cv2.circle(preview, point, 8, (0, 0, 255), -1)
        cv2.putText(
            preview,
            str(index + 1),
            (point[0] + 10, point[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    if len(points) == 4:
        cv2.polylines(
            preview,
            [np.array(points, dtype=np.int32)],
            True,
            (0, 255, 0),
            3
        )

    cv2.imshow("Click 4 corners", preview)

    key = cv2.waitKey(1) & 0xFF

    if key == 13:  # Enter
        if len(points) == 4:
            break
        else:
            print("請先點滿 4 個角")

    if key == 27:  # ESC
        cv2.destroyAllWindows()
        raise SystemExit


warped = four_point_transform(
    image,
    np.array(points, dtype="float32")
)

gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

scan = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    21,
    10
)

cv2.imshow("Scanned Color", warped)
cv2.imshow("Scanned Black White", scan)

cv2.waitKey(0)
cv2.destroyAllWindows()