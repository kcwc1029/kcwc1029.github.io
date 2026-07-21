"""依 meta.has_next 取得全部 72 筆 API 資料。"""

import time

import requests

from api_utils import BASE_URL

page = 1
all_products: list[dict] = []

while True:
    response = requests.get(
        f"{BASE_URL}/products",
        params={"page": page, "per_page": 15},
        timeout=(3.05, 10),
    )
    response.raise_for_status()
    payload = response.json()
    all_products.extend(payload["data"])
    print(f"第 {page} 頁取得 {len(payload['data'])} 筆，累計 {len(all_products)} 筆")

    if not payload["meta"]["has_next"]:
        break
    page += 1
    time.sleep(0.1)

print("API 宣告總筆數：", payload["meta"]["total"])
print("實際取得總筆數：", len(all_products))
