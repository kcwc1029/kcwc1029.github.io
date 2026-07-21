from pathlib import Path

import pandas as pd

dataset_path = Path(__file__).resolve().parents[1] / "Pandas_datasets" / "職訓班求職追蹤.csv"
df = pd.read_csv(dataset_path)

# 選取幾個上課常用欄位，讓表格不要一次太多資訊。
selected = df[["姓名", "班別", "投遞職缺", "薪資下限", "薪資上限", "通勤分鐘"]]
print(selected.head())

# 新增欄位：預估平均薪資。
df["平均薪資"] = (df["薪資下限"] + df["薪資上限"]) / 2

# 新增欄位：通勤是否偏久。
df["通勤分類"] = df["通勤分鐘"].apply(lambda minutes: "通勤偏久" if minutes >= 50 else "通勤可接受")

print("\n新增欄位後:")
print(df[["姓名", "投遞職缺", "平均薪資", "通勤分鐘", "通勤分類"]].head(10))

