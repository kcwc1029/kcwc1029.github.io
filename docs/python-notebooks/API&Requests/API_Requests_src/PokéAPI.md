PokéAPI 是全球知名的免費 REST API，提供完整的寶可夢世界資料庫，包含：

- 寶可夢基本資料
- 屬性(type)
- 能力值(stats)
- 技能(moves)
- 進化鏈
- 圖鑑編號
- 圖片 sprites
- 道具 items
- 地區 region
- 世代 generation

### 範例：終端機版寶可夢查詢器

```python
import webbrowser

import requests


BASE_URL = "https://pokeapi.co/api/v2"


def get_json(url: str) -> dict:
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        raise ValueError("找不到這隻寶可夢，請確認英文名稱或圖鑑編號。")

    response.raise_for_status()
    return response.json()


def fetch_pokemon(keyword: str) -> dict:
    keyword = keyword.strip().lower()
    return get_json(f"{BASE_URL}/pokemon/{keyword}")


def fetch_species(species_url: str) -> dict:
    return get_json(species_url)


def fetch_evolution_chain(chain_url: str) -> dict:
    return get_json(chain_url)


def parse_evolution_chain(chain_data: dict) -> list[str]:
    result = []

    def walk(node: dict):
        result.append(node["species"]["name"])

        for next_node in node["evolves_to"]:
            walk(next_node)

    walk(chain_data["chain"])
    return result


def show_pokemon_info(pokemon: dict) -> None:
    species = fetch_species(pokemon["species"]["url"])
    chain_data = fetch_evolution_chain(species["evolution_chain"]["url"])
    evolution_names = parse_evolution_chain(chain_data)

    types = [item["type"]["name"] for item in pokemon["types"]]
    abilities = [item["ability"]["name"] for item in pokemon["abilities"]]
    stats = {
        item["stat"]["name"]: item["base_stat"]
        for item in pokemon["stats"]
    }
    moves = [item["move"]["name"] for item in pokemon["moves"][:20]]

    official_image = (
        pokemon["sprites"]
        ["other"]
        ["official-artwork"]
        ["front_default"]
    )

    print("\n" + "=" * 50)
    print("寶可夢完整資料")
    print("=" * 50)
    print(f"圖鑑編號：{pokemon['id']}")
    print(f"英文名稱：{pokemon['name']}")
    print(f"身高：{pokemon['height'] / 10} 公尺")
    print(f"體重：{pokemon['weight'] / 10} 公斤")
    print(f"基礎經驗值：{pokemon['base_experience']}")
    print(f"屬性：{', '.join(types)}")
    print(f"特性：{', '.join(abilities)}")
    print(f"世代：{species['generation']['name']}")
    print(f"顏色：{species['color']['name']}")
    print(f"棲息地：{species['habitat']['name'] if species['habitat'] else '無資料'}")
    print(f"進化鏈：{' -> '.join(evolution_names)}")

    print("\n能力值")
    for name, value in stats.items():
        print(f"- {name}: {value}")

    print("\n前 20 個技能")
    for move in moves:
        print(f"- {move}")

    print("\n圖片網址")
    print(official_image)

    if official_image:
        answer = input("\n是否要用瀏覽器開啟圖片？(y/n)：").strip().lower()
        if answer == "y":
            webbrowser.open(official_image)
            print("已開啟瀏覽器。")


def main() -> None:
    print("=== PokéAPI 寶可夢查詢器 ===")
    print("可輸入英文名稱，例如 pikachu、charizard、bulbasaur")
    print("也可輸入圖鑑編號，例如 25、6、1")

    keyword = input("\n請輸入寶可夢名稱或圖鑑編號：")

    try:
        pokemon = fetch_pokemon(keyword)
        show_pokemon_info(pokemon)
    except ValueError as error:
        print("錯誤：", error)
    except requests.RequestException as error:
        print("API 連線失敗：", error)


if __name__ == "__main__":
    main()
```

### 範例：Streamlit 高完成度圖鑑儀表板

```py
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


### API 設定
BASE_URL = "https://pokeapi.co/api/v2" # PokéAPI 的基礎網址


### 寶可夢屬性顏色
TYPE_COLOR = {
    "normal": "#A8A77A",
    "fire": "#EE8130",
    "water": "#6390F0",
    "electric": "#F7D02C",
    "grass": "#7AC74C",
    "ice": "#96D9D6",
    "fighting": "#C22E28",
    "poison": "#A33EA1",
    "ground": "#E2BF65",
    "flying": "#A98FF3",
    "psychic": "#F95587",
    "bug": "#A6B91A",
    "rock": "#B6A136",
    "ghost": "#735797",
    "dragon": "#6F35FC",
    "dark": "#705746",
    "steel": "#B7B7CE",
    "fairy": "#D685AD",
}


### Streamlit 頁面設定
st.set_page_config(
    page_title="PokéAPI 寶可夢圖鑑", # 瀏覽器分頁標題
    page_icon="⚡", # 瀏覽器分頁圖示
    layout="wide" # 使用寬版頁面
)


### 自訂 CSS 樣式
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
        color: #666;
        margin-bottom: 24px;
    }

    .pokemon-card {
        padding: 24px;
        border-radius: 24px;
        background: linear-gradient(135deg, #fff7d6, #ffffff);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.06);
    }

    .type-badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px 6px 4px 0px;
        border-radius: 999px;
        color: white;
        font-weight: 800;
        font-size: 14px;
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
        timeout=10 # API 最多等待 10 秒
    )

    if response.status_code == 404:
        raise ValueError("找不到資料") # 查無資料時產生自訂錯誤

    response.raise_for_status() # HTTP 狀態碼不是成功狀態時產生例外

    return response.json() # 將 JSON Response 轉成 Python dict


### 取得寶可夢基本資料
@st.cache_data(show_spinner=False)
def fetch_pokemon(keyword: str) -> dict:
    """
    根據寶可夢英文名稱或圖鑑編號，
    取得寶可夢的基本資料。
    """

    keyword = keyword.strip().lower() # 移除前後空白並統一轉成小寫

    return get_json(
        f"{BASE_URL}/pokemon/{keyword}"
    )


### 取得寶可夢物種資料
@st.cache_data(show_spinner=False)
def fetch_species(url: str) -> dict:
    """
    透過 Species API 網址，
    取得寶可夢的世代、顏色、棲息地等資料。
    """

    return get_json(url)


### 取得寶可夢進化鏈資料
@st.cache_data(show_spinner=False)
def fetch_evolution_chain(url: str) -> dict:
    """
    透過 Evolution Chain API 網址，
    取得寶可夢完整進化鏈資料。
    """

    return get_json(url)


### 整理寶可夢進化鏈
def parse_evolution_chain(
    chain_data: dict
) -> list[str]:

    result = [] # 儲存整理完成的寶可夢名稱

    def walk(node: dict):

        result.append(
            node["species"]["name"]
        ) # 將目前節點的寶可夢名稱加入結果

        for next_node in node["evolves_to"]:
            walk(next_node) # 使用遞迴繼續尋找下一階段進化

    walk(
        chain_data["chain"] # 從進化鏈第一個節點開始處理
    )

    return result


### 取得寶可夢官方圖片
def get_official_image(
    pokemon: dict
) -> str | None:

    return (
        pokemon["sprites"]
        ["other"]
        ["official-artwork"]
        ["front_default"]
    ) # 取得 PokéAPI 提供的官方 Artwork 圖片網址


### 建立寶可夢屬性標籤
def get_type_badges(
    types: list[str]
) -> str:

    html = "" # 儲存所有屬性標籤的 HTML

    for pokemon_type in types:

        color = TYPE_COLOR.get(
            pokemon_type,
            "#666" # 找不到對應屬性時使用灰色
        )

        html += (
            f"<span class='type-badge' "
            f"style='background:{color}'>"
            f"{pokemon_type.upper()}"
            f"</span>"
        )

    return html


### 建立能力值 DataFrame
def build_stats_df(
    pokemon: dict
) -> pd.DataFrame:

    rows = [] # 儲存每一項能力值資料

    for item in pokemon["stats"]:

        rows.append(
            {
                "能力": item["stat"]["name"],
                "數值": item["base_stat"]
            }
        )

    return pd.DataFrame(rows) # 將 list 轉成 Pandas DataFrame


### 建立技能 DataFrame
def build_moves_df(
    pokemon: dict
) -> pd.DataFrame:

    rows = [] # 儲存每一個技能的資料

    for item in pokemon["moves"]:

        move = item["move"]["name"] # 取得技能名稱

        version_details = (
            item["version_group_details"]
        ) # 取得不同版本中的技能學習資料

        learn_methods = sorted(
            {
                detail["move_learn_method"]["name"]
                for detail in version_details
            }
        ) # 使用 set 移除重複的技能學習方式，再進行排序

        rows.append(
            {
                "技能": move,
                "學習方式": ", ".join(
                    learn_methods[:3]
                ) # 最多顯示前三種學習方式
            }
        )

    return pd.DataFrame(rows)


### 建立能力值雷達圖
def render_radar_chart(
    stats_df: pd.DataFrame,
    pokemon_name: str
) -> None:

    fig = go.Figure() # 建立 Plotly Figure

    fig.add_trace(
        go.Scatterpolar(
            r=stats_df["數值"], # 雷達圖半徑使用能力值
            theta=stats_df["能力"], # 雷達圖各軸使用能力名稱
            fill="toself", # 填滿雷達圖內部區域
            name=pokemon_name
        )
    )

    max_value = max(
        160,
        int(
            stats_df["數值"].max()
        ) + 20
    ) # 最大刻度至少 160，若能力值更高則自動增加 20

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[
                    0,
                    max_value
                ]
            )
        ),
        showlegend=False, # 隱藏圖例
        height=430,
        margin=dict(
            l=40,
            r=40,
            t=40,
            b=40
        )
    )

    st.plotly_chart(
        fig,
        width="stretch" # 圖表寬度自動填滿容器
    )


### 建立能力值長條圖
def render_bar_chart(
    stats_df: pd.DataFrame
) -> None:

    fig = px.bar(
        stats_df,
        x="能力",
        y="數值",
        text="數值", # 在長條上顯示能力值
        title="能力值長條圖"
    )

    fig.update_traces(
        textposition="outside" # 將數值顯示在長條上方
    )

    max_value = max(
        160,
        int(
            stats_df["數值"].max()
        ) + 20
    ) # 設定 Y 軸最大值並保留額外顯示空間

    fig.update_layout(
        height=430,
        yaxis_range=[
            0,
            max_value
        ]
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


### 顯示網站標題
st.markdown(
    "<div class='main-title'>⚡ PokéAPI 寶可夢圖鑑儀表板</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    輸入英文名稱或圖鑑編號，即時查詢屬性、能力值、技能、進化鏈與官方圖片。
    </div>
    """,
    unsafe_allow_html=True
)


### 建立 Sidebar 查詢設定
with st.sidebar:

    st.header(
        "查詢設定"
    )

    keyword = st.text_input(
        "寶可夢英文名稱或圖鑑編號",
        value="pikachu", # 預設查詢皮卡丘
        placeholder="例如 pikachu、charizard、25"
    )

    show_all_moves = st.checkbox(
        "顯示全部技能",
        value=False # 預設只顯示部分技能
    )

    search_button = st.button(
        "開始查詢",
        type="primary",
        width="stretch"
    )

    st.divider()

    st.caption(
        "建議學生先查："
        "pikachu、eevee、charizard、mewtwo、lucario"
    )


### 建立 Session State 儲存查詢條件
# Streamlit 操作元件時會重新執行整份程式
# 使用 session_state 可以保存使用者目前查詢的寶可夢
if "search_keyword" not in st.session_state:
    st.session_state.search_keyword = "pikachu" # 第一次開啟網站預設查詢 pikachu


### 按下查詢按鈕後更新查詢條件
if search_button:

    if keyword.strip():

        st.session_state.search_keyword = (
            keyword.strip()
        ) # 移除輸入內容前後的空白


search_keyword = (
    st.session_state.search_keyword
) # 取得目前要查詢的寶可夢


### 呼叫 API 取得寶可夢資料
try:

    with st.spinner(
        f"正在查詢 {search_keyword}..."
    ):

        pokemon = fetch_pokemon(
            search_keyword
        ) # 取得寶可夢基本資料

        species = fetch_species(
            pokemon["species"]["url"]
        ) # 使用基本資料中的網址取得 Species 資料

        evolution_chain = (
            fetch_evolution_chain(
                species["evolution_chain"]["url"]
            )
        ) # 使用 Species 資料中的網址取得進化鏈


    ### 整理寶可夢基本資料
    pokemon_name = (
        pokemon["name"]
    )

    pokemon_id = (
        pokemon["id"]
    )

    image_url = (
        get_official_image(
            pokemon
        )
    )


    ### 整理寶可夢屬性
    types = [
        item["type"]["name"]
        for item in pokemon["types"]
    ]


    ### 整理寶可夢特性
    abilities = [
        item["ability"]["name"]
        for item in pokemon["abilities"]
    ]


    ### 整理寶可夢能力值
    stats_df = (
        build_stats_df(
            pokemon
        )
    )


    ### 整理寶可夢技能
    moves_df = (
        build_moves_df(
            pokemon
        )
    )


    ### 整理寶可夢進化鏈
    evolution_names = (
        parse_evolution_chain(
            evolution_chain
        )
    )


    ### 建立基本資訊左右兩欄
    left_col, right_col = (
        st.columns(
            [1, 2] # 左欄比例 1、右欄比例 2
        )
    )


    ### 左側顯示寶可夢圖片與基本資料
    with left_col:

        st.markdown(
            "<div class='pokemon-card'>",
            unsafe_allow_html=True
        )

        if image_url:

            st.image(
                image_url,
                width="stretch"
            )

        st.markdown(
            f"## #{pokemon_id} "
            f"{pokemon_name.title()}"
        )

        st.markdown(
            get_type_badges(
                types
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <p class='small-note'>
            世代：{species['generation']['name']} ｜
            顏色：{species['color']['name']}
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    ### 右側顯示寶可夢基本數據
    with right_col:

        metric_cols = (
            st.columns(4)
        )

        metric_cols[0].metric(
            "身高",
            f"{pokemon['height'] / 10} m" # API 的身高單位為 0.1 公尺，因此除以 10
        )

        metric_cols[1].metric(
            "體重",
            f"{pokemon['weight'] / 10} kg" # API 的體重單位為 0.1 公斤，因此除以 10
        )

        metric_cols[2].metric(
            "基礎經驗",
            pokemon["base_experience"]
        )

        metric_cols[3].metric(
            "技能數",
            len(
                pokemon["moves"]
            )
        )

        st.markdown(
            "### 特性"
        )

        st.write(
            "、".join(
                abilities
            )
        ) # 使用頓號串接所有特性名稱

        st.markdown(
            "### 進化鏈"
        )

        st.success(
            " → ".join(
                evolution_names
            )
        ) # 使用箭頭串接完整進化鏈


    ### 建立功能分頁
    tab1, tab2, tab3, tab4 = (
        st.tabs(
            [
                "能力分析",
                "技能資料庫",
                "原始資料摘要",
                "教學引導"
            ]
        )
    )


    ### Tab 1：能力分析
    with tab1:

        chart_col1, chart_col2 = (
            st.columns(2)
        )

        with chart_col1:

            render_radar_chart(
                stats_df,
                pokemon_name
            )

        with chart_col2:

            render_bar_chart(
                stats_df
            )


        ### 計算能力值摘要
        total_score = int(
            stats_df[
                "數值"
            ].sum()
        ) # 加總所有基礎能力值


        strongest = (
            stats_df
            .sort_values(
                "數值",
                ascending=False
            )
            .iloc[0]
        ) # 依照能力值由高到低排序，取得最高能力


        weakest = (
            stats_df
            .sort_values(
                "數值",
                ascending=True
            )
            .iloc[0]
        ) # 依照能力值由低到高排序，取得最低能力


        ### 顯示能力值摘要
        insight_col1, insight_col2, insight_col3 = (
            st.columns(3)
        )

        insight_col1.metric(
            "總能力值",
            total_score
        )

        insight_col2.metric(
            "最高能力",
            f"{strongest['能力']} "
            f"({strongest['數值']})"
        )

        insight_col3.metric(
            "最低能力",
            f"{weakest['能力']} "
            f"({weakest['數值']})"
        )


    ### Tab 2：技能資料庫
    with tab2:

        st.markdown(
            "### 技能列表"
        )

        if show_all_moves:

            st.dataframe(
                moves_df,
                width="stretch",
                height=500,
                hide_index=True # 不顯示 DataFrame index
            )

        else:

            st.info(
                "目前只顯示前 30 筆。"
                "若要看完整技能，"
                "請到左側勾選「顯示全部技能」。"
            )

            st.dataframe(
                moves_df.head(30), # 只取前 30 筆技能
                width="stretch",
                height=500,
                hide_index=True
            )


    ### Tab 3：原始資料摘要
    with tab3:

        habitat = (
            species["habitat"]["name"]
            if species["habitat"]
            else "無資料"
        ) # 如果 API 沒有棲息地資料則顯示「無資料」


        ### 建立寶可夢資料摘要
        summary = {
            "圖鑑編號":
                pokemon_id,

            "名稱":
                pokemon_name,

            "屬性":
                ", ".join(
                    types
                ),

            "特性":
                ", ".join(
                    abilities
                ),

            "身高(m)":
                pokemon["height"] / 10,

            "體重(kg)":
                pokemon["weight"] / 10,

            "世代":
                species[
                    "generation"
                ][
                    "name"
                ],

            "棲息地":
                habitat,

            "進化鏈":
                " -> ".join(
                    evolution_names
                ),

            "圖片網址":
                image_url
        }


        ### 使用 JSON 格式顯示資料摘要
        st.json(
            summary
        )


    ### Tab 4：教學引導
    with tab4:

        st.markdown(
            """
            ### 可以引導學生觀察的問題

            這個範例很適合拿來教 REST API，因為學生可以直接看到：
            一隻寶可夢的完整資料，其實不是從單一 API 一次取得。

            - 基本資料來自 `/pokemon/{name}`
            - 世代、顏色、棲息地來自 Species API
            - 進化鏈來自 Evolution Chain API
            - 圖片來自 API 回傳的圖片網址
            - 技能資料可以再透過 Pandas 整理
            - 能力值可以再利用 Plotly 視覺化

            因此整個流程會變成：

            `輸入資料 → 發送 Request → JSON → 整理資料 → DataFrame → 圖表 → Streamlit`

            這樣比單純把 JSON 印出來，更容易理解 API 在實際專案裡怎麼使用。
            """
        )


### 處理找不到寶可夢的錯誤
except ValueError:

    st.error(
        "找不到這隻寶可夢。"
        "請輸入英文名稱，例如 pikachu，"
        "或輸入圖鑑編號，例如 25。"
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
