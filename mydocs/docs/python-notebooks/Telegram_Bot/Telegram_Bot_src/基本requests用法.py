import requests
import json

API_URL = "https://jsonplaceholder.typicode.com/posts/1"


def main() -> None:
    # 用公開測試 API 示範最基本的 GET 請求
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    # 轉成 Python 字典
    data = response.json()

    print("API 回傳結果：")
    print(json.dumps(data, indent=4, ensure_ascii=False)) # 把 Python 資料轉成 JSON 格式字串（string）


if __name__ == "__main__":
    main()