TVMaze 提供免費 REST API，根網址是 https://api.tvmaze.com，回傳 JSON，可查影集、集數、演員、播出表等資料。

```
# API網址
https://api.tvmaze.com/search/shows?q=影集名稱
```

### 範例：終端機版 TVMaze 影集查詢器

```python
"""
範例：TVMaze API 終端機影集查詢器

功能：
1. 輸入影集關鍵字
2. 列出搜尋結果
3. 選擇一部影集
4. 顯示基本資料、類型、評分、官方網站、摘要
5. 詢問是否用瀏覽器開啟官方網站或圖片

執行方式：
uv run python tvmaze_cli_explorer.py
"""

import re
import webbrowser

import requests


BASE_URL = "https://api.tvmaze.com"


def clean_html(raw_text: str | None) -> str:
    """TVMaze 的 summary 會帶 HTML 標籤，這裡把標籤拿掉。"""
    if not raw_text:
        return "無摘要資料"

    return re.sub(r"<.*?>", "", raw_text)


def get_json(url: str, params: dict | None = None) -> list | dict:
    """送出 GET 請求，並把回傳資料轉成 Python 物件。"""
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def search_shows(keyword: str) -> list[dict]:
    """搜尋影集。"""
    return get_json(f"{BASE_URL}/search/shows", {"q": keyword})


def show_search_results(results: list[dict]) -> None:
    """列出搜尋結果，讓使用者選。"""
    print("\n=== 搜尋結果 ===")

    for index, item in enumerate(results, start=1):
        show = item["show"]

        name = show.get("name", "無名稱")
        language = show.get("language", "無語言")
        genres = ", ".join(show.get("genres", [])) or "無類型"
        rating = show.get("rating", {}).get("average") or "無評分"

        print(f"{index}. {name}｜語言：{language}｜類型：{genres}｜評分：{rating}")


def show_detail(show: dict) -> None:
    """顯示單一影集詳細資料。"""
    image_url = None

    if show.get("image"):
        image_url = show["image"].get("original") or show["image"].get("medium")

    official_site = show.get("officialSite")
    summary = clean_html(show.get("summary"))

    print("\n" + "=" * 60)
    print("影集詳細資料")
    print("=" * 60)
    print(f"名稱：{show.get('name')}")
    print(f"狀態：{show.get('status')}")
    print(f"語言：{show.get('language')}")
    print(f"類型：{', '.join(show.get('genres', [])) or '無資料'}")
    print(f"首播日期：{show.get('premiered')}")
    print(f"結束日期：{show.get('ended')}")
    print(f"平均片長：{show.get('averageRuntime')} 分鐘")
    print(f"評分：{show.get('rating', {}).get('average') or '無評分'}")
    print(f"官方網站：{official_site or '無資料'}")
    print(f"圖片網址：{image_url or '無資料'}")

    print("\n摘要：")
    print(summary)

    if official_site:
        answer = input("\n是否要開啟官方網站？(y/n)：").strip().lower()
        if answer == "y":
            webbrowser.open(official_site)

    if image_url:
        answer = input("是否要開啟影集海報圖片？(y/n)：").strip().lower()
        if answer == "y":
            webbrowser.open(image_url)


def main() -> None:
    print("=== TVMaze 影集查詢器 ===")
    print("可輸入：friends、breaking bad、stranger things、dark")

    keyword = input("\n請輸入影集關鍵字：").strip()

    if not keyword:
        print("請輸入關鍵字。")
        return

    try:
        results = search_shows(keyword)

        if not results:
            print("查無影集資料。")
            return

        show_search_results(results)

        choice = int(input("\n請選擇要查看的影集編號："))

        if choice < 1 or choice > len(results):
            print("編號超出範圍。")
            return

        selected_show = results[choice - 1]["show"]
        show_detail(selected_show)

    except ValueError:
        print("請輸入正確的數字。")

    except requests.RequestException as error:
        print("API 連線失敗：", error)


if __name__ == "__main__":
    main()
```

### 範例：Streamlit 高吸睛影集搜尋儀表板

```python
"""
範例：TVMaze API Streamlit 影集搜尋儀表板

功能：
1. 搜尋影集
2. 海報卡片牆
3. 評分排行
4. 類型統計
5. 影集詳細資料
6. 匯出搜尋結果 CSV

執行方式：
uv run streamlit run tvmaze_streamlit_dashboard.py
"""

import re

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


### API 設定
BASE_URL = "https://api.tvmaze.com" # TVMaze API 的基礎網址


### Streamlit 頁面設定
st.set_page_config(
    page_title="TVMaze 影集搜尋儀表板", # 瀏覽器分頁標題
    page_icon="🎬", # 瀏覽器分頁圖示
    layout="wide" # 使用寬版頁面
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
        color: #8b8b8b;
        font-size: 18px;
        margin-bottom: 26px;
    }

    .show-card {
        padding: 18px;
        border-radius: 24px;
        background: linear-gradient(135deg, #111827, #1f2937);
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.22);
        min-height: 170px;
        margin-bottom: 18px;
    }

    .show-name {
        color: #ffffff;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .pill {
        display: inline-block;
        padding: 5px 12px;
        margin: 4px 4px 4px 0px;
        border-radius: 999px;
        background: #f97316;
        color: white;
        font-size: 13px;
        font-weight: 700;
    }

    .small-note {
        color: #d1d5db;
        font-size: 14px;
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True
)


### 清除 HTML 標籤
def clean_html(raw_text: str | None) -> str:
    """
    清除 TVMaze summary 裡面的 HTML 標籤，
    只保留純文字摘要。
    """

    if not raw_text:
        return "目前沒有摘要資料。"

    return re.sub(
        r"<.*?>",
        "",
        raw_text
    )


### 建立 API GET Request 函式
@st.cache_data(show_spinner=False)
def get_json(
    url: str,
    params: dict | None = None
) -> list | dict:
    """
    向指定 API 網址發送 GET Request，
    並將 JSON Response 轉成 Python 物件。
    """

    response = requests.get(
        url,
        params=params,
        timeout=10 # API 最多等待 10 秒
    )

    response.raise_for_status() # HTTP 狀態碼不是成功狀態時產生例外

    return response.json()


### 搜尋影集
@st.cache_data(show_spinner=False)
def search_shows(keyword: str) -> list[dict]:
    """
    根據使用者輸入的關鍵字，
    呼叫 TVMaze Search API 搜尋影集。
    """

    keyword = keyword.strip() # 移除關鍵字前後空白

    return get_json(
        f"{BASE_URL}/search/shows",
        {
            "q": keyword
        }
    )


### 整理影集搜尋結果
def parse_results(
    results: list[dict]
) -> pd.DataFrame:
    """
    將 TVMaze API 搜尋結果，
    整理成 Pandas DataFrame。
    """

    rows = []

    for item in results:

        show = item["show"] # 取得目前這筆搜尋結果中的影集資料


        ### 取得海報圖片
        image_url = None

        if show.get("image"):

            image_url = show["image"].get(
                "medium"
            )


        ### 取得評分
        rating = (
            show
            .get("rating", {})
            .get("average")
        )


        ### 建立影集資料
        rows.append(
            {
                "名稱":
                    show.get("name"),

                "語言":
                    show.get("language"),

                "狀態":
                    show.get("status"),

                "類型":
                    ", ".join(
                        show.get(
                            "genres",
                            []
                        )
                    )
                    or "無資料",

                "首播日期":
                    show.get("premiered"),

                "結束日期":
                    show.get("ended"),

                "平均片長":
                    show.get("averageRuntime"),

                "評分":
                    rating,

                "官方網站":
                    show.get("officialSite"),

                "圖片網址":
                    image_url,

                "摘要":
                    clean_html(
                        show.get("summary")
                    )
            }
        )

    return pd.DataFrame(
        rows
    )


### 顯示影集卡片牆
def render_show_cards(
    df: pd.DataFrame
) -> None:
    """
    使用 Streamlit columns，
    將影集搜尋結果顯示成三欄卡片牆。
    """

    columns = st.columns(
        3
    )

    for index, (_, row) in enumerate(
        df.iterrows()
    ):

        column = columns[
            index % 3
        ] # 使用餘數決定目前卡片要放在哪一欄


        with column:

            ### 顯示海報
            if pd.notna(row["圖片網址"]):

                st.image(
                    row["圖片網址"],
                    width="stretch"
                )

            else:

                st.info(
                    "此影集沒有海報圖片。"
                )


            ### 建立類型標籤
            genres_html = ""

            if row["類型"] != "無資料":

                for genre in row["類型"].split(
                    ", "
                ):

                    genres_html += (
                        f"<span class='pill'>"
                        f"{genre}"
                        f"</span>"
                    )


            ### 處理評分文字
            rating_text = (
                row["評分"]
                if pd.notna(row["評分"])
                else "無評分"
            )


            ### 顯示影集卡片
            st.markdown(
                f"""
<div class="show-card">
    <div class="show-name">{row["名稱"]}</div>
    <div class="small-note">
        語言：{row["語言"] or "無資料"}<br>
        狀態：{row["狀態"] or "無資料"}<br>
        評分：{rating_text}
    </div>
    <div style="margin-top:10px;">
        {genres_html}
    </div>
</div>
""",
                unsafe_allow_html=True
            )


### 建立評分排行圖
def render_rating_chart(
    df: pd.DataFrame
) -> None:
    """
    取得有評分的影集，
    並顯示評分最高的前 10 筆資料。
    """

    chart_df = (
        df
        .dropna(
            subset=[
                "評分"
            ]
        )
        .copy()
    )


    ### 沒有評分資料時停止繪圖
    if chart_df.empty:

        st.warning(
            "這次搜尋結果沒有足夠評分資料。"
        )

        return


    ### 取得評分最高的前 10 筆
    chart_df = (
        chart_df
        .sort_values(
            "評分",
            ascending=True
        )
        .tail(10)
    )


    ### 建立橫向長條圖
    fig = px.bar(
        chart_df,
        x="評分",
        y="名稱",
        orientation="h",
        text="評分",
        color="評分",
        title="搜尋結果評分排行 Top 10",
        color_continuous_scale="Oranges"
    )


    fig.update_traces(
        textposition="outside"
    )


    fig.update_layout(
        height=480,
        coloraxis_showscale=False
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


### 建立影集類型統計圖
def render_genre_chart(
    df: pd.DataFrame
) -> None:
    """
    統計搜尋結果中不同影集類型出現的次數，
    並使用圓餅圖顯示類型分布。
    """

    genres = []


    ### 將所有類型拆成單獨資料
    for value in df["類型"].dropna():

        if value == "無資料":
            continue

        genres.extend(
            value.split(
                ", "
            )
        )


    ### 沒有類型資料時停止繪圖
    if not genres:

        st.warning(
            "這次搜尋結果沒有類型資料。"
        )

        return


    ### 建立類型 DataFrame
    genre_df = pd.DataFrame(
        {
            "類型":
                genres
        }
    )


    ### 統計每個類型出現次數
    count_df = (
        genre_df
        .value_counts(
            "類型"
        )
        .reset_index(
            name="數量"
        )
    )


    ### 建立圓餅圖
    fig = px.pie(
        count_df,
        names="類型",
        values="數量",
        title="影集類型分布",
        hole=0.35
    )


    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


### 顯示網站標題
st.markdown(
    "<div class='main-title'>🎬 TVMaze 影集搜尋儀表板</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
輸入影集關鍵字，把 REST API 回傳資料變成可搜尋、可視覺化、可下載的小作品。
</div>
""",
    unsafe_allow_html=True
)


### Sidebar 查詢設定
with st.sidebar:

    st.header(
        "🔍 搜尋設定"
    )


    keyword = st.text_input(
        "影集關鍵字",
        value="friends",
        placeholder="例如 friends、dark、suits、breaking bad"
    )


    min_rating = st.slider(
        "最低評分",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.5
    )


    status_filter = st.multiselect(
        "影集狀態",
        [
            "Running",
            "Ended",
            "To Be Determined",
            "In Development"
        ],
        default=[]
    )


    search_button = st.button(
        "🎬 開始搜尋",
        type="primary",
        width="stretch"
    )


    st.divider()


    st.caption(
        "推薦關鍵字：friends、dark、love、doctor、school、crime"
    )


### 建立 Session State
# Streamlit 每次操作元件時都會重新執行整份程式
# 使用 session_state 保存目前真正要搜尋的關鍵字
if "search_keyword" not in st.session_state:

    st.session_state.search_keyword = (
        "friends"
    )


### 按下搜尋按鈕後更新關鍵字
if search_button:

    if keyword.strip():

        st.session_state.search_keyword = (
            keyword.strip()
        )


### 取得目前搜尋關鍵字
search_keyword = (
    st.session_state.search_keyword
)


### 主程式
try:

    ### 呼叫 TVMaze API
    with st.spinner(
        f"正在搜尋 {search_keyword}..."
    ):

        results = search_shows(
            search_keyword
        )


    ### 查無搜尋結果
    if not results:

        st.error(
            "查無資料，請換一個關鍵字。"
        )

        st.stop()


    ### 將 API 搜尋結果整理成 DataFrame
    df = parse_results(
        results
    )


    ### 最低評分篩選
    if min_rating > 0:

        df = df[
            df["評分"]
            .fillna(0)
            >= min_rating
        ]


    ### 影集狀態篩選
    if status_filter:

        df = df[
            df["狀態"]
            .isin(
                status_filter
            )
        ]


    ### 篩選後沒有資料
    if df.empty:

        st.warning(
            "篩選後沒有資料，請降低評分或取消狀態篩選。"
        )

        st.stop()


    ### 顯示搜尋關鍵字
    st.caption(
        f"目前搜尋：{search_keyword}"
    )


    ### 統計資訊
    metric_col1, metric_col2, metric_col3, metric_col4 = (
        st.columns(4)
    )


    metric_col1.metric(
        "搜尋結果",
        len(df)
    )


    metric_col2.metric(
        "有評分資料",
        int(
            df["評分"]
            .notna()
            .sum()
        )
    )


    metric_col3.metric(
        "有海報圖片",
        int(
            df["圖片網址"]
            .notna()
            .sum()
        )
    )


    ### 計算最高評分
    if df["評分"].notna().any():

        highest_rating = (
            df["評分"]
            .max()
        )

    else:

        highest_rating = "無"


    metric_col4.metric(
        "最高評分",
        highest_rating
    )


    st.divider()


    ### 建立功能分頁
    tab1, tab2, tab3, tab4, tab5 = (
        st.tabs(
            [
                "🎞️ 海報卡片牆",
                "⭐ 評分排行",
                "🍿 類型分析",
                "📋 資料表",
                "🔎 詳細資料"
            ]
        )
    )


    ### Tab 1：海報卡片牆
    with tab1:

        st.subheader(
            "🔥 影集海報卡片牆"
        )

        render_show_cards(
            df
        )


    ### Tab 2：評分排行
    with tab2:

        st.subheader(
            "⭐ 評分排行"
        )

        render_rating_chart(
            df
        )


    ### Tab 3：類型分析
    with tab3:

        st.subheader(
            "🍿 類型分析"
        )

        render_genre_chart(
            df
        )


    ### Tab 4：搜尋結果資料表
    with tab4:

        st.subheader(
            "📋 搜尋結果資料表"
        )


        ### 選擇要顯示的欄位
        table_df = df[
            [
                "名稱",
                "語言",
                "狀態",
                "類型",
                "首播日期",
                "平均片長",
                "評分",
                "官方網站"
            ]
        ]


        ### 顯示資料表
        st.dataframe(
            table_df,
            width="stretch",
            height=520,
            hide_index=True
        )


        ### 將 DataFrame 轉成 CSV
        csv_data = df.to_csv(
            index=False
        ).encode(
            "utf-8-sig"
        )


        ### 建立 CSV 下載按鈕
        st.download_button(
            label="📥 下載搜尋結果 CSV",
            data=csv_data,
            file_name="tvmaze_search_results.csv",
            mime="text/csv"
        )


    ### Tab 5：單部影集詳細資料
    with tab5:

        st.subheader(
            "🔎 單部影集詳細資料"
        )


        ### 選擇影集
        selected_name = st.selectbox(
            "選擇影集",
            df["名稱"].tolist()
        )


        ### 取得目前選擇的影集
        selected_row = (
            df[
                df["名稱"]
                == selected_name
            ]
            .iloc[0]
        )


        ### 建立左右兩欄
        detail_col1, detail_col2 = (
            st.columns(
                [1, 2]
            )
        )


        ### 左側顯示海報
        with detail_col1:

            if pd.notna(
                selected_row["圖片網址"]
            ):

                st.image(
                    selected_row["圖片網址"],
                    width="stretch"
                )

            else:

                st.info(
                    "這部影集沒有海報圖片。"
                )


        ### 右側顯示詳細資料
        with detail_col2:

            st.markdown(
                f"## {selected_row['名稱']}"
            )


            st.write(
                f"狀態："
                f"{selected_row['狀態'] or '無資料'}"
            )


            st.write(
                f"語言："
                f"{selected_row['語言'] or '無資料'}"
            )


            st.write(
                f"類型："
                f"{selected_row['類型']}"
            )


            st.write(
                f"首播日期："
                f"{selected_row['首播日期'] or '無資料'}"
            )


            ### 處理平均片長
            runtime = (
                selected_row["平均片長"]
                if pd.notna(
                    selected_row["平均片長"]
                )
                else "無資料"
            )


            st.write(
                f"平均片長：{runtime}"
                + (
                    " 分鐘"
                    if runtime != "無資料"
                    else ""
                )
            )


            ### 處理評分
            selected_rating = (
                selected_row["評分"]
                if pd.notna(
                    selected_row["評分"]
                )
                else "無評分"
            )


            st.write(
                f"評分：{selected_rating}"
            )


            ### 官方網站
            if pd.notna(
                selected_row["官方網站"]
            ):

                st.link_button(
                    "🌐 前往官方網站",
                    selected_row["官方網站"]
                )


            ### 顯示影集摘要
            st.markdown(
                "### 摘要"
            )

            st.write(
                selected_row["摘要"]
            )


### API 連線錯誤
except requests.RequestException as error:

    st.error(
        f"API 連線失敗：{error}"
    )


### 其他程式錯誤
except Exception as error:

    st.error(
        f"程式發生錯誤：{error}"
    )
```
