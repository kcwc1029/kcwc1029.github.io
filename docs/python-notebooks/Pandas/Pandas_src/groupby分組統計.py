from pathlib import Path

import pandas as pd

dataset_path = Path(__file__).resolve().parents[1] / "Pandas_datasets" / "職訓班求職追蹤.csv"
df = pd.read_csv(dataset_path)
df["平均薪資"] = (df["薪資下限"] + df["薪資上限"]) / 2

class_summary = df.groupby("班別").agg(
    投遞筆數=("學員編號", "count"),
    平均薪資=("平均薪資", "mean"),
    平均通勤=("通勤分鐘", "mean"),
    平均滿意度=("滿意度", "mean"),
)

print("各班別求職狀況:")
print(class_summary.round(2))

status_summary = df.groupby(["班別", "錄取狀態"]).size()
print("\n各班別錄取狀態筆數:")
print(status_summary)

