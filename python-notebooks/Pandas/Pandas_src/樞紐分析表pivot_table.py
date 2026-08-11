from pathlib import Path

import pandas as pd

dataset_path = Path(__file__).resolve().parents[1] / "Pandas_datasets" / "職訓班求職追蹤.csv"
df = pd.read_csv(dataset_path)

# pivot_table 很像 Excel 的樞紐分析表。
# 這裡統計每個班別在不同錄取狀態下有幾筆資料。
pivot = pd.pivot_table(
    df,
    index="班別",
    columns="錄取狀態",
    values="學員編號",
    aggfunc="count",
    fill_value=0,
)

print("班別 x 錄取狀態:")
print(pivot)

