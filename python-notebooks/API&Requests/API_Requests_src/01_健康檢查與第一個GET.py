"""使用 GET 呼叫公開 API。"""

import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()

    print("狀態碼：", response.status_code)
    print("內容類型：", response.headers.get("Content-Type"))
    print("JSON 內容：", data)
    print("文章標題：", data["title"])

except requests.exceptions.HTTPError as error:
    print("HTTP 錯誤：", error)

except requests.exceptions.JSONDecodeError:
    print("伺服器回傳的內容不是合法 JSON")

except requests.exceptions.Timeout:
    print("請求逾時")

except requests.exceptions.RequestException as error:
    print("請求失敗：", error)