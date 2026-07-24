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

```python
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_URL = "https://pokeapi.co/api/v2"


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


st.set_page_config(
    page_title="PokéAPI 寶可夢圖鑑",
    page_icon="⚡",
    layout="wide"
)


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
    unsafe_allow_html=True
)


@st.cache_data(show_spinner=False)
def get_json(url: str) -> dict:
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        raise ValueError("找不到資料")

    response.raise_for_status()
    return response.json()


@st.cache_data(show_spinner=False)
def fetch_pokemon(keyword: str) -> dict:
    keyword = keyword.strip().lower()
    return get_json(f"{BASE_URL}/pokemon/{keyword}")


@st.cache_data(show_spinner=False)
def fetch_species(url: str) -> dict:
    return get_json(url)


@st.cache_data(show_spinner=False)
def fetch_evolution_chain(url: str) -> dict:
    return get_json(url)


def parse_evolution_chain(chain_data: dict) -> list[str]:
    result = []

    def walk(node: dict):
        result.append(node["species"]["name"])
        for next_node in node["evolves_to"]:
            walk(next_node)

    walk(chain_data["chain"])
    return result


def get_official_image(pokemon: dict) -> str | None:
    return (
        pokemon["sprites"]
        ["other"]
        ["official-artwork"]
        ["front_default"]
    )


def get_type_badges(types: list[str]) -> str:
    html = ""

    for pokemon_type in types:
        color = TYPE_COLOR.get(pokemon_type, "#666")
        html += (
            f"<span class='type-badge' "
            f"style='background:{color}'>{pokemon_type.upper()}</span>"
        )

    return html


def build_stats_df(pokemon: dict) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "能力": item["stat"]["name"],
                "數值": item["base_stat"]
            }
            for item in pokemon["stats"]
        ]
    )


def build_moves_df(pokemon: dict) -> pd.DataFrame:
    rows = []

    for item in pokemon["moves"]:
        move = item["move"]["name"]
        version_details = item["version_group_details"]

        learn_methods = sorted({
            detail["move_learn_method"]["name"]
            for detail in version_details
        })

        rows.append({
            "技能": move,
            "學習方式": ", ".join(learn_methods[:3])
        })

    return pd.DataFrame(rows)


def render_radar_chart(stats_df: pd.DataFrame, pokemon_name: str):
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=stats_df["數值"],
            theta=stats_df["能力"],
            fill="toself",
            name=pokemon_name
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(160, int(stats_df["數值"].max()) + 20)]
            )
        ),
        showlegend=False,
        height=430,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(stats_df: pd.DataFrame):
    fig = px.bar(
        stats_df,
        x="能力",
        y="數值",
        text="數值",
        title="能力值長條圖"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        height=430,
        yaxis_range=[0, max(160, int(stats_df["數值"].max()) + 20)]
    )

    st.plotly_chart(fig, use_container_width=True)


st.markdown("<div class='main-title'>⚡ PokéAPI 寶可夢圖鑑儀表板</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>輸入英文名稱或圖鑑編號，即時查詢屬性、能力值、技能、進化鏈與官方圖片。</div>",
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("查詢設定")
    keyword = st.text_input(
        "寶可夢英文名稱或圖鑑編號",
        value="pikachu",
        placeholder="例如 pikachu、charizard、25"
    )

    show_all_moves = st.checkbox("顯示全部技能", value=False)
    search_button = st.button("開始查詢", type="primary", use_container_width=True)

    st.divider()
    st.caption("建議學生先查：pikachu、eevee、charizard、mewtwo、lucario")


if search_button or keyword:
    try:
        pokemon = fetch_pokemon(keyword)
        species = fetch_species(pokemon["species"]["url"])
        evolution_chain = fetch_evolution_chain(species["evolution_chain"]["url"])

        pokemon_name = pokemon["name"]
        pokemon_id = pokemon["id"]
        image_url = get_official_image(pokemon)

        types = [item["type"]["name"] for item in pokemon["types"]]
        abilities = [item["ability"]["name"] for item in pokemon["abilities"]]
        stats_df = build_stats_df(pokemon)
        moves_df = build_moves_df(pokemon)
        evolution_names = parse_evolution_chain(evolution_chain)

        left_col, right_col = st.columns([1, 2])

        with left_col:
            st.markdown("<div class='pokemon-card'>", unsafe_allow_html=True)

            if image_url:
                st.image(image_url, use_container_width=True)

            st.markdown(f"## #{pokemon_id} {pokemon_name.title()}")
            st.markdown(get_type_badges(types), unsafe_allow_html=True)
            st.markdown(
                f"<p class='small-note'>世代：{species['generation']['name']} ｜ "
                f"顏色：{species['color']['name']}</p>",
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            metric_cols = st.columns(4)

            metric_cols[0].metric("身高", f"{pokemon['height'] / 10} m")
            metric_cols[1].metric("體重", f"{pokemon['weight'] / 10} kg")
            metric_cols[2].metric("基礎經驗", pokemon["base_experience"])
            metric_cols[3].metric("技能數", len(pokemon["moves"]))

            st.markdown("### 特性")
            st.write("、".join(abilities))

            st.markdown("### 進化鏈")
            st.success(" → ".join(evolution_names))

        tab1, tab2, tab3, tab4 = st.tabs(
            ["能力分析", "技能資料庫", "原始資料摘要", "教學引導"]
        )

        with tab1:
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                render_radar_chart(stats_df, pokemon_name)

            with chart_col2:
                render_bar_chart(stats_df)

            total_score = int(stats_df["數值"].sum())
            strongest = stats_df.sort_values("數值", ascending=False).iloc[0]
            weakest = stats_df.sort_values("數值", ascending=True).iloc[0]

            insight_col1, insight_col2, insight_col3 = st.columns(3)
            insight_col1.metric("總能力值", total_score)
            insight_col2.metric("最高能力", f"{strongest['能力']} ({strongest['數值']})")
            insight_col3.metric("最低能力", f"{weakest['能力']} ({weakest['數值']})")

        with tab2:
            st.markdown("### 技能列表")

            if show_all_moves:
                st.dataframe(moves_df, use_container_width=True, height=500)
            else:
                st.info("目前只顯示前 30 筆。若要看完整技能，請到左側勾選「顯示全部技能」。")
                st.dataframe(moves_df.head(30), use_container_width=True, height=500)

        with tab3:
            summary = {
                "圖鑑編號": pokemon_id,
                "名稱": pokemon_name,
                "屬性": ", ".join(types),
                "特性": ", ".join(abilities),
                "身高(m)": pokemon["height"] / 10,
                "體重(kg)": pokemon["weight"] / 10,
                "世代": species["generation"]["name"],
                "棲息地": species["habitat"]["name"] if species["habitat"] else "無資料",
                "進化鏈": " -> ".join(evolution_names),
                "圖片網址": image_url
            }

            st.json(summary)

        with tab4:
            st.markdown(
                """
                ### 可以引導學生觀察的問題

                這個範例其實很適合拿來教 REST API。
                因為學生會很快看到：不是每個資料都在同一個 API 回傳裡。

                例如：

                - 基本能力值來自 `/pokemon/{name}`
                - 世代、顏色、棲息地來自 species URL
                - 進化鏈又要再接 evolution chain URL
                - 圖片不是本機檔案，而是 API 回傳的圖片網址
                - 技能資料很多，所以要設計表格與篩選策略

                這比單純印出 JSON 有感很多。
                學生會真的理解「資料串接」不是背語法，而是在拆資料來源。
                """
            )

    except ValueError:
        st.error("找不到這隻寶可夢。請輸入英文名稱，例如 pikachu，或輸入圖鑑編號，例如 25。")
    except requests.RequestException as error:
        st.error(f"API 連線失敗：{error}")
```
