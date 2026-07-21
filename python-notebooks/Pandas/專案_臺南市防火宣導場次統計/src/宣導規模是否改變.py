from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import re

### 設定圖表中文字型
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"] # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號顯示問題


### 讀取所有年度 CSV 檔案
data_dir = Path("data") # 指定存放 CSV 檔案的資料夾
files = data_dir.glob("*年防火宣導成果*.csv") # 取得所有年度防火宣導成果檔案


### 建立統計結果清單
summary = [] # 用來儲存各年度統計結果


### 逐年讀取資料並統計
for file in files:
    year = int(re.search(r"(\d+)年", file.name).group(1)) # 從檔名擷取年度
    df = pd.read_csv(file) # 讀取 CSV 檔案

    ### 計算年度總量
    total_events = df["合計場次"].sum() # 年度總宣導場次
    total_people = df["合計人次"].sum() # 年度總宣導人次
    total_staff = df["合計動員宣導人次"].sum() # 年度總動員人次


    ### 計算年度指標並加入結果清單
    summary.append({
        "年度": year,
        "宣導場次": total_events,
        "宣導人次": total_people,
        "動員人次": total_staff,
        "平均每場宣導人次": round(total_people / total_events, 2), # 每場平均觸及人數
        "平均每位動員觸及人次": round(total_people / total_staff, 2) # 每位宣導人員平均觸及人數
    })


### 建立年度統計 DataFrame
result = pd.DataFrame(summary) # 將統計結果轉成 DataFrame
result = result.sort_values("年度") # 依年度排序


### 顯示統計結果
print("Q1 宣導規模年度統計")
print(result)


### 匯出統計結果 CSV
result.to_csv(
    "Q1_宣導規模年度統計.csv",
    index=False,
    encoding="utf-8-sig" # 避免 Excel 開啟中文亂碼
)


### 圖表 1：歷年宣導場次變化
plt.figure(figsize=(10, 5))
plt.plot(
    result["年度"],
    result["宣導場次"],
    marker="o"
)
plt.title("歷年防火宣導場次變化")
plt.xlabel("年度")
plt.ylabel("宣導場次")
plt.grid(True)
plt.show()


### 圖表 2：歷年宣導人次變化
plt.figure(figsize=(10, 5))
plt.plot(
    result["年度"],
    result["宣導人次"],
    marker="o"
)
plt.title("歷年防火宣導人次變化")
plt.xlabel("年度")
plt.ylabel("宣導人次")
plt.grid(True)
plt.show()


### 圖表 3：歷年動員人次變化
plt.figure(figsize=(10, 5))
plt.plot(
    result["年度"],
    result["動員人次"],
    marker="o"
)
plt.title("歷年防火宣導動員人次變化")
plt.xlabel("年度")
plt.ylabel("動員人次")
plt.grid(True)
plt.show()