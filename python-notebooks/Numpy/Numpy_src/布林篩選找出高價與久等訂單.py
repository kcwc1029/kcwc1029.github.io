import csv
from pathlib import Path

import numpy as np

dataset_path = Path(__file__).resolve().parents[1] / "Numpy_datasets" / "飲料店一週訂單.csv"

rows = []
with dataset_path.open("r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

drinks = np.array([row["飲品"] for row in rows])
stores = np.array([row["門市"] for row in rows])
quantities = np.array([int(row["數量"]) for row in rows])
prices = np.array([int(row["單價"]) for row in rows])
wait_minutes = np.array([int(row["等待分鐘"]) for row in rows])
ratings = np.array([int(row["評分"]) for row in rows])

revenue = quantities * prices

# 條件可以像白話文一樣組合：金額 >= 150，而且等待時間 >= 10 分鐘。
mask = (revenue >= 150) & (wait_minutes >= 10)

print("高價又久等的訂單:")
for drink, store, money, wait, rating in zip(drinks[mask], stores[mask], revenue[mask], wait_minutes[mask], ratings[mask]):
    print(f"{store} | {drink} | 金額 {money} 元 | 等待 {wait} 分鐘 | 評分 {rating}")

