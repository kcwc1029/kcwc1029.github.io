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


BASE_URL = "https://api.tvmaze.com"


st.set_page_config(
    page_title="TVMaze 影集搜尋儀表板",
    page_icon="🎬",
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
    }
    </style>
    """,
    unsafe_allow_html=True
)


def clean_html(raw_text: str | None) -> str:
    """清掉 TVMaze summary 裡面的 HTML 標籤。"""
    if not raw_text:
        return "目前沒有摘要資料。"

    return re.sub(r"<.*?>", "", raw_text)


@st.cache_data(show_spinner=False)
def get_json(url: str, params: dict | None = None) -> list | dict:
    """取得 API JSON 資料。"""
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(show_spinner=False)
def search_shows(keyword: str) -> list[dict]:
    """搜尋影集。"""
    return get_json(f"{BASE_URL}/search/shows", {"q": keyword})


def parse_results(results: list[dict]) -> pd.DataFrame:
    """把 TVMaze 搜尋結果整理成表格。"""
    rows = []

    for item in results:
        show = item["show"]

        image_url = None
        if show.get("image"):
            image_url = show["image"].get("medium")

        rows.append({
            "名稱": show.get("name"),
            "語言": show.get("language"),
            "狀態": show.get("status"),
            "類型": ", ".join(show.get("genres", [])) or "無資料",
            "首播日期": show.get("premiered"),
            "結束日期": show.get("ended"),
            "平均片長": show.get("averageRuntime"),
            "評分": show.get("rating", {}).get("average"),
            "官方網站": show.get("officialSite"),
            "圖片網址": image_url,
            "摘要": clean_html(show.get("summary"))
        })

    return pd.DataFrame(rows)


def render_show_cards(df: pd.DataFrame) -> None:
    """顯示影集卡片牆。"""
    columns = st.columns(3)

    for index, row in df.iterrows():
        with columns[index % 3]:
            if row["圖片網址"]:
                st.image(row["圖片網址"], use_container_width=True)

            genres_html = ""

            if row["類型"] != "無資料":
                for genre in row["類型"].split(", "):
                    genres_html += f"<span class='pill'>{genre}</span>"

            st.markdown(
                f"""
                <div class="show-card">
                    <div class="show-name">{row["名稱"]}</div>
                    <div class="small-note">
                        語言：{row["語言"] or "無資料"}｜
                        狀態：{row["狀態"] or "無資料"}｜
                        評分：{row["評分"] or "無評分"}
                    </div>
                    <div style="margin-top:10px;">{genres_html}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_rating_chart(df: pd.DataFrame) -> None:
    """顯示評分排行圖。"""
    chart_df = df.dropna(subset=["評分"]).copy()

    if chart_df.empty:
        st.warning("這次搜尋結果沒有足夠評分資料。")
        return

    chart_df = chart_df.sort_values("評分", ascending=True).tail(10)

    fig = px.bar(
        chart_df,
        x="評分",
        y="名稱",
        orientation="h",
        text="評分",
        title="搜尋結果評分排行 Top 10"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(height=480)

    st.plotly_chart(fig, use_container_width=True)


def render_genre_chart(df: pd.DataFrame) -> None:
    """統計搜尋結果中出現的影集類型。"""
    genres = []

    for value in df["類型"].dropna():
        if value == "無資料":
            continue

        genres.extend(value.split(", "))

    if not genres:
        st.warning("這次搜尋結果沒有類型資料。")
        return

    genre_df = pd.DataFrame({"類型": genres})
    count_df = genre_df.value_counts("類型").reset_index(name="數量")

    fig = px.pie(
        count_df,
        names="類型",
        values="數量",
        title="影集類型分布"
    )

    st.plotly_chart(fig, use_container_width=True)


st.markdown("<div class='main-title'>🎬 TVMaze 影集搜尋儀表板</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>輸入影集關鍵字，把 REST API 回傳資料變成可搜尋、可視覺化、可下載的小作品。</div>",
    unsafe_allow_html=True
)


with st.sidebar:
    st.header("搜尋設定")

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
        ["Running", "Ended", "To Be Determined", "In Development"],
        default=[]
    )

    search_button = st.button("開始搜尋", type="primary", use_container_width=True)

    st.divider()
    st.caption("推薦關鍵字：friends、dark、love、doctor、school、crime")


if search_button or keyword:
    try:
        results = search_shows(keyword)

        if not results:
            st.error("查無資料，請換一個關鍵字。")
            st.stop()

        df = parse_results(results)

        if min_rating > 0:
            df = df[df["評分"].fillna(0) >= min_rating]

        if status_filter:
            df = df[df["狀態"].isin(status_filter)]

        if df.empty:
            st.warning("篩選後沒有資料，請降低評分或取消狀態篩選。")
            st.stop()

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        metric_col1.metric("搜尋結果", len(df))
        metric_col2.metric("有評分資料", int(df["評分"].notna().sum()))
        metric_col3.metric("有海報圖片", int(df["圖片網址"].notna().sum()))
        metric_col4.metric("最高評分", df["評分"].max() if df["評分"].notna().any() else "無")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["海報卡片牆", "評分排行", "類型分析", "資料表", "詳細資料"]
        )

        with tab1:
            st.subheader("🔥 影集海報卡片牆")
            render_show_cards(df)

        with tab2:
            st.subheader("⭐ 評分排行")
            render_rating_chart(df)

        with tab3:
            st.subheader("🍿 類型分析")
            render_genre_chart(df)

        with tab4:
            st.subheader("📋 搜尋結果資料表")

            st.dataframe(
                df[
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
                ],
                use_container_width=True,
                height=520
            )

            csv_data = df.to_csv(index=False).encode("utf-8-sig")

            st.download_button(
                "下載搜尋結果 CSV",
                data=csv_data,
                file_name="tvmaze_search_results.csv",
                mime="text/csv"
            )

        with tab5:
            st.subheader("🔎 單部影集詳細資料")

            selected_name = st.selectbox(
                "選擇影集",
                df["名稱"].tolist()
            )

            selected_row = df[df["名稱"] == selected_name].iloc[0]

            detail_col1, detail_col2 = st.columns([1, 2])

            with detail_col1:
                if selected_row["圖片網址"]:
                    st.image(selected_row["圖片網址"], use_container_width=True)
                else:
                    st.info("這部影集沒有海報圖片。")

            with detail_col2:
                st.markdown(f"## {selected_row['名稱']}")
                st.write(f"狀態：{selected_row['狀態']}")
                st.write(f"語言：{selected_row['語言']}")
                st.write(f"類型：{selected_row['類型']}")
                st.write(f"首播日期：{selected_row['首播日期']}")
                st.write(f"平均片長：{selected_row['平均片長']} 分鐘")
                st.write(f"評分：{selected_row['評分'] or '無評分'}")

                if selected_row["官方網站"]:
                    st.link_button("前往官方網站", selected_row["官方網站"])

                st.markdown("### 摘要")
                st.write(selected_row["摘要"])

    except requests.RequestException as error:
        st.error(f"API 連線失敗：{error}")
```
