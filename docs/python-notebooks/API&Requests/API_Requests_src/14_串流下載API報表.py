"""用 stream=True 分塊下載 API 提供的 CSV 報表。"""

import requests

from api_utils import BASE_URL, OUTPUT_DIR, prepare_output

prepare_output()
output_file = OUTPUT_DIR / "API下載商品報表.csv"

with requests.get(f"{BASE_URL}/products.csv", stream=True, timeout=(3, 30)) as response:
    response.raise_for_status()
    expected_type = response.headers.get("Content-Type", "")
    if "text/csv" not in expected_type:
        raise ValueError(f"預期 CSV，實際收到：{expected_type}")

    with output_file.open("wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

print("下載完成：", output_file)
print("檔案大小：", output_file.stat().st_size, "bytes")
