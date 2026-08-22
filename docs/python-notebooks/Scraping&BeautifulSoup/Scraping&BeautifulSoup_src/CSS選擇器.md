```py
"""第一次解析 HTML：找一個與找全部。"""

from bs4 import BeautifulSoup


# 讀取 HTML 檔案
with open("../Scraping&BeautifulSoup_datasets/迷你商店.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")



# 1. tag：找所有 article
articles = soup.select("article")
print("article 數量：", len(articles))


# 2. .class：找所有商品
products = soup.select(".product")
print("商品數量：", len(products))


# 3. #id：找網站標題
title = soup.select_one("#site-title")
print("網站標題：", title.get_text(strip=True))


# 4. A B：找商品裡面的名稱
names = soup.select("article.product .name")

for name in names:
    print("商品：", name.get_text(strip=True))


# 5. A > B：找 menu 的直接子元素 article
cards = soup.select("#menu > article")
print("直接子商品數量：", len(cards))


# 6. [attr]：找具有 data-id 的元素
items = soup.select("[data-id]")

for item in items:
    print("商品編號：", item["data-id"])


# 7. [attr=value]：指定商品編號
item = soup.select_one("[data-id='P003']")
print("P003：", item.select_one(".name").get_text(strip=True))


# 8. :not(...)：排除售完商品
available = soup.select(".product:not(.sold-out)")

print("目前可以購買：")

for item in available:
    name = item.select_one(".name").get_text(strip=True)
    print("-", name)
```
