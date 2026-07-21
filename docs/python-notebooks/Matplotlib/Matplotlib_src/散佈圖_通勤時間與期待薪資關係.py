import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft JhengHei" # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False # 解決負號無法正常顯示

df = pd.read_csv("../Matplotlib_datasets/職訓生活觀察.csv")

# 散佈圖適合看兩個數字之間有沒有關係。
plt.figure(figsize=(9, 5))
plt.scatter(
    df["通勤分鐘"],
    df["期待薪資"],
    s=df["面試邀約數"] * 35 + 30,
    alpha=0.7,
    color="#6a4c93",
)
plt.title("通勤時間與期待薪資關係")
plt.xlabel("通勤分鐘")
plt.ylabel("期待薪資")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
