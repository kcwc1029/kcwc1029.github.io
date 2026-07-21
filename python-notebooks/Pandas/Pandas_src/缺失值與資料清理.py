from pathlib import Path

import pandas as pd

dataset_path = Path(__file__).resolve().parents[1] / "Pandas_datasets" / "職訓班求職追蹤.csv"
df = pd.read_csv(dataset_path)

print("每個欄位缺失值數量:")
print(df.isna().sum())

# 備註空白很正常，代表沒有特別補充。
df["備註"] = df["備註"].fillna("無")

# 去除文字欄位前後空白，避免「台北市」和「 台北市」被當成不同資料。
text_columns = ["姓名", "居住縣市", "班別", "投遞職缺", "公司名稱", "公司產業", "面試邀約", "錄取狀態"]
for column in text_columns:
    df[column] = df[column].str.strip()

print("\n清理後備註欄前 10 筆:")
print(df[["姓名", "公司名稱", "備註"]].head(10))

