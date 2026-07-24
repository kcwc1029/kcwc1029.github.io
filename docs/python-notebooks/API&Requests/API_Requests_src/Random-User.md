Random User 是免費、開源的假會員資料 API，可以產生姓名、性別、Email、電話、地址、照片等資料，官方也把它定位成「像 Lorem Ipsum 一樣，但用在人員資料」的測試資料產生器。

```py
# API 網址
https://randomuser.me/api/

# 一次產生多筆：
https://randomuser.me/api/?results=10

# 指定國家
https://randomuser.me/api/?nat=us,gb,ca

# 只取需要欄位：
https://randomuser.me/api/?inc=name,email,phone,location,picture
```

### 範例：取得一位假會員資料

```py
"""取得一位假會員資料"""
import requests


API_URL = "https://randomuser.me/api/"


def main() -> None:
    # 發送 GET 請求，向 Random User API 要一筆假會員資料
    response = requests.get(API_URL, timeout=10)

    # 檢查 HTTP 狀態碼，如果失敗會丟出錯誤
    response.raise_for_status()

    # 將 JSON 回傳結果轉成 Python 字典
    data = response.json()

    # results 是一個清單，第一筆會員資料放在 results[0]
    user = data["results"][0]

    # 取出常用欄位
    name = user["name"]
    full_name = f"{name['title']} {name['first']} {name['last']}"
    email = user["email"]
    phone = user["phone"]
    country = user["location"]["country"]
    city = user["location"]["city"]
    picture = user["picture"]["large"]

    print("===== 假會員資料 =====")
    print(f"姓名：{full_name}")
    print(f"Email：{email}")
    print(f"電話：{phone}")
    print(f"國家：{country}")
    print(f"城市：{city}")
    print(f"照片：{picture}")


if __name__ == "__main__":
    main()
```

### 產生 20 位會員並匯出 CSV

```py
""" 產生 20 位會員並匯出 CSV """
import requests
import pandas as pd


API_URL = "https://randomuser.me/api/"


def fetch_users(count: int = 20) -> list[dict]:
    """
    從 Random User API 取得多筆假會員資料。
    """
    params = {
        "results": count,
        "inc": "name,gender,email,phone,location,picture,login,dob,nat"
    }

    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data["results"]


def clean_user(user: dict) -> dict:
    """
    將 API 原始資料整理成比較適合課堂使用的格式。
    """
    name = user["name"]
    location = user["location"]
    dob = user["dob"]

    return {
        "會員ID": user["login"]["uuid"],
        "姓名": f"{name['title']} {name['first']} {name['last']}",
        "性別": user["gender"],
        "年齡": dob["age"],
        "Email": user["email"],
        "電話": user["phone"],
        "國家": location["country"],
        "城市": location["city"],
        "地址": f"{location['street']['number']} {location['street']['name']}",
        "國籍代碼": user["nat"],
        "大頭貼": user["picture"]["medium"]
    }


def main() -> None:
    users = fetch_users(count=20)

    # 將每一位會員整理成乾淨格式
    cleaned_users = [clean_user(user) for user in users]

    # 轉成 pandas DataFrame
    df = pd.DataFrame(cleaned_users)

    print("===== 會員資料表 =====")
    print(df)

    # 匯出 CSV，方便後續做資料分析或後台系統練習
    df.to_csv("API_Requests_datasets/random_users.csv", index=False, encoding="utf-8-sig")

    print("\n已匯出 random_users.csv")


if __name__ == "__main__":
    main()
```
