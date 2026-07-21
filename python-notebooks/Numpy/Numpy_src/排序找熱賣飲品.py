import csv
from pathlib import Path

import numpy as np

dataset_path = Path(__file__).resolve().parents[1] / "Numpy_datasets" / "飲料店一週訂單.csv"

with dataset_path.open("r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

drinks = np.array([row["飲品"] for row in rows])
quantities = np.array([int(row["數量"]) for row in rows])
prices = np.array([int(row["單價"]) for row in rows])
revenue = quantities * prices

unique_drinks = np.unique(drinks)
drink_revenue = []

for drink in unique_drinks:
    # 每次只挑出某一種飲品，計算它的總營收。
    total = revenue[drinks == drink].sum()
    drink_revenue.append(total)

drink_revenue = np.array(drink_revenue)

# argsort 會回傳排序後的位置；[::-1] 代表從大排到小。
rank_index = np.argsort(drink_revenue)[::-1]

print("飲品營收排行:")
for rank, index in enumerate(rank_index, start=1):
    print(f"第 {rank} 名: {unique_drinks[index]}，營收 {drink_revenue[index]} 元")

