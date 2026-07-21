"""使用 params 查詢指定分類、價格範圍與排序。"""

import requests

from api_utils import BASE_URL

params = {
    "category": "學習進修",
    "min_price": 200,
    "max_price": 500,
    "sort": "-rating",  # 負號代表由大到小
    "page": 1,
    "per_page": 20,
}

response = requests.get(f"{BASE_URL}/products", params=params, timeout=5)
response.raise_for_status()
payload = response.json()

print("完整請求網址：", response.url)
print("符合筆數：", payload["meta"]["total"])
for product in payload["data"]:
    print(f'{product["name"]}｜NT$ {product["price"]}｜評分 {product["rating"]}')
