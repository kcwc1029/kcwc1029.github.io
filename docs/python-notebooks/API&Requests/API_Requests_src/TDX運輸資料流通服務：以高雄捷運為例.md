# TDX運輸資料流通服務：以高雄捷運為例

- TDX首頁：https://tdx.transportdata.tw/
- 傳接API服務：https://tdx.transportdata.tw/data-service/basic

- 要先註冊(手機，gmail，如果有校方信件會更推薦)
- 他是有提供免費額度，用完就收費
- 要去得Client ID與Client Secret
  - 【會員中心】->左側【資料服務】->【資料存取金要】

```text
### 註冊練習的
# Client ID
n96144250-55b41d4f-c6a6-4bd6

# Client Secret
9a92a379-1210-47d0-bf0c-b9cf0e2414a3
```

### 完整程式碼

```py
"""
高雄捷運即時查詢系統
使用 TDX API：
1. Station/KRTC      - 車站基本資料與位置
2. LiveBoard/KRTC    - 即時到站時間
3. Station + LiveBoard - 車站地圖與即時到站資訊

執行：
uv run streamlit run kaohsiung_metro_streamlit_fixed_v2.py
"""

import os
from datetime import datetime

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st


# =========================
# 基本設定
# =========================

st.set_page_config(
    page_title="高雄捷運即時查詢",
    page_icon="🚇",
    layout="wide",
)

TDX_TOKEN_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_BASE_URL = "https://tdx.transportdata.tw/api/basic/v2/Rail/Metro"

STATION_API = f"{TDX_BASE_URL}/Station/KRTC"
LIVE_BOARD_API = f"{TDX_BASE_URL}/LiveBoard/KRTC"


# =========================
# CSS
# =========================

st.markdown(
    """
    <style>
    :root {
        --page-bg: #0e1117;
        --card-bg: #161b22;
        --card-border: #30363d;
        --text-main: #f0f6fc;
        --text-muted: #9da7b3;
        --red-line: #e53935;
        --orange-line: #ff9800;
        --green: #2ecc71;
        --blue: #58a6ff;
    }

    .main-title {
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 0;
        color: var(--text-main);
    }

    .subtitle {
        color: var(--text-muted);
        font-size: 17px;
        margin-bottom: 24px;
    }

    .station-title {
        font-size: 28px;
        font-weight: 850;
        color: var(--text-main);
        margin-bottom: 8px;
    }

    .direction-title {
        font-size: 24px;
        font-weight: 800;
        color: var(--text-main);
        margin: 8px 0 12px 0;
    }

    .metro-card {
        padding: 18px 20px;
        border: 1px solid var(--card-border);
        border-radius: 16px;
        margin-bottom: 12px;
        background: var(--card-bg);
        color: var(--text-main);
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.18);
    }

    .line-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        color: white;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .line-red { background: var(--red-line); }
    .line-orange { background: var(--orange-line); color: #1a1a1a; }
    .line-other { background: #6b7280; }

    .arrive-now {
        font-size: 25px;
        font-weight: 900;
        color: var(--green);
        margin: 2px 0 4px 0;
    }

    .estimate-time {
        font-size: 25px;
        font-weight: 900;
        color: var(--blue);
        margin: 2px 0 4px 0;
    }

    .small-text {
        color: var(--text-muted);
        font-size: 14px;
    }

    /* 避免深色模式下卡片文字變成白底白字 */
    .metro-card strong,
    .metro-card div,
    .metro-card span {
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# TDX 認證
# =========================

def get_setting(name: str, default: str = "") -> str:
    """
    讀取順序：
    1. Streamlit secrets
    2. 環境變數
    3. 預設值
    """
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass

    return os.getenv(name, default)


@st.cache_data(ttl=1200, show_spinner=False)
def get_access_token(client_id: str, client_secret: str) -> str:
    """使用 Client Credentials 取得 TDX Access Token。"""

    response = requests.post(
        TDX_TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=20,
    )

    response.raise_for_status()

    return response.json()["access_token"]


def get_headers(client_id: str, client_secret: str) -> dict:
    token = get_access_token(client_id, client_secret)

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


# =========================
# API
# =========================

def call_tdx_api(url: str, headers: dict, params: dict | None = None):
    response = requests.get(
        url,
        headers=headers,
        params=params or {"$format": "JSON"},
        timeout=20,
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=3600, show_spinner=False)
def get_stations(client_id: str, client_secret: str):
    """取得高雄捷運所有車站。"""

    headers = get_headers(client_id, client_secret)

    return call_tdx_api(
        STATION_API,
        headers,
        {
            "$top": 200,
            "$format": "JSON",
        },
    )


@st.cache_data(ttl=15, show_spinner=False)
def get_live_board(client_id: str, client_secret: str):
    """取得全高雄捷運即時到站資訊。"""

    headers = get_headers(client_id, client_secret)

    return call_tdx_api(
        LIVE_BOARD_API,
        headers,
        {
            "$top": 500,
            "$format": "JSON",
        },
    )




# =========================
# 資料整理
# =========================

def zh_name(value, default=""):
    if isinstance(value, dict):
        return value.get("Zh_tw") or value.get("En") or default
    return value or default


def normalize_station_data(data):
    rows = []

    for item in data:
        position = item.get("StationPosition", {}) or {}

        lat = (
            position.get("PositionLat")
            or item.get("PositionLat")
            or item.get("Latitude")
        )

        lon = (
            position.get("PositionLon")
            or item.get("PositionLon")
            or item.get("Longitude")
        )

        station_id = item.get("StationID", "")
        station_name = zh_name(item.get("StationName"))
        line_id = item.get("LineID") or item.get("LineNO") or ""

        rows.append(
            {
                "StationID": station_id,
                "StationName": station_name,
                "LineID": line_id,
                "Lat": lat,
                "Lon": lon,
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.drop_duplicates(subset=["StationID"])
        df["Lat"] = pd.to_numeric(df["Lat"], errors="coerce")
        df["Lon"] = pd.to_numeric(df["Lon"], errors="coerce")

    return df


def normalize_live_board(data):
    rows = []

    for item in data:
        estimate_time = item.get("EstimateTime")

        try:
            estimate_time = int(estimate_time)
        except (TypeError, ValueError):
            estimate_time = None

        rows.append(
            {
                "LineID": item.get("LineID") or item.get("LineNO") or "",
                "LineName": zh_name(item.get("LineName")),
                "StationID": item.get("StationID", ""),
                "StationName": zh_name(item.get("StationName")),
                "Direction": item.get("TripHeadSign", ""),
                "Destination": zh_name(item.get("DestinationStationName")),
                "EstimateTime": estimate_time,
                "ServiceStatus": item.get("ServiceStatus"),
                "UpdateTime": item.get("UpdateTime", ""),
            }
        )

    return pd.DataFrame(rows)



def format_estimate_time(minutes):
    if minutes is None or pd.isna(minutes):
        return "暫無資料"

    minutes = int(minutes)

    if minutes <= 0:
        return "🚇 進站中"

    if minutes == 1:
        return "約 1 分鐘"

    return f"約 {minutes} 分鐘"


def line_name_from_id(line_id: str) -> str:
    if line_id == "R":
        return "紅線"
    if line_id == "O":
        return "橘線"
    return line_id or "未知路線"


def line_badge_class(line_id: str) -> str:
    if line_id == "R":
        return "line-red"
    if line_id == "O":
        return "line-orange"
    return "line-other"


def station_sort_key(station_id: str):
    """讓 R3、R4、R4A、...、R24、RK1 / O1、O2、...、OT1 依路線順序排列。"""
    special = {"RK1": 999, "OT1": 999}
    if station_id in special:
        return special[station_id]

    import re
    match = re.match(r"^[RO](\d+)([A-Z]?)$", station_id or "")
    if not match:
        return 10000

    number = int(match.group(1))
    suffix = match.group(2)
    return number * 10 + (1 if suffix else 0)


# =========================
# Sidebar
# =========================

st.markdown('<div class="main-title">🚇 高雄捷運即時查詢</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">查詢車站即時到站時間，並在地圖查看各捷運站位置</div>',
    unsafe_allow_html=True,
)

default_client_id = get_setting("TDX_CLIENT_ID")
default_client_secret = get_setting("TDX_CLIENT_SECRET")

with st.sidebar:
    st.header("⚙️ TDX API 設定")

    client_id = st.text_input(
        "Client ID",
        value=default_client_id,
        type="default",
    )

    client_secret = st.text_input(
        "Client Secret",
        value=default_client_secret,
        type="password",
    )

    st.caption(
        "也可以放在 .streamlit/secrets.toml："
        "TDX_CLIENT_ID、TDX_CLIENT_SECRET"
    )

    auto_refresh = st.toggle(
        "每 15 秒重新讀取即時資料",
        value=False,
    )

    if st.button("🔄 立即重新整理", use_container_width=True):
        get_live_board.clear()
        st.rerun()


# =========================
# 檢查 API Key
# =========================

if not client_id or not client_secret:
    st.warning(
        "請先在左側輸入 TDX Client ID 與 Client Secret。"
    )

    st.code(
        """
# .streamlit/secrets.toml

TDX_CLIENT_ID = "你的 Client ID"
TDX_CLIENT_SECRET = "你的 Client Secret"
        """.strip(),
        language="toml",
    )

    st.stop()


# =========================
# 讀取資料
# =========================

try:
    station_raw = get_stations(client_id, client_secret)
    live_board_raw = get_live_board(client_id, client_secret)

    station_df = normalize_station_data(station_raw)
    live_df = normalize_live_board(live_board_raw)

except requests.HTTPError as e:
    st.error(f"TDX API 回傳錯誤：{e}")
    st.stop()

except requests.RequestException as e:
    st.error(f"連線 TDX 失敗：{e}")
    st.stop()

except Exception as e:
    st.error(f"資料處理發生錯誤：{e}")
    st.stop()


# =========================
# 查詢區
# =========================

tab1, tab2, tab3 = st.tabs(
    [
        "🚉 即時到站",
        "🗺️ 捷運地圖",
        "📋 全站即時資訊",
    ]
)


# =========================
# TAB 1：即時到站
# =========================

with tab1:

    line_options = ["全部", "紅線", "橘線"]

    selected_line = st.selectbox(
        "選擇路線",
        line_options,
    )

    station_options_df = station_df.copy()

    if selected_line == "紅線":
        station_options_df = station_options_df[
            station_options_df["StationID"].str.startswith("R", na=False)
        ]

    elif selected_line == "橘線":
        station_options_df = station_options_df[
            station_options_df["StationID"].str.startswith("O", na=False)
        ]

    station_options_df = station_options_df.sort_values("StationID")

    station_dict = {
        f'{row["StationID"]}｜{row["StationName"]}': row["StationID"]
        for _, row in station_options_df.iterrows()
    }

    if not station_dict:
        st.info("目前沒有可選擇的車站。")
    else:
        selected_station_label = st.selectbox(
            "選擇車站",
            list(station_dict.keys()),
        )

        selected_station_id = station_dict[selected_station_label]

        station_info = station_df[
            station_df["StationID"] == selected_station_id
        ]

        station_name = (
            station_info.iloc[0]["StationName"]
            if not station_info.empty
            else selected_station_id
        )

        station_live = live_df[
            live_df["StationID"] == selected_station_id
        ].copy()

        station_live = station_live.sort_values(
            ["Direction", "EstimateTime"],
            na_position="last",
        )

        st.markdown("---")
        st.markdown(
            f'<div class="station-title">🚉 {station_name} ({selected_station_id})</div>',
            unsafe_allow_html=True,
        )

        if station_live.empty:
            st.info("目前這個車站沒有即時到站資料。")

        else:
            directions = station_live["Direction"].fillna("").unique()

            columns = st.columns(max(1, min(2, len(directions))))

            for index, direction in enumerate(directions):
                direction_df = station_live[
                    station_live["Direction"] == direction
                ].copy()

                with columns[index % len(columns)]:
                    st.markdown(
                        f'<div class="direction-title">{direction or "方向未提供"}</div>',
                        unsafe_allow_html=True,
                    )

                    for _, train in direction_df.iterrows():
                        estimate_text = format_estimate_time(
                            train["EstimateTime"]
                        )

                        if train["EstimateTime"] == 0:
                            css_class = "arrive-now"
                        else:
                            css_class = "estimate-time"

                        badge_class = line_badge_class(train["LineID"])
                        line_label = train["LineName"] or line_name_from_id(train["LineID"])

                        st.markdown(
                            f"""
                            <div class="metro-card">
                                <div class="line-badge {badge_class}">{line_label}</div>
                                <div class="{css_class}">{estimate_text}</div>
                                <div class="small-text">終點：{train["Destination"] or "-"}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            update_values = station_live["UpdateTime"].dropna()

            if not update_values.empty:
                st.caption(f"資料更新時間：{update_values.iloc[0]}")


# =========================
# TAB 2：捷運地圖
# =========================

with tab2:

    st.subheader("🗺️ 高雄捷運車站地圖")
    map_station_df = station_df.dropna(
        subset=["Lat", "Lon"]
    ).copy()

    if map_station_df.empty:
        st.warning("Station API 沒有取得可用的經緯度資料。")

    else:
        # 把目前各站最近一班車資訊合併到地圖 tooltip
        nearest_rows = []

        for station_id, group in live_df.groupby("StationID"):
            group = group.copy()
            group = group.sort_values("EstimateTime", na_position="last")

            parts = []
            for _, row in group.head(2).iterrows():
                parts.append(
                    f'{row["Direction"]}：{format_estimate_time(row["EstimateTime"])}'
                )

            nearest_rows.append(
                {
                    "StationID": station_id,
                    "ArrivalInfo": " / ".join(parts) if parts else "暫無即時資料",
                }
            )

        arrival_df = pd.DataFrame(nearest_rows)

        map_station_df = map_station_df.merge(
            arrival_df,
            on="StationID",
            how="left",
        )

        map_station_df["ArrivalInfo"] = map_station_df["ArrivalInfo"].fillna(
            "暫無即時資料"
        )

        map_station_df["Type"] = "捷運站"
        map_station_df["Name"] = (
            map_station_df["StationID"]
            + " "
            + map_station_df["StationName"]
        )

        # 依紅線 / 橘線設定顏色
        map_station_df["Color"] = map_station_df["StationID"].apply(
            lambda sid: [229, 57, 53, 220]
            if str(sid).startswith("R")
            else [255, 152, 0, 220]
        )

        # 依實際車站順序建立兩條捷運路線
        path_rows = []
        for prefix, line_name, color in [
            ("R", "紅線", [229, 57, 53, 220]),
            ("O", "橘線", [255, 152, 0, 220]),
        ]:
            line_df = map_station_df[
                map_station_df["StationID"].astype(str).str.startswith(prefix)
            ].copy()

            line_df["SortKey"] = line_df["StationID"].apply(station_sort_key)
            line_df = line_df.sort_values("SortKey")

            if len(line_df) >= 2:
                path_rows.append(
                    {
                        "LineName": line_name,
                        "Path": line_df[["Lon", "Lat"]].values.tolist(),
                        "Color": color,
                    }
                )

        path_layer = pdk.Layer(
            "PathLayer",
            data=pd.DataFrame(path_rows),
            get_path="Path",
            get_color="Color",
            get_width=7,
            width_min_pixels=4,
            pickable=False,
        )

        station_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_station_df,
            get_position="[Lon, Lat]",
            get_fill_color="Color",
            get_line_color=[255, 255, 255, 220],
            stroked=True,
            line_width_min_pixels=2,
            get_radius=95,
            pickable=True,
            auto_highlight=True,
        )

        center_lat = map_station_df["Lat"].mean()
        center_lon = map_station_df["Lon"].mean()

        deck = pdk.Deck(
            map_style="dark",
            initial_view_state=pdk.ViewState(
                latitude=center_lat,
                longitude=center_lon,
                zoom=10.8,
                pitch=0,
            ),
            layers=[path_layer, station_layer],
            tooltip={
                "html": "<b>{Name}</b><br>{ArrivalInfo}",
                "style": {
                    "backgroundColor": "#161b22",
                    "color": "#f0f6fc",
                },
            },
        )

        st.pydeck_chart(
            deck,
            use_container_width=True,
        )

        st.caption(
            "🔴 紅色為紅線、🟠 橘色為橘線。把滑鼠移到車站上，可查看該站最近的即時到站資訊。"
        )


# =========================
# TAB 3：全站即時資訊
# =========================

with tab3:

    st.subheader("📋 全站即時到站")

    display_df = live_df.copy()

    display_df["預估到站"] = display_df["EstimateTime"].apply(
        format_estimate_time
    )

    display_df = display_df[
        [
            "LineName",
            "StationID",
            "StationName",
            "Direction",
            "Destination",
            "預估到站",
            "UpdateTime",
        ]
    ]

    display_df.columns = [
        "路線",
        "車站代碼",
        "車站",
        "方向",
        "終點",
        "預估到站",
        "更新時間",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# =========================
# 自動更新
# =========================

if auto_refresh:
    st.caption("🔄 已開啟每 15 秒自動更新")

    import time

    time.sleep(15)

    get_live_board.clear()

    st.rerun()
```
