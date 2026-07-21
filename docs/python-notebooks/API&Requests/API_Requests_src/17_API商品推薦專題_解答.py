"""專題解答：可靠地串接分頁 API、驗證、分析並輸出推薦報表。"""

import time

import pandas as pd
import requests

from api_utils import BASE_URL, OUTPUT_DIR, prepare_output

prepare_output()
all_products: list[dict] = []
page = 1

with requests.Session() as session:
    session.headers.update({
        "User-Agent": "VocationalTrainingApiProject/1.0",
        "Accept": "application/json",
    })

    while True:
        try:
            response = session.get(
                f"{BASE_URL}/products",
                params={"page": page, "per_page": 20, "sort": "id"},
                timeout=(3.05, 10),
            )
            response.raise_for_status()
            payload = response.json()
        except requests.exceptions.RequestException as error:
            raise SystemExit(f"第 {page} 頁取得失敗：{error}") from error

        if "data" not in payload or "meta" not in payload:
            raise ValueError("API 回應不符合 data/meta 契約")
        all_products.extend(payload["data"])
        print(f"第 {page} 頁完成，累計 {len(all_products)} 筆")

        if not payload["meta"]["has_next"]:
            expected_total = payload["meta"]["total"]
            break
        page += 1
        time.sleep(0.1)

ids = [item["id"] for item in all_products]
if len(all_products) != expected_total or len(ids) != len(set(ids)):
    raise ValueError("API 資料有漏抓或重複")

df = pd.DataFrame(all_products)
df["discount_percent"] = ((df["original_price"] - df["price"]) / df["original_price"] * 100).round(1)
recommended = df.query("price <= 500 and rating >= 4.7 and stock > 0").copy()
recommended = recommended.sort_values(["rating", "price"], ascending=[False, True])

output_file = OUTPUT_DIR / "API_商品推薦清單_解答.csv"
recommended.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"完成：原始 {len(df)} 筆、推薦 {len(recommended)} 筆")
print("輸出：", output_file)
print(recommended[["name", "category", "price", "rating", "discount_percent"]].to_string(index=False))
