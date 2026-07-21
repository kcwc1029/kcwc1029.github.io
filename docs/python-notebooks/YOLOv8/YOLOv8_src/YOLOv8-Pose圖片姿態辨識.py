from ultralytics import YOLO

model = YOLO("yolov8n-pose.pt")

results = model("../YOLOv8_datasets/男生軀體.png")

# 顯示結果
results[0].show()