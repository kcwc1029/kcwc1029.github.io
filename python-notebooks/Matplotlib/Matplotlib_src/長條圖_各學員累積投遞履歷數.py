import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

df = pd.read_csv("../Matplotlib_datasets/職訓生活觀察.csv")

# 核心寫法：
# 長條圖適合比較不同類別，例如不同學員投遞履歷的數量。
applications = df.groupby("學員姓名")["投遞履歷數"].sum().sort_values(ascending=False)

plt.figure(figsize=(9, 5))
plt.bar(applications.index, applications.values, color="#457b9d")
plt.title("各學員累積投遞履歷數")
plt.xlabel("學員")
plt.ylabel("投遞履歷數")

# 在每個長條上方加上數字，方便學生直接讀圖。
for index, value in enumerate(applications.values):
    plt.text(index, value + 0.5, str(value), ha="center")

plt.tight_layout()
plt.show()
