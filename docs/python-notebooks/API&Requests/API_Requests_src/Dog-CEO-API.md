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
import random
import requests
import pandas as pd
import streamlit as st


### API 設定
BASE_URL = "https://dog.ceo/api" # Dog CEO API 的基礎網址


### Streamlit 頁面設定
st.set_page_config(
    page_title="Dog CEO 狗狗圖片牆", # 瀏覽器分頁標題
    page_icon="🐶", # 瀏覽器分頁圖示
    layout="wide" # 使用寬版頁面配置
)


### 自訂 CSS 樣式
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
    unsafe_allow_html=True # 允許 Streamlit 執行 HTML 與 CSS
)


### 建立 API GET Request 函式
def get_json(url: str) -> dict:
    """
    向指定 API 網址發送 GET Request，
    並將回傳的 JSON 資料轉成 Python dict。
    """

    response = requests.get(
        url,
        timeout=10 # 最多等待 API 回應 10 秒
    )

    response.raise_for_status() # HTTP 狀態碼不是成功狀態時直接產生例外

    return response.json() # 將 JSON Response 轉成 Python dict


### 取得所有狗狗品種
@st.cache_data(show_spinner=False)
def get_all_breeds() -> dict:
    """
    取得 Dog CEO API 提供的所有狗狗品種。

    因為品種資料不常變動，
    使用 Streamlit cache 避免每次重新呼叫 API。
    """

    data = get_json(
        f"{BASE_URL}/breeds/list/all"
    )

    return data["message"] # message 裡面存放所有品種資料


### 取得多張隨機狗狗圖片
def get_random_images(count: int) -> list[str]:
    """
    根據指定數量，
    取得多張隨機狗狗圖片網址。
    """

    data = get_json(
        f"{BASE_URL}/breeds/image/random/{count}"
    )

    return data["message"] # 回傳圖片網址 list


### 取得指定品種的多張隨機圖片
def get_breed_random_images(
    breed: str,
    count: int
) -> list[str]:
    """
    根據指定狗狗品種與圖片數量，
    取得多張隨機圖片網址。
    """

    data = get_json(
        f"{BASE_URL}/breed/{breed}/images/random/{count}"
    )

    return data["message"]


### 取得指定品種的一張隨機圖片
def get_breed_random_image(breed: str) -> str:
    """
    根據指定狗狗品種，
    取得一張隨機圖片網址。
    """

    data = get_json(
        f"{BASE_URL}/breed/{breed}/images/random"
    )

    return data["message"]


### 整理狗狗品種資料
def flatten_breeds(breeds: dict) -> list[str]:
    """
    將 Dog CEO API 的品種 dict，
    整理成 Streamlit 下拉選單可以使用的 list。

    這個版本只顯示主品種，
    不另外展開子品種。
    """

    return sorted(
        breeds.keys() # 取得 dict 裡所有主品種名稱並排序
    )


### 建立狗狗圖片牆函式
def show_image_grid(
    image_urls: list[str],
    columns_count: int = 3
) -> None:
    """
    根據指定欄位數量建立 Streamlit columns，
    並將狗狗圖片平均排列到不同欄位。
    """

    columns = st.columns(
        columns_count
    )

    for index, image_url in enumerate(image_urls):

        # 使用餘數決定目前這張圖片要放在哪一欄
        column = columns[
            index % columns_count
        ]

        with column:

            st.image(
                image_url,
                width="stretch" # 圖片寬度自動填滿目前欄位
            )

            st.caption(
                f"Dog #{index + 1}" # 顯示圖片編號
            )


### 顯示網站標題
st.markdown(
    "<div class='main-title'>🐶 Dog CEO 狗狗圖片牆</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    用 REST API 打造一個超療癒的狗狗圖片展示網站。
    </div>
    """,
    unsafe_allow_html=True
)


### 主程式
try:

    ### 取得所有狗狗品種
    breeds = get_all_breeds()

    breed_options = flatten_breeds(
        breeds
    )


    ### 建立 Sidebar 查詢設定
    with st.sidebar:

        st.header(
            "🐶 查詢設定"
        )

        mode = st.radio(
            "選擇模式",
            [
                "隨機圖片牆",
                "指定品種",
                "今日狗狗抽卡",
                "品種資料表"
            ]
        )

        image_count = st.slider(
            "圖片數量",
            min_value=3, # 最少顯示 3 張
            max_value=50, # 最多顯示 50 張
            value=9, # 預設顯示 9 張
            step=1
        )


        ### 設定預設狗狗品種
        default_index = 0 # 找不到 shiba 時預設選擇第一個品種

        if "shiba" in breed_options:
            default_index = breed_options.index(
                "shiba"
            ) # 找到 shiba 在品種清單中的索引位置


        selected_breed = st.selectbox(
            "選擇狗狗品種",
            breed_options,
            index=default_index
        )

        columns_count = st.slider(
            "每列顯示幾張",
            min_value=2,
            max_value=5,
            value=3
        )

        run_button = st.button(
            "🐾 開始產生",
            type="primary",
            width="stretch"
        )

        st.divider()

        st.caption(
            "建議查詢：shiba、pug、husky、retriever、terrier"
        )


    ### 顯示網站統計資訊
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric(
        "API 主題",
        "狗狗圖片"
    )

    metric_col2.metric(
        "可選品種",
        len(breed_options) # 計算目前 API 提供多少個主品種
    )

    metric_col3.metric(
        "最多隨機張數",
        "50 張"
    )

    st.divider()


    ### 模式 1：隨機圖片牆
    if mode == "隨機圖片牆":

        st.subheader(
            "🎲 隨機狗狗圖片牆"
        )


        ### 取得隨機狗狗圖片
        if run_button:

            with st.spinner(
                "正在召喚狗狗..."
            ):

                image_urls = get_random_images(
                    image_count
                ) # 根據 Sidebar 選擇的圖片數量取得圖片

        else:

            image_urls = get_random_images(
                9
            ) # 第一次開啟網站時預設顯示 9 張圖片


        ### 顯示狗狗圖片牆
        show_image_grid(
            image_urls,
            columns_count
        )


        ### 建立圖片網址 DataFrame
        df = pd.DataFrame(
            {
                "編號": range(
                    1,
                    len(image_urls) + 1
                ),
                "圖片網址": image_urls
            }
        )


        ### 將 DataFrame 轉成 CSV
        csv_data = df.to_csv(
            index=False # CSV 不加入 DataFrame index
        ).encode(
            "utf-8-sig" # 使用 UTF-8 BOM，避免 Excel 開啟中文時出現亂碼
        )


        ### 提供 CSV 下載按鈕
        st.download_button(
            label="📥 下載圖片網址 CSV",
            data=csv_data,
            file_name="dog_image_urls.csv",
            mime="text/csv"
        )


    ### 模式 2：指定品種
    elif mode == "指定品種":

        st.subheader(
            f"🐕 指定品種：{selected_breed}"
        )


        ### 設定要取得的圖片數量
        if run_button:

            count = image_count # 按下按鈕後使用 Sidebar 選擇的圖片數量

        else:

            count = 6 # 第一次進入這個模式時預設顯示 6 張


        ### 取得指定品種圖片
        with st.spinner(
            f"正在尋找 {selected_breed}..."
        ):

            image_urls = get_breed_random_images(
                selected_breed,
                count
            )


        st.success(
            f"已取得 {count} 張 {selected_breed} 圖片"
        )


        ### 顯示指定品種圖片牆
        show_image_grid(
            image_urls,
            columns_count
        )


        ### 建立指定品種圖片 DataFrame
        df = pd.DataFrame(
            {
                "品種": [
                    selected_breed
                ] * len(image_urls), # 每一筆圖片資料都填入相同品種名稱

                "圖片網址":
                    image_urls
            }
        )


        ### 將 DataFrame 轉成 CSV
        csv_data = df.to_csv(
            index=False
        ).encode(
            "utf-8-sig"
        )


        ### 提供 CSV 下載按鈕
        st.download_button(
            label="📥 下載圖片網址 CSV",
            data=csv_data,
            file_name=f"{selected_breed}_images.csv",
            mime="text/csv"
        )


    ### 模式 3：今日狗狗抽卡
    elif mode == "今日狗狗抽卡":

        st.subheader(
            "✨ 今日狗狗抽卡"
        )


        ### 建立 Session State 儲存抽卡結果
        # Streamlit 每次操作元件都會重新執行程式
        # 因此使用 session_state 保存目前抽到的狗狗，避免每次重新執行都自動換卡
        if "lucky_breed" not in st.session_state:

            st.session_state.lucky_breed = random.choice(
                breed_options
            ) # 第一次進入頁面時隨機選擇一個品種

            st.session_state.lucky_image = (
                get_breed_random_image(
                    st.session_state.lucky_breed
                )
            ) # 根據抽到的品種取得一張隨機圖片


        ### 按下按鈕重新抽卡
        if run_button:

            st.session_state.lucky_breed = random.choice(
                breed_options
            )

            st.session_state.lucky_image = (
                get_breed_random_image(
                    st.session_state.lucky_breed
                )
            )


        ### 取得目前 Session State 中的抽卡結果
        lucky_breed = (
            st.session_state.lucky_breed
        )

        lucky_image = (
            st.session_state.lucky_image
        )


        ### 今日狗狗隨機評語
        comments = [
            "今天適合放慢速度，像狗狗曬太陽一樣。",
            "今天的任務是：不要把自己逼太緊。",
            "你今天的幸運值很高，適合開始一個小專案。",
            "這張狗狗提醒你：debug 也是人生的一部分。",
            "今天適合寫程式，也適合看狗。"
        ]


        ### 建立抽卡結果左右兩欄
        card_col1, card_col2 = st.columns(
            [1, 2] # 左欄寬度 1、右欄寬度 2
        )


        ### 左側顯示狗狗圖片
        with card_col1:

            st.markdown(
                "<div class='dog-card'>",
                unsafe_allow_html=True
            )

            st.image(
                lucky_image,
                width="stretch"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        ### 右側顯示抽卡資訊
        with card_col2:

            st.markdown(
                "### 你的今日狗狗"
            )

            st.markdown(
                f"""
                <div class='big-number'>
                {lucky_breed.upper()}
                </div>
                """,
                unsafe_allow_html=True
            ) # 將抽到的狗狗品種轉成大寫顯示

            st.write(
                random.choice(
                    comments
                )
            ) # 隨機顯示一句今日評語

            st.info(
                "這個功能可以拿來教學生："
                "API 不只能查資料，"
                "還可以搭配隨機邏輯，"
                "做成有互動感的小作品。"
            )

            st.markdown(
                "#### 圖片網址"
            )

            st.code(
                lucky_image
            ) # 顯示目前狗狗圖片的原始網址


    ### 模式 4：品種資料表
    elif mode == "品種資料表":

        st.subheader(
            "📋 Dog CEO 品種資料表"
        )


        ### 建立品種資料 list
        rows = []

        for breed, sub_breeds in breeds.items():

            rows.append(
                {
                    "主品種": breed,

                    "是否有子品種":
                        "是"
                        if sub_breeds
                        else "否",

                    "子品種":
                        ", ".join(sub_breeds)
                        if sub_breeds
                        else "無"
                }
            )


        ### 將品種資料轉成 DataFrame
        df = pd.DataFrame(
            rows
        )


        ### 顯示品種資料表
        st.dataframe(
            df,
            width="stretch", # 表格寬度自動填滿頁面
            height=520 # 設定表格高度
        )


        ### 將品種資料轉成 CSV
        csv_data = df.to_csv(
            index=False
        ).encode(
            "utf-8-sig"
        )


        ### 提供 CSV 下載按鈕
        st.download_button(
            label="📥 下載品種資料 CSV",
            data=csv_data,
            file_name="dog_breeds.csv",
            mime="text/csv"
        )


### 處理 API 連線錯誤
except requests.RequestException as error:

    st.error(
        f"API 連線失敗：{error}"
    )


### 處理其他程式錯誤
except Exception as error:

    st.error(
        f"程式發生錯誤：{error}"
    )
```
