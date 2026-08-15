### 基於gradio實作水果營養查詢器

```py
import requests
import gradio as gr


### API 設定
BASE_URL = "https://www.fruityvice.com/api/fruit"


### 查詢水果資料
def get_fruit_info(fruit_name: str):
    """
    根據使用者輸入的水果英文名稱，
    向 Fruityvice API 查詢水果與營養資料。
    """

    fruit_name = fruit_name.strip().lower() # 移除前後空白並統一轉成小寫

    if not fruit_name:
        return "請輸入水果英文名稱", "", "", "", "", "", "", "", ""

    try:

        response = requests.get(
            f"{BASE_URL}/{fruit_name}",
            timeout=10
        ) # 向 Fruityvice API 發送 GET Request


        if response.status_code == 404:
            return "找不到這個水果", "", "", "", "", "", "", "", ""


        response.raise_for_status() # HTTP 狀態碼不是成功狀態時產生例外

        data = response.json() # 將 JSON Response 轉成 Python dict


        ### 取得水果基本資料
        name = data["name"]
        family = data["family"]
        genus = data["genus"]
        order = data["order"]


        ### 取得水果營養資料
        nutritions = data["nutritions"]

        calories = nutritions["calories"]
        fat = nutritions["fat"]
        sugar = nutritions["sugar"]
        carbohydrates = nutritions["carbohydrates"]
        protein = nutritions["protein"]


        return (
            name,
            family,
            genus,
            order,
            calories,
            fat,
            sugar,
            carbohydrates,
            protein
        )


    except requests.RequestException as error:

        return (
            f"API 連線失敗：{error}",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        )


    except Exception as error:

        return (
            f"程式發生錯誤：{error}",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        )


### 建立 Gradio 介面
with gr.Blocks(title="水果營養查詢器") as demo:

    gr.Markdown(
        """
        # 🍎 Fruityvice 水果營養查詢器

        輸入水果的英文名稱，
        即可查詢水果分類與營養資訊。

        例如：`apple`、`banana`、`strawberry`、`orange`
        """
    )


    ### 水果名稱輸入
    fruit_input = gr.Textbox(
        label="水果英文名稱",
        placeholder="例如 apple",
        value="apple"
    )


    ### 查詢按鈕
    search_button = gr.Button(
        "🔍 查詢水果",
        variant="primary"
    )


    ### 水果基本資料
    gr.Markdown("## 🍎 水果基本資料")

    with gr.Row():

        name_output = gr.Textbox(
            label="水果名稱"
        )

        family_output = gr.Textbox(
            label="科 Family"
        )


    with gr.Row():

        genus_output = gr.Textbox(
            label="屬 Genus"
        )

        order_output = gr.Textbox(
            label="目 Order"
        )


    ### 水果營養資料
    gr.Markdown("## 🥗 營養資訊")

    with gr.Row():

        calories_output = gr.Number(
            label="熱量 Calories"
        )

        sugar_output = gr.Number(
            label="糖分 Sugar"
        )

        carbohydrates_output = gr.Number(
            label="碳水化合物 Carbohydrates"
        )


    with gr.Row():

        protein_output = gr.Number(
            label="蛋白質 Protein"
        )

        fat_output = gr.Number(
            label="脂肪 Fat"
        )


    ### 按下按鈕後執行水果查詢
    search_button.click(
        fn=get_fruit_info,
        inputs=fruit_input,
        outputs=[
            name_output,
            family_output,
            genus_output,
            order_output,
            calories_output,
            fat_output,
            sugar_output,
            carbohydrates_output,
            protein_output
        ]
    )


    ### 按 Enter 也可以直接查詢
    fruit_input.submit(
        fn=get_fruit_info,
        inputs=fruit_input,
        outputs=[
            name_output,
            family_output,
            genus_output,
            order_output,
            calories_output,
            fat_output,
            sugar_output,
            carbohydrates_output,
            protein_output
        ]
    )


### 啟動 Gradio
demo.launch()
```

### 基於Streamlit實作Fruityvice 水果營養分析儀表板

