from pathlib import Path

import pandas as pd

dataset_path = Path(__file__).resolve().parents[1] / "Pandas_datasets" / "職訓班求職追蹤.csv"
df = pd.read_csv(dataset_path)
df["平均薪資"] = (df["薪資下限"] + df["薪資上限"]) / 2

# 先依平均薪資由高到低，再依通勤分鐘由低到高。
ranked = df.sort_values(by=["平均薪資", "通勤分鐘"], ascending=[False, True])

print("高薪且通勤較短的前 10 個機會:")
print(ranked[["姓名", "投遞職缺", "公司名稱", "平均薪資", "通勤分鐘", "錄取狀態"]].head(10))

