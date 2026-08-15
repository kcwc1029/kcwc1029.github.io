網路不是函式直接呼叫，DNS、連線、TLS、Server 與傳輸每一層都可能失敗。

```py
import requests

# JSONPlaceholder 測試 API
url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    # 發送 GET 請求
    response = requests.get(
        url,
        timeout=(3.05, 10) # 連線逾時時間, 讀取逾時時間
        # timeout=0.000001 # 故意把等待時間設得非常短
    )

    # 檢查 HTTP 狀態碼
    response.raise_for_status()

    data = response.json() # 將 JSON 轉成 Python 字典
    # 顯示取得的資料
    print("取得資料成功")
    print("文章 ID：", data["id"])
    print("使用者 ID：", data["userId"])
    print("標題：", data["title"])
    print("內容：", data["body"])

except requests.exceptions.Timeout:
    print("等待逾時")

except requests.exceptions.ConnectionError:
    print("連線失敗")

except requests.exceptions.HTTPError as error:
    print("HTTP 錯誤：", error.response.status_code)

except requests.exceptions.JSONDecodeError:
    print("JSON 格式錯誤")

except requests.exceptions.RequestException as error:
    print("其他 Requests 錯誤：", error)
```
