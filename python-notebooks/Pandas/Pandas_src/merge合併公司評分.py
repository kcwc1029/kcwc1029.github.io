from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
jobs_path = project_root / "Pandas_datasets" / "職訓班求職追蹤.csv"
companies_path = project_root / "Pandas_datasets" / "公司評分.csv"

jobs = pd.read_csv(jobs_path)
companies = pd.read_csv(companies_path)

# merge 像 Excel 的 VLOOKUP：用共同欄位把兩張表接起來。
merged = jobs.merge(companies, on="公司名稱", how="left")

print("合併後前 10 筆:")
print(merged[["姓名", "公司名稱", "投遞職缺", "員工評分", "是否遠端", "加班程度"]].head(10))