```py
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


### API 設定
BASE_URL = "https://www.fruityvice.com/api/fruit"


### Streamlit 頁面設定
st.set_page_config(
    page_title="Fruityvice 水果營養分析儀表板", # 瀏覽器分頁標題
    page_icon="🍎", # 瀏覽器分頁圖示
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
        color: #8a8a8a;
        margin-bottom: 24px;
    }

    .fruit-card {
        padding: 24px;
        border-radius: 24px;
        background: linear-gradient(135deg, #fff5dc, #ffffff);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.06);
        color: #2b2b2b; # 固定卡片內主要文字顏色
    }

    .fruit-name {
        font-size: 36px;
        font-weight: 900;
        color: #ff7a00;
        margin-bottom: 18px;
    }

    .fruit-card p {
        color: #333333;
        font-size: 16px;
        line-height: 1.8;
        margin: 8px 0px;
    }

    .fruit-card b {
        color: #111111;
        font-weight: 800;
    }

    .small-note {
        color: #666666;
        font-size: 14px;
        margin-top: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


### 建立 API GET Request 函式
def get_json(url: str):
    """
    向指定 API 網址發送 GET Request，
    並將回傳的 JSON 資料轉成 Python 物件。
    """

    response = requests.get(
        url,
        timeout=10 # API 最多等待 10 秒
    )

    if response.status_code == 404:
        raise ValueError("找不到水果資料")

    response.raise_for_status() # HTTP 狀態碼不是成功狀態時產生例外

    return response.json() # 將 JSON Response 轉成 Python 物件


### 取得所有水果資料
@st.cache_data(show_spinner=False)
def get_all_fruits() -> list[dict]:
    """
    取得 Fruityvice 所有水果資料。

    使用 Streamlit cache，
    避免每次重新執行程式都重新呼叫 API。
    """

    return get_json(
        f"{BASE_URL}/all"
    )


### 取得指定水果資料
@st.cache_data(show_spinner=False)
def get_fruit(fruit_name: str) -> dict:
    """
    根據水果英文名稱，
    取得指定水果的完整資料。
    """

    fruit_name = fruit_name.strip().lower() # 移除前後空白並轉成小寫

    return get_json(
        f"{BASE_URL}/{fruit_name}"
    )


### 建立所有水果 DataFrame
def build_fruits_df(fruits: list[dict]) -> pd.DataFrame:
    """
    將 Fruityvice 回傳的水果 JSON，
    整理成 Pandas DataFrame。
    """

    rows = []

    for fruit in fruits:

        nutrition = fruit["nutritions"] # 取得目前水果的營養資料

        rows.append(
            {
                "水果": fruit["name"],
                "科": fruit["family"],
                "屬": fruit["genus"],
                "目": fruit["order"],
                "熱量": nutrition["calories"],
                "脂肪": nutrition["fat"],
                "糖分": nutrition["sugar"],
                "碳水化合物": nutrition["carbohydrates"],
                "蛋白質": nutrition["protein"]
            }
        )

    return pd.DataFrame(rows)


### 建立單一水果營養 DataFrame
def build_nutrition_df(fruit: dict) -> pd.DataFrame:
    """
    將單一水果的營養資訊，
    整理成適合製作圖表的 DataFrame。
    """

    nutrition = fruit["nutritions"]

    data = {
        "營養素": [
            "脂肪",
            "糖分",
            "碳水化合物",
            "蛋白質"
        ],
        "數值": [
            nutrition["fat"],
            nutrition["sugar"],
            nutrition["carbohydrates"],
            nutrition["protein"]
        ]
    }

    return pd.DataFrame(data)


### 建立營養長條圖
def render_bar_chart(nutrition_df: pd.DataFrame) -> None:
    """
    使用 Plotly 建立水果營養長條圖。
    """

    fig = px.bar(
        nutrition_df,
        x="營養素",
        y="數值",
        text="數值",
        color="營養素",
        title="營養成分比較"
    )

    fig.update_traces(
        textposition="outside" # 將數值顯示在長條上方
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


### 建立營養雷達圖
def render_radar_chart(
    nutrition_df: pd.DataFrame,
    fruit_name: str
) -> None:
    """
    使用 Plotly 建立水果營養雷達圖。
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=nutrition_df["數值"],
            theta=nutrition_df["營養素"],
            fill="toself",
            name=fruit_name
        )
    )

    max_value = max(
        20,
        float(
            nutrition_df["數值"].max()
        ) * 1.2
    ) # 雷達圖最大刻度稍微高於最高營養值

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
        showlegend=False,
        height=430
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


### 顯示網站標題
st.markdown(
    "<div class='main-title'>🍎 Fruityvice 水果營養分析儀表板</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    查詢水果營養資訊、比較營養成分，並分析不同水果的營養差異。
    </div>
    """,
    unsafe_allow_html=True
)


### 主程式
try:

    ### 取得所有水果資料
    with st.spinner(
        "正在載入水果資料..."
    ):

        fruits = get_all_fruits()

        fruits_df = build_fruits_df(
            fruits
        )


    ### 建立水果名稱清單
    fruit_names = sorted(
        [
            fruit["name"]
            for fruit in fruits
        ]
    )


    ### Sidebar 查詢設定
    with st.sidebar:

        st.header(
            "🍎 查詢設定"
        )


        ### 選擇水果
        selected_fruit = st.selectbox(
            "選擇水果",
            fruit_names,
            index=fruit_names.index("Apple")
            if "Apple" in fruit_names
            else 0
        )


        ### 搜尋水果名稱
        keyword = st.text_input(
            "或輸入水果英文名稱",
            placeholder="例如 apple、banana、orange"
        )


        search_button = st.button(
            "🔍 開始查詢",
            type="primary",
            width="stretch"
        )


        st.divider()


        ### 排行榜設定
        ranking_type = st.selectbox(
            "排行榜依據",
            [
                "熱量",
                "糖分",
                "碳水化合物",
                "蛋白質",
                "脂肪"
            ]
        )


        ranking_count = st.slider(
            "排行榜顯示數量",
            min_value=5,
            max_value=20,
            value=10
        )


        st.caption(
            "營養資料皆以每 100g 水果為基準。"
        )


    ### 建立 Session State
    if "fruit_name" not in st.session_state:
        st.session_state.fruit_name = selected_fruit


    ### 按下查詢按鈕後更新水果名稱
    if search_button:

        if keyword.strip():

            st.session_state.fruit_name = (
                keyword.strip()
            )

        else:

            st.session_state.fruit_name = (
                selected_fruit
            )


    ### 下拉選單改變時使用目前選擇的水果
    if not search_button and not keyword.strip():

        st.session_state.fruit_name = (
            selected_fruit
        )


    fruit_name = (
        st.session_state.fruit_name
    )


    ### 查詢目前選擇的水果
    fruit = get_fruit(
        fruit_name
    )


    ### 取得水果基本資料
    name = fruit["name"]
    family = fruit["family"]
    genus = fruit["genus"]
    order = fruit["order"]
    fruit_id = fruit["id"]

    nutrition = fruit["nutritions"]


    ### 建立營養 DataFrame
    nutrition_df = build_nutrition_df(
        fruit
    )


    ### 顯示水果基本資料
    st.markdown(
        f"""
        <div class="fruit-card">
            <div class="fruit-name">🍊 {name}</div>
            <p><b>ID：</b>{fruit_id}</p>
            <p><b>科 Family：</b>{family}</p>
            <p><b>屬 Genus：</b>{genus}</p>
            <p><b>目 Order：</b>{order}</p>
            <div class="small-note">
                以下營養數值以每 100g 水果為基準
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    ### 顯示營養指標
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = (
        st.columns(5)
    )


    metric_col1.metric(
        "🔥 熱量",
        f"{nutrition['calories']} kcal"
    )


    metric_col2.metric(
        "🍬 糖分",
        f"{nutrition['sugar']} g"
    )


    metric_col3.metric(
        "🍞 碳水化合物",
        f"{nutrition['carbohydrates']} g"
    )


    metric_col4.metric(
        "💪 蛋白質",
        f"{nutrition['protein']} g"
    )


    metric_col5.metric(
        "🥑 脂肪",
        f"{nutrition['fat']} g"
    )


    st.divider()


    ### 建立功能分頁
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 營養分析",
            "🏆 水果排行榜",
            "📋 水果資料庫",
            "🔎 原始資料"
        ]
    )


    ### Tab 1：營養分析
    with tab1:

        st.subheader(
            f"📊 {name} 營養分析"
        )


        chart_col1, chart_col2 = st.columns(2)


        ### 左側顯示長條圖
        with chart_col1:

            render_bar_chart(
                nutrition_df
            )


        ### 右側顯示雷達圖
        with chart_col2:

            render_radar_chart(
                nutrition_df,
                name
            )


        ### 計算最高營養成分
        highest_nutrition = (
            nutrition_df
            .sort_values(
                "數值",
                ascending=False
            )
            .iloc[0]
        )


        ### 顯示分析摘要
        st.info(
            f"{name} 在脂肪、糖分、碳水化合物、蛋白質之中，"
            f"數值最高的是「{highest_nutrition['營養素']}」，"
            f"數值為 {highest_nutrition['數值']} g。"
        )


    ### Tab 2：水果排行榜
    with tab2:

        st.subheader(
            f"🏆 {ranking_type}排行榜"
        )


        ### 根據選擇的營養素進行排序
        ranking_df = (
            fruits_df
            .sort_values(
                ranking_type,
                ascending=False
            )
            .head(
                ranking_count
            )
        )


        ### 建立排行榜長條圖
        ranking_fig = px.bar(
            ranking_df,
            x="水果",
            y=ranking_type,
            color=ranking_type,
            text=ranking_type,
            title=f"水果 {ranking_type} Top {ranking_count}"
        )


        ranking_fig.update_traces(
            textposition="outside"
        )


        ranking_fig.update_layout(
            height=500
        )


        st.plotly_chart(
            ranking_fig,
            width="stretch"
        )


        ### 顯示排行榜資料
        st.dataframe(
            ranking_df[
                [
                    "水果",
                    ranking_type
                ]
            ],
            width="stretch",
            hide_index=True
        )


    ### Tab 3：水果資料庫
    with tab3:

        st.subheader(
            "📋 Fruityvice 水果資料庫"
        )


        ### 顯示所有水果資料
        st.dataframe(
            fruits_df,
            width="stretch",
            height=520,
            hide_index=True
        )


        ### 將 DataFrame 轉成 CSV
        csv_data = fruits_df.to_csv(
            index=False
        ).encode(
            "utf-8-sig" # 避免 Excel 開啟中文時出現亂碼
        )


        ### 建立 CSV 下載按鈕
        st.download_button(
            label="📥 下載水果營養資料 CSV",
            data=csv_data,
            file_name="fruityvice_fruits.csv",
            mime="text/csv"
        )


    ### Tab 4：原始資料
    with tab4:

        st.subheader(
            f"🔎 {name} 原始 JSON 資料"
        )


        ### 顯示 API 原始 JSON
        st.json(
            fruit
        )


### 找不到水果
except ValueError:

    st.error(
        "找不到這個水果。"
        "請輸入英文名稱，例如 apple、banana、orange。"
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
