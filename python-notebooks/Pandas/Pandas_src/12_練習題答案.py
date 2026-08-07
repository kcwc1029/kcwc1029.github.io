from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
dataset_path = project_root / "Pandas_datasets" / "職訓班求職追蹤.csv"
df = pd.read_csv(dataset_path)
df["平均薪資"] = (df["薪資下限"] + df["薪資上限"]) / 2

print("練習 1: 總共有幾筆投遞紀錄")
print(len(df))

print("\n練習 2: 面試邀約率")
interview_rate = (df["面試邀約"] == "是").mean()
print(f"{interview_rate:.2%}")

print("\n練習 3: 哪個班別平均薪資最高")
salary_by_class = df.groupby("班別")["平均薪資"].mean().sort_values(ascending=False)
print(salary_by_class.round(0))

print("\n練習 4: 找出錄取且平均薪資 >= 40000 的紀錄")
accepted_high_salary = df[(df["錄取狀態"] == "錄取") & (df["平均薪資"] >= 40000)]
print(accepted_high_salary[["姓名", "班別", "公司名稱", "投遞職缺", "平均薪資"]])

print("\n練習 5: 各產業投遞筆數")
print(df["公司產業"].value_counts())

print("\n練習 6: 每位學員投遞幾次、錄取幾次")
student_summary = df.groupby("姓名").agg(
    投遞次數=("學員編號", "count"),
    錄取次數=("錄取狀態", lambda data: (data == "錄取").sum()),
)
print(student_summary)

