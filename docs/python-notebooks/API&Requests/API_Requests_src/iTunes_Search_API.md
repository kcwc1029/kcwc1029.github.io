### 基於Streamlit實作iTunes Search API 音樂搜尋儀表板

```py
import requests
import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# iTunes Search API
# =========================================================

BASE_URL = "https://itunes.apple.com/search"


# =========================================================
# Streamlit 頁面設定
# =========================================================

st.set_page_config(
    page_title="iTunes 音樂搜尋儀表板",
    page_icon="🎵",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 46px;
        font-weight: 900;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #888;
        margin-bottom: 28px;
    }

    .song-card {
        padding: 20px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            rgba(255, 80, 100, 0.12),
            rgba(255,255,255,0.04)
        );
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 18px;
    }

    .song-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .artist-name {
        font-size: 16px;
        color: #aaa;
        margin-bottom: 8px;
    }

    .small-note {
        font-size: 14px;
        color: #888;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# API Request
# =========================================================

@st.cache_data(show_spinner=False)
def search_music(
    keyword: str,
    limit: int = 30,
    country: str = "TW"
) -> list[dict]:

    """
    使用 iTunes Search API 搜尋歌曲。
    """

    params = {
        "term": keyword,
        "media": "music",
        "entity": "song",
        "limit": limit,
        "country": country
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "results",
        []
    )


# =========================================================
# 整理 DataFrame
# =========================================================

def build_music_df(
    songs: list[dict]
) -> pd.DataFrame:

    """
    將 API JSON 整理成 Pandas DataFrame。
    """

    rows = []

    for song in songs:

        release_date = song.get(
            "releaseDate",
            ""
        )

        year = None

        if release_date:

            try:
                year = int(
                    release_date[:4]
                )

            except ValueError:
                year = None


        rows.append(
            {
                "歌曲名稱":
                    song.get(
                        "trackName",
                        "無資料"
                    ),

                "歌手":
                    song.get(
                        "artistName",
                        "無資料"
                    ),

                "專輯":
                    song.get(
                        "collectionName",
                        "無資料"
                    ),

                "年份":
                    year,

                "曲風":
                    song.get(
                        "primaryGenreName",
                        "無資料"
                    ),

                "價格":
                    song.get(
                        "trackPrice"
                    ),

                "幣別":
                    song.get(
                        "currency",
                        ""
                    ),

                "封面":
                    song.get(
                        "artworkUrl100"
                    ),

                "試聽網址":
                    song.get(
                        "previewUrl"
                    ),

                "iTunes網址":
                    song.get(
                        "trackViewUrl"
                    )
            }
        )


    return pd.DataFrame(
        rows
    )


# =========================================================
# 發行年份圖
# =========================================================

def render_year_chart(
    music_df: pd.DataFrame
) -> None:

    """
    統計搜尋結果中不同年份的歌曲數量。
    """

    chart_df = (
        music_df
        .dropna(
            subset=["年份"]
        )
        .groupby(
            "年份"
        )
        .size()
        .reset_index(
            name="歌曲數量"
        )
    )


    if chart_df.empty:

        st.info(
            "目前沒有足夠的年份資料可以畫圖。"
        )

        return


    chart_df["年份"] = (
        chart_df["年份"]
        .astype(int)
    )


    fig = px.bar(
        chart_df,
        x="年份",
        y="歌曲數量",
        text="歌曲數量",
        title="搜尋結果的發行年份分布"
    )


    fig.update_traces(
        textposition="outside"
    )


    fig.update_layout(
        height=450,
        xaxis_title="年份",
        yaxis_title="歌曲數量"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


# =========================================================
# 顯示歌曲卡片
# =========================================================

def show_song_cards(
    songs: list[dict],
    max_cards: int = 12
) -> None:

    """
    顯示歌曲封面、名稱、專輯與試聽。
    """

    display_songs = songs[
        :max_cards
    ]


    for index in range(
        0,
        len(display_songs),
        3
    ):

        columns = st.columns(3)


        row_songs = display_songs[
            index:index + 3
        ]


        for column, song in zip(
            columns,
            row_songs
        ):

            with column:

                st.markdown(
                    "<div class='song-card'>",
                    unsafe_allow_html=True
                )


                artwork = song.get(
                    "artworkUrl100"
                )


                # 將 100x100 封面換成較大尺寸
                if artwork:

                    artwork = artwork.replace(
                        "100x100",
                        "600x600"
                    )


                    st.image(
                        artwork,
                        width="stretch"
                    )


                track_name = song.get(
                    "trackName",
                    "無資料"
                )


                artist_name = song.get(
                    "artistName",
                    "無資料"
                )


                album_name = song.get(
                    "collectionName",
                    "無資料"
                )


                genre = song.get(
                    "primaryGenreName",
                    "無資料"
                )


                release_date = song.get(
                    "releaseDate",
                    ""
                )


                year = (
                    release_date[:4]
                    if release_date
                    else "無資料"
                )


                st.markdown(
                    f"""
                    <div class="song-title">
                    🎵 {track_name}
                    </div>

                    <div class="artist-name">
                    🎤 {artist_name}
                    </div>

                    <div class="small-note">
                    💿 {album_name}<br>
                    📅 {year}<br>
                    🎼 {genre}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                preview_url = song.get(
                    "previewUrl"
                )


                if preview_url:

                    st.audio(
                        preview_url
                    )

                else:

                    st.caption(
                        "這首歌目前沒有提供試聽。"
                    )


                track_url = song.get(
                    "trackViewUrl"
                )


                if track_url:

                    st.link_button(
                        "🍎 前往 iTunes",
                        track_url,
                        width="stretch"
                    )


                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


# =========================================================
# 網站標題
# =========================================================

st.markdown(
    """
    <div class="main-title">
    🎵 iTunes 音樂搜尋儀表板
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="subtitle">
    搜尋歌手或歌曲，查看專輯封面、發行年份、曲風，並直接試聽歌曲。
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header(
        "🎧 音樂搜尋"
    )


    keyword = st.text_input(
        "輸入歌手或歌曲名稱",
        value="Jay Chou",
        placeholder=(
            "例如 Jay Chou、"
            "Taylor Swift、Adele"
        )
    )


    result_count = st.slider(
        "搜尋筆數",
        min_value=5,
        max_value=100,
        value=30,
        step=5
    )


    country = st.selectbox(
        "iTunes Store 地區",
        [
            "TW",
            "US",
            "JP",
            "HK"
        ],
        index=0
    )


    search_button = st.button(
        "🔍 開始搜尋",
        type="primary",
        width="stretch"
    )


    st.divider()


    st.caption(
        "建議搜尋："
    )


    st.caption(
        "Jay Chou、Jolin Tsai、"
        "JJ Lin、Mayday、"
        "Taylor Swift、Adele"
    )


# =========================================================
# Session State
# =========================================================

if "music_keyword" not in st.session_state:

    st.session_state.music_keyword = (
        "Jay Chou"
    )


if "music_limit" not in st.session_state:

    st.session_state.music_limit = 30


if "music_country" not in st.session_state:

    st.session_state.music_country = (
        "TW"
    )


if search_button:

    if keyword.strip():

        st.session_state.music_keyword = (
            keyword.strip()
        )

        st.session_state.music_limit = (
            result_count
        )

        st.session_state.music_country = (
            country
        )

    else:

        st.warning(
            "請先輸入歌手或歌曲名稱。"
        )


# =========================================================
# API 查詢
# =========================================================

try:

    with st.spinner(
        f"正在搜尋「"
        f"{st.session_state.music_keyword}"
        f"」..."
    ):

        songs = search_music(
            st.session_state.music_keyword,
            st.session_state.music_limit,
            st.session_state.music_country
        )


    # =====================================================
    # 沒有結果
    # =====================================================

    if not songs:

        st.warning(
            "找不到相關歌曲，"
            "可以改用英文歌手名稱或更換地區再試一次。"
        )


    else:

        music_df = build_music_df(
            songs
        )


        # =================================================
        # 搜尋摘要
        # =================================================

        st.markdown(
            f"### 🔎 「"
            f"{st.session_state.music_keyword}"
            f"」搜尋結果"
        )


        metric_col1, metric_col2, metric_col3, metric_col4 = (
            st.columns(4)
        )


        metric_col1.metric(
            "搜尋結果",
            len(songs)
        )


        unique_artists = (
            music_df["歌手"]
            .nunique()
        )


        metric_col2.metric(
            "歌手數",
            unique_artists
        )


        unique_albums = (
            music_df["專輯"]
            .nunique()
        )


        metric_col3.metric(
            "專輯數",
            unique_albums
        )


        valid_years = (
            music_df["年份"]
            .dropna()
        )


        if not valid_years.empty:

            year_range = (
                f"{int(valid_years.min())}"
                f" ～ "
                f"{int(valid_years.max())}"
            )

        else:

            year_range = "無資料"


        metric_col4.metric(
            "發行年份",
            year_range
        )


        # =================================================
        # Tabs
        # =================================================

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🎧 歌曲試聽",
                "📊 年份分析",
                "📋 歌曲資料",
                "📚 API 教學"
            ]
        )


        # =================================================
        # Tab 1：歌曲卡片
        # =================================================

        with tab1:

            st.markdown(
                "### 🎵 歌曲搜尋結果"
            )


            st.caption(
                "目前顯示前 12 筆結果。"
            )


            show_song_cards(
                songs,
                max_cards=12
            )


        # =================================================
        # Tab 2：Plotly
        # =================================================

        with tab2:

            render_year_chart(
                music_df
            )


            # ---------------------------------------------
            # 曲風統計
            # ---------------------------------------------

            genre_df = (
                music_df[
                    "曲風"
                ]
                .value_counts()
                .reset_index()
            )


            genre_df.columns = [
                "曲風",
                "歌曲數量"
            ]


            if not genre_df.empty:

                fig = px.pie(
                    genre_df,
                    names="曲風",
                    values="歌曲數量",
                    title="曲風分布"
                )


                fig.update_layout(
                    height=450
                )


                st.plotly_chart(
                    fig,
                    width="stretch"
                )


        # =================================================
        # Tab 3：DataFrame
        # =================================================

        with tab3:

            st.markdown(
                "### 📋 歌曲資料表"
            )


            display_df = (
                music_df[
                    [
                        "歌曲名稱",
                        "歌手",
                        "專輯",
                        "年份",
                        "曲風",
                        "價格",
                        "幣別"
                    ]
                ]
            )


            st.dataframe(
                display_df,
                width="stretch",
                height=520,
                hide_index=True
            )


            csv_data = (
                music_df
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8-sig"
                )
            )


            st.download_button(
                label="📥 下載歌曲資料 CSV",
                data=csv_data,
                file_name="itunes_music_results.csv",
                mime="text/csv"
            )


        # =================================================
        # Tab 4：API 教學
        # =================================================

        with tab4:

            st.markdown(
                """
                ### iTunes Search API 流程

                使用者輸入歌手或歌曲名稱：

                `歌手／歌曲名稱`

                ↓

                `iTunes Search API`

                ↓

                `JSON`

                ↓

                `Pandas DataFrame`

                ↓

                `Plotly`

                ↓

                `Streamlit`

                這個 API 一次就能取得很多實用資料：

                - 歌曲名稱 `trackName`
                - 歌手名稱 `artistName`
                - 專輯名稱 `collectionName`
                - 封面 `artworkUrl100`
                - 試聽網址 `previewUrl`
                - 發行日期 `releaseDate`
                - 曲風 `primaryGenreName`
                - iTunes 網址 `trackViewUrl`

                因此很適合拿來練習：

                `API → JSON → DataFrame → 視覺化`
                """
            )


# =========================================================
# API 錯誤
# =========================================================

except requests.exceptions.Timeout:

    st.error(
        "iTunes Search API 回應時間過長，"
        "請稍後再試一次。"
    )


except requests.exceptions.ConnectionError:

    st.error(
        "目前無法連線到 iTunes Search API，"
        "請檢查網路連線。"
    )


except requests.RequestException as error:

    st.error(
        f"API 查詢失敗：{error}"
    )


except Exception as error:

    st.error(
        f"程式發生錯誤：{error}"
    )
```
