"""學生練習：串接所有分頁，產生高評價優惠商品報表。"""

import pandas as pd
import requests

from api_utils import BASE_URL, OUTPUT_DIR, prepare_output

prepare_output()

# TODO 1：使用 Session，設定 User-Agent 與 Accept。
# TODO 2：呼叫 /products，使用 per_page=20 取得全部分頁。
# TODO 3：每次請求設定 timeout、呼叫 raise_for_status()。
# TODO 4：驗證最後取得 72 筆，且商品 id 不重複。
# TODO 5：轉成 DataFrame，計算 discount_percent。
# TODO 6：篩選 price <= 500、rating >= 4.7、stock > 0。
# TODO 7：依 rating 降冪、price 升冪排序。
# TODO 8：輸出 API_商品推薦清單_我的答案.csv。

all_products: list[dict] = []

# 請從這裡開始完成。

