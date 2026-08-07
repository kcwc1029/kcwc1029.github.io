"""用 countplot 回答：同學最常選哪種飲料？"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chart_utils import DATA_FILE, save_chart, setup_chart

setup_chart()
df = pd.read_csv(DATA_FILE)
order = df["最常買飲料"].value_counts().index

plt.figure(figsize=(10, 5))
ax = sns.countplot(data=df, y="最常買飲料", order=order, hue="最常買飲料", legend=False)
ax.bar_label(ax.containers[0])  # 在柱子尾端顯示人數
plt.title("職訓學員最常購買的飲料")
plt.xlabel("人數")
plt.ylabel("飲料")
save_chart("飲料人氣排行.png")
