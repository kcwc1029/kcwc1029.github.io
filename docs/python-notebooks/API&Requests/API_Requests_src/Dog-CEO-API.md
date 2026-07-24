Dog CEO API 主打開源狗狗圖片資料，官方說它提供超過 20,000 張狗狗圖片、涵蓋 120 多種品種；多張隨機圖片端點最多一次回傳 50 張

```py
# API 網址
https://dog.ceo/dog-api/

# 隨機取得一張狗狗圖片：
https://dog.ceo/api/breeds/image/random

# 一次取得多張狗狗圖片：
https://dog.ceo/api/breeds/image/random/3

# 取得所有狗狗品種：
https://dog.ceo/api/breeds/list/all

# 指定品種隨機圖片，例如柴犬：
https://dog.ceo/api/breed/shiba/images/random
```

### 範例：終端機版 Dog CEO 查詢器

```python
"""
範例：Dog CEO API 終端機查詢器

功能：
1. 隨機取得一張狗狗圖片
2. 一次取得多張狗狗圖片
3. 查看所有狗狗品種
4. 指定品種取得圖片
5. 詢問是否用瀏覽器開啟圖片

執行方式：
uv run python dog_ceo_cli_explorer.py
"""

import webbrowser
import requests


BASE_URL = "https://dog.ceo/api"


def get_json(url: str) -> dict:
    """送出 GET 請求，並把 API 回傳結果轉成 dict。"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_random_image() -> str:
    """取得一張隨機狗狗圖片。"""
    data = get_json(f"{BASE_URL}/breeds/image/random")
    return data["message"]


def get_random_images(count: int) -> list[str]:
    """一次取得多張隨機狗狗圖片。"""
    data = get_json(f"{BASE_URL}/breeds/image/random/{count}")
    return data["message"]


def get_all_breeds() -> dict:
    """取得所有狗狗品種。"""
    data = get_json(f"{BASE_URL}/breeds/list/all")
    return data["message"]


def get_breed_image(breed: str) -> str:
    """指定品種，取得一張隨機圖片。"""
    breed = breed.strip().lower()
    data = get_json(f"{BASE_URL}/breed/{breed}/images/random")
    return data["message"]


def ask_open_image(image_url: str) -> None:
    """詢問使用者是否要用瀏覽器開啟圖片。"""
    print("\n圖片網址：")
    print(image_url)

    answer = input("\n是否要用瀏覽器開啟圖片？(y/n)：").strip().lower()

    if answer == "y":
        webbrowser.open(image_url)
        print("已開啟瀏覽器。")
    else:
        print("已取消開啟圖片。")


def show_all_breeds() -> None:
    """用比較好讀的方式印出所有品種。"""
    breeds = get_all_breeds()

    print("\n=== 所有狗狗品種 ===")

    for breed, sub_breeds in breeds.items():
        if sub_breeds:
            print(f"- {breed}：{', '.join(sub_breeds)}")
        else:
            print(f"- {breed}")


def main() -> None:
    while True:
        print("\n=== Dog CEO API 狗狗圖片查詢器 ===")
        print("1. 隨機取得一張狗狗圖片")
        print("2. 一次取得多張狗狗圖片")
        print("3. 查看所有狗狗品種")
        print("4. 指定品種取得圖片")
        print("0. 離開")

        choice = input("\n請選擇功能：").strip()

        try:
            if choice == "1":
                image_url = get_random_image()
                ask_open_image(image_url)

            elif choice == "2":
                count = int(input("請輸入圖片張數(1-50)："))

                if count < 1 or count > 50:
                    print("張數請輸入 1 到 50。")
                    continue

                image_urls = get_random_images(count)

                print("\n=== 圖片列表 ===")
                for index, url in enumerate(image_urls, start=1):
                    print(f"{index}. {url}")

                answer = input("\n是否要開啟第一張圖片？(y/n)：").strip().lower()
                if answer == "y":
                    webbrowser.open(image_urls[0])

            elif choice == "3":
                show_all_breeds()

            elif choice == "4":
                breed = input("請輸入狗狗品種英文，例如 shiba、hound、pug：")
                image_url = get_breed_image(breed)
                ask_open_image(image_url)

            elif choice == "0":
                print("程式結束。")
                break

            else:
                print("請輸入正確選項。")

        except requests.RequestException as error:
            print("API 連線失敗：", error)

        except ValueError:
            print("輸入格式錯誤，請重新輸入。")


if __name__ == "__main__":
    main()
```

### 範例：Streamlit 狗狗圖片牆

