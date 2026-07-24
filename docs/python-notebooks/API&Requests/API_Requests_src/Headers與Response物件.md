```py
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

headers = {
    "Accept": "application/json",
    "User-Agent": "APIRequestsCourse/1.0 (vocational-training)",
    "X-Request-ID": "class-demo-001",
}

response = requests.get(url, headers=headers, timeout=5)
response.raise_for_status()

print("請求方法：", response.request.method)
print("請求標頭：", dict(response.request.headers))
print("最終網址：", response.url)
print("回應時間：", response.elapsed.total_seconds(), "秒")
print("回應標頭：", dict(response.headers))

data = response.json()

print("JSON 內容：", data)
print("文章標題：", data["title"])
```