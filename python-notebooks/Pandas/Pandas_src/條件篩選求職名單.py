from pathlib import Path

import pandas as pd

dataset_path = Path(__file__).resolve().parents[1] / "Pandas_datasets" / "職訓班求職追蹤.csv"
df = pd.read_csv(dataset_path)
df["平均薪資"] = (df["薪資下限"] + df["薪資上限"]) / 2

# 找出薪資不錯、通勤不要太遠、已經拿到面試邀約的機會。
mask = (df["平均薪資"] >= 40000) & (df["通勤分鐘"] <= 45) & (df["面試邀約"] == "是")
good_chances = df.loc[mask, ["姓名", "投遞職缺", "公司名稱", "平均薪資", "通勤分鐘", "錄取狀態"]]

print("值得優先準備的面試機會:")
print(good_chances)

