from ultralytics import YOLO




image_path = "../YOLOv8_datasets/街景照片.png"
model = YOLO("yolov8n.pt")
result = model.predict(image_path, conf=0.35, verbose=False)[0]

if result.boxes is None or len(result.boxes) == 0:
    print("這張圖片沒有偵測到符合門檻的物件。")
else:
    for index, box in enumerate(result.boxes, start=1):
        class_id = int(box.cls.item())
        confidence = float(box.conf.item())
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        class_name = result.names[class_id]

        print(
            f"第 {index} 個物件：{class_name}，"
            f"信心分數 {confidence:.2%}，"
            f"座標 ({x1:.0f}, {y1:.0f}) 到 ({x2:.0f}, {y2:.0f})"
        )

