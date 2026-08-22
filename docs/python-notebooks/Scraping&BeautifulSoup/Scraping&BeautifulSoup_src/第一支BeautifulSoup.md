```py
"""第一次解析 HTML：找一個與找全部。"""

from bs4 import BeautifulSoup


# 讀取 HTML 檔案
with open("../Scraping&BeautifulSoup_datasets/迷你商店.html", "r", encoding="utf-8") as file:
    html = file.read()

# 解析 HTML
soup = BeautifulSoup(html, "html.parser")
# BeautifulSoup 再把長字串解析成樹。
# `html.parser` 是 Python 內建解析器，教室環境不需額外安裝。

# 找第一個 h1
title = soup.find("h1")
print("頁面標題：", title.get_text(strip=True))


# 找出所有商品
cards = soup.find_all("article", class_="product")

print("商品數量：", len(cards))

for card in cards:
    name = card.find("h2", class_="name")
    print("-", name.get_text(strip=True))
```
