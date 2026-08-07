import csv
from pathlib import Path

import numpy as np

dataset_path = Path(__file__).resolve().parents[1] / "Numpy_datasets" / "飲料店一週訂單.csv"

rows = []
with dataset_path.open("r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        rows.append(row)

# 把需要計算的欄位轉成 NumPy array。
quantities = np.array([int(row["數量"]) for row in rows])
prices = np.array([int(row["單價"]) for row in rows])
wait_minutes = np.array([int(row["等待分鐘"]) for row in rows])
ratings = np.array([int(row["評分"]) for row in rows])

revenue = quantities * prices

print("訂單筆數:", len(rows))
print("總杯數:", quantities.sum())
print("總營收:", revenue.sum())
print("平均等待分鐘:", wait_minutes.mean().round(2))
print("平均評分:", ratings.mean().round(2))
print("最高單筆金額:", revenue.max())

