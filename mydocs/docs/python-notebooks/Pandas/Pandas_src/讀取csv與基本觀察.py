from pathlib import Path

import pandas as pd

dataset_path = Path(__file__).resolve().parents[1] / "Pandas_datasets" / "職訓班求職追蹤.csv"

df = pd.read_csv(dataset_path)

print("前 5 筆資料:")
print(df.head())

print("\n資料形狀:")
print(df.shape)

print("\n欄位資訊:")
print(df.info())

print("\n數值欄位摘要:")
print(df.describe())