```python
"""
範例：Dog CEO API Streamlit 狗狗圖片牆

功能：
1. 隨機狗狗圖片牆
2. 指定品種查詢
3. 顯示所有品種
4. 抽卡式狗狗推薦
5. 可下載圖片網址清單

執行方式：
uv run streamlit run dog_ceo_streamlit_gallery.py
"""

import random
import requests
import pandas as pd
import streamlit as st


BASE_URL = "https://dog.ceo/api"


st.set_page_config(
    page_title="Dog CEO 狗狗圖片牆",
    page_icon="🐶",
    layout="wide"
)


st.markdown(
    """
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #666;
        font-size: 18px;
        margin-bottom: 28px;
    }

    .dog-card {
        padding: 18px;
        border-radius: 24px;
        background: linear-gradient(135deg, #fff4d6, #ffffff);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.06);
    }

    .big-number {
        font-size: 34px;
        font-weight: 900;
    }

    .small-note {
        color: #777;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data(show_spinner=False)
def get_json(url: str) -> dict:
    """取得 API JSON 資料。"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(show_spinner=False)
def get_all_breeds() -> dict:
    """取得所有狗狗品種。"""
    data = get_json(f"{BASE_URL}/breeds/list/all")
    return data["message"]


def get_random_images(count: int) -> list[str]:
    """取得多張隨機狗狗圖片。"""
    data = get_json(f"{BASE_URL}/breeds/image/random/{count}")
    return data["message"]


def get_breed_random_image(breed: str) -> str:
    """指定品種取得一張圖片。"""
    data = get_json(f"{BASE_URL}/breed/{breed}/images/random")
    return data["message"]


def flatten_breeds(breeds: dict) -> list[str]:
    """
    把 Dog CEO 的品種資料整理成下拉選單格式。

    原始資料像這樣：
    {
        "hound": ["afghan", "basset"],
        "shiba": []
    }

    這裡先處理主品種，讓學生比較好理解。
    """
    return sorted(breeds.keys())


def show_image_grid(image_urls: list[str], columns_count: int = 3) -> None:
    """用多欄排版顯示圖片牆。"""
    columns = st.columns(columns_count)

    for index, image_url in enumerate(image_urls):
        with columns[index % columns_count]:
            st.image(image_url, use_container_width=True)
            st.caption(f"Dog #{index + 1}")


st.markdown("<div class='main-title'>🐶 Dog CEO 狗狗圖片牆</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>用 REST API 打造一個超療癒的狗狗圖片展示網站。</div>",
    unsafe_allow_html=True
)


try:
    breeds = get_all_breeds()
    breed_options = flatten_breeds(breeds)

    with st.sidebar:
        st.header("查詢設定")

        mode = st.radio(
            "選擇模式",
            ["隨機圖片牆", "指定品種", "今日狗狗抽卡", "品種資料表"]
        )

        image_count = st.slider(
            "圖片數量",
            min_value=3,
            max_value=50,
            value=9,
            step=1
        )

        selected_breed = st.selectbox(
            "選擇狗狗品種",
            breed_options,
            index=breed_options.index("shiba") if "shiba" in breed_options else 0
        )

        columns_count = st.slider(
            "每列顯示幾張",
            min_value=2,
            max_value=5,
            value=3
        )

        run_button = st.button("開始產生", type="primary", use_container_width=True)

        st.divider()
        st.caption("建議查詢：shiba、pug、husky、retriever、terrier")

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric("API 主題", "狗狗圖片")
    metric_col2.metric("可選品種", len(breed_options))
    metric_col3.metric("最多隨機張數", "50 張")

    st.divider()

    if mode == "隨機圖片牆":
        st.subheader("🎲 隨機狗狗圖片牆")

        if run_button:
            image_urls = get_random_images(image_count)
        else:
            image_urls = get_random_images(9)

        show_image_grid(image_urls, columns_count)

        df = pd.DataFrame({
            "編號": range(1, len(image_urls) + 1),
            "圖片網址": image_urls
        })

        csv_data = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "下載圖片網址 CSV",
            data=csv_data,
            file_name="dog_image_urls.csv",
            mime="text/csv"
        )

    elif mode == "指定品種":
        st.subheader(f"🐕 指定品種：{selected_breed}")

        image_urls = []

        if run_button:
            with st.spinner("正在召喚狗狗圖片..."):
                for _ in range(image_count):
                    image_urls.append(get_breed_random_image(selected_breed))
        else:
            for _ in range(6):
                image_urls.append(get_breed_random_image(selected_breed))

        st.success(f"已取得 {selected_breed} 的狗狗圖片")
        show_image_grid(image_urls, columns_count)

    elif mode == "今日狗狗抽卡":
        st.subheader("✨ 今日狗狗抽卡")

        card_col1, card_col2 = st.columns([1, 2])

        lucky_breed = random.choice(breed_options)
        lucky_image = get_breed_random_image(lucky_breed)

        comments = [
            "今天適合放慢速度，像狗狗曬太陽一樣。",
            "今天的任務是：不要把自己逼太緊。",
            "你今天的幸運值很高，適合開始一個小專案。",
            "這張狗狗提醒你：debug 也是人生的一部分。",
            "今天適合寫程式，也適合看狗。"
        ]

        with card_col1:
            st.markdown("<div class='dog-card'>", unsafe_allow_html=True)
            st.image(lucky_image, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with card_col2:
            st.markdown("### 你的今日狗狗")
            st.markdown(f"<div class='big-number'>{lucky_breed.upper()}</div>", unsafe_allow_html=True)
            st.write(random.choice(comments))

            st.info(
                "這個功能可以拿來教學生：API 不只能查資料，"
                "還可以搭配隨機邏輯做成有互動感的小作品。"
            )

            st.code(lucky_image)

    elif mode == "品種資料表":
        st.subheader("📋 Dog CEO 品種資料表")

        rows = []

        for breed, sub_breeds in breeds.items():
            rows.append({
                "主品種": breed,
                "是否有子品種": "是" if sub_breeds else "否",
                "子品種": ", ".join(sub_breeds) if sub_breeds else "無"
            })

        df = pd.DataFrame(rows)

        st.dataframe(df, use_container_width=True, height=520)

        st.download_button(
            "下載品種資料 CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="dog_breeds.csv",
            mime="text/csv"
        )

except requests.RequestException as error:
    st.error(f"API 連線失敗：{error}")

except Exception as error:
    st.error(f"程式發生錯誤：{error}")
```
