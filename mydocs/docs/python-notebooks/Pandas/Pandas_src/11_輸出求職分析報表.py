from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
dataset_path = project_root / "Pandas_datasets" / "職訓班求職追蹤.csv"
output_dir = project_root / "Pandas_outputs"
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(dataset_path)
df["平均薪資"] = (df["薪資下限"] + df["薪資上限"]) / 2

class_summary = df.groupby("班別").agg(
    投遞筆數=("學員編號", "count"),
    面試邀約數=("面試邀約", lambda data: (data == "是").sum()),
    錄取數=("錄取狀態", lambda data: (data == "錄取").sum()),
    平均薪資=("平均薪資", "mean"),
    平均通勤=("通勤分鐘", "mean"),
)

class_summary["面試邀約率"] = class_summary["面試邀約數"] / class_summary["投遞筆數"]
class_summary["錄取率"] = class_summary["錄取數"] / class_summary["投遞筆數"]

class_summary = class_summary.round(2)

output_path = output_dir / "班別求職分析.csv"
class_summary.to_csv(output_path, encoding="utf-8-sig")

print("已輸出:", output_path)
print(class_summary)

