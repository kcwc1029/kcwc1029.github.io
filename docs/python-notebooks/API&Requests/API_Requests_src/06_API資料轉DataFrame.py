"""將 API JSON 轉成 DataFrame，計算優惠後輸出 CSV。"""

import pandas as pd
import requests

from api_utils import BASE_URL, OUTPUT_DIR, prepare_output

prepare_output()
response = requests.get(f"{BASE_URL}/products", params={"per_page": 30}, timeout=5)
response.raise_for_status()
df = pd.DataFrame(response.json()["data"])

df["discount_amount"] = df["original_price"] - df["price"]
df["discount_percent"] = (df["discount_amount"] / df["original_price"] * 100).round(1)
recommended = df.query("price <= 500 and rating >= 4.7 and stock > 0")
recommended = recommended.sort_values(["rating", "price"], ascending=[False, True])

output_file = OUTPUT_DIR / "第一頁API優惠商品.csv"
recommended.to_csv(output_file, index=False, encoding="utf-8-sig")
print(recommended[["name", "price", "rating", "discount_percent"]].to_string(index=False))
print("已輸出：", output_file)
