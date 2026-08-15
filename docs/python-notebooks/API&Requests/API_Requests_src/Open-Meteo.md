Open-Meteo 提供各種氣象資料 API，讓你用程式直接取得：

- 即時天氣(Current Weather)
- 小時預報(Hourly Forecast)
- 每日預報(Daily Forecast)
- 歷史天氣(Historical Weather)
- 空氣品質(Air Quality)
- 海浪資料(Marine Weather)
- 地理編碼(城市名稱轉經緯度)

## 台灣即時天氣查詢系統

### 提示詞

```text
請使用 **Python + Streamlit** 製作一個「台灣即時天氣查詢系統」，天氣資料使用 **Open-Meteo API**。

### 功能需求

**1. 台灣地圖查詢**

* 首頁顯示台灣地圖。
* 可以選擇「縣市 → 行政區」。
* 選擇行政區後，自動查詢該地區天氣。

**2. 天氣資訊**

提供三種查詢模式：

* 🌤️ **即時天氣**

  * 目前氣溫
  * 體感溫度
  * 濕度
  * 降雨量
  * 風速

* 🌧️ **未來 24 小時**

  * 每小時氣溫
  * 降雨機率
  * 降雨量
  * 使用圖表呈現

* 📅 **未來一週**

  * 每日最高溫、最低溫
  * 天氣狀況
  * 降雨機率
  * 降雨量

**3. 經緯度查詢**

讓使用者可以直接輸入：

* Latitude
* Longitude

輸入後顯示該座標的即時、24 小時及一週天氣。

**4. 我的最愛**

* 可以將目前查詢地點加入最愛。
* 可以自行設定名稱，例如「家裡」、「公司」。
* 下次點擊最愛地點即可直接查看天氣。
* 可以刪除最愛地點。

### 介面設計

希望做成簡潔、現代化的 Weather Dashboard。

上方顯示目前天氣資訊，下方使用：

`🌤️ 即時`｜`🌧️ 24 小時`｜`📅 一週`

三個頁籤切換。

側邊欄放：

* 縣市 / 行政區選擇
* 經緯度查詢
* 我的最愛
```

### 完整程式碼

```py

import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


# =========================================================
# 基本設定
# =========================================================

st.set_page_config(
    page_title="台灣即時天氣查詢系統",
    page_icon="🌤️",
    layout="wide",
)

WEATHER_API = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
NOMINATIM_API = "https://nominatim.openstreetmap.org/search"
FAVORITES_FILE = Path("favorites.json")


# =========================================================
# 台灣縣市 / 行政區資料
# =========================================================

TAIWAN_DISTRICTS = {
    "臺北市": [
        "中正區", "大同區", "中山區", "松山區", "大安區", "萬華區",
        "信義區", "士林區", "北投區", "內湖區", "南港區", "文山區"
    ],
    "新北市": [
        "板橋區", "三重區", "中和區", "永和區", "新莊區", "新店區",
        "樹林區", "鶯歌區", "三峽區", "淡水區", "汐止區", "瑞芳區",
        "土城區", "蘆洲區", "五股區", "泰山區", "林口區", "深坑區",
        "石碇區", "坪林區", "三芝區", "石門區", "八里區", "平溪區",
        "雙溪區", "貢寮區", "金山區", "萬里區", "烏來區"
    ],
    "桃園市": [
        "桃園區", "中壢區", "平鎮區", "八德區", "楊梅區", "蘆竹區",
        "大溪區", "龍潭區", "龜山區", "大園區", "觀音區", "新屋區",
        "復興區"
    ],
    "臺中市": [
        "中區", "東區", "南區", "西區", "北區", "西屯區", "南屯區",
        "北屯區", "豐原區", "東勢區", "大甲區", "清水區", "沙鹿區",
        "梧棲區", "后里區", "神岡區", "潭子區", "大雅區", "新社區",
        "石岡區", "外埔區", "大安區", "烏日區", "大肚區", "龍井區",
        "霧峰區", "太平區", "大里區", "和平區"
    ],
    "臺南市": [
        "中西區", "東區", "南區", "北區", "安平區", "安南區", "永康區",
        "歸仁區", "新化區", "左鎮區", "玉井區", "楠西區", "南化區",
        "仁德區", "關廟區", "龍崎區", "官田區", "麻豆區", "佳里區",
        "西港區", "七股區", "將軍區", "學甲區", "北門區", "新營區",
        "後壁區", "白河區", "東山區", "六甲區", "下營區", "柳營區",
        "鹽水區", "善化區", "大內區", "山上區", "新市區", "安定區"
    ],
    "高雄市": [
        "楠梓區", "左營區", "鼓山區", "三民區", "鹽埕區", "前金區",
        "新興區", "苓雅區", "前鎮區", "旗津區", "小港區", "鳳山區",
        "林園區", "大寮區", "大樹區", "大社區", "仁武區", "鳥松區",
        "岡山區", "橋頭區", "燕巢區", "田寮區", "阿蓮區", "路竹區",
        "湖內區", "茄萣區", "永安區", "彌陀區", "梓官區", "旗山區",
        "美濃區", "六龜區", "甲仙區", "杉林區", "內門區", "茂林區",
        "桃源區", "那瑪夏區"
    ],
    "基隆市": ["仁愛區", "信義區", "中正區", "中山區", "安樂區", "暖暖區", "七堵區"],
    "新竹市": ["東區", "北區", "香山區"],
    "嘉義市": ["東區", "西區"],
    "新竹縣": [
        "竹北市", "竹東鎮", "新埔鎮", "關西鎮", "湖口鄉", "新豐鄉",
        "芎林鄉", "橫山鄉", "北埔鄉", "寶山鄉", "峨眉鄉", "尖石鄉", "五峰鄉"
    ],
    "苗栗縣": [
        "苗栗市", "頭份市", "苑裡鎮", "通霄鎮", "竹南鎮", "後龍鎮",
        "卓蘭鎮", "大湖鄉", "公館鄉", "銅鑼鄉", "南庄鄉", "頭屋鄉",
        "三義鄉", "西湖鄉", "造橋鄉", "三灣鄉", "獅潭鄉", "泰安鄉"
    ],
    "彰化縣": [
        "彰化市", "員林市", "和美鎮", "鹿港鎮", "溪湖鎮", "二林鎮",
        "田中鎮", "北斗鎮", "花壇鄉", "芬園鄉", "大村鄉", "永靖鄉",
        "伸港鄉", "線西鄉", "福興鄉", "秀水鄉", "埔心鄉", "埔鹽鄉",
        "大城鄉", "芳苑鄉", "竹塘鄉", "社頭鄉", "二水鄉", "田尾鄉",
        "埤頭鄉", "溪州鄉"
    ],
    "南投縣": [
        "南投市", "埔里鎮", "草屯鎮", "竹山鎮", "集集鎮", "名間鄉",
        "鹿谷鄉", "中寮鄉", "魚池鄉", "國姓鄉", "水里鄉", "信義鄉", "仁愛鄉"
    ],
    "雲林縣": [
        "斗六市", "斗南鎮", "虎尾鎮", "西螺鎮", "土庫鎮", "北港鎮",
        "古坑鄉", "大埤鄉", "莿桐鄉", "林內鄉", "二崙鄉", "崙背鄉",
        "麥寮鄉", "東勢鄉", "褒忠鄉", "臺西鄉", "元長鄉", "四湖鄉",
        "口湖鄉", "水林鄉"
    ],
    "嘉義縣": [
        "太保市", "朴子市", "布袋鎮", "大林鎮", "民雄鄉", "溪口鄉",
        "新港鄉", "六腳鄉", "東石鄉", "義竹鄉", "鹿草鄉", "水上鄉",
        "中埔鄉", "竹崎鄉", "梅山鄉", "番路鄉", "大埔鄉", "阿里山鄉"
    ],
    "屏東縣": [
        "屏東市", "潮州鎮", "東港鎮", "恆春鎮", "萬丹鄉", "長治鄉",
        "麟洛鄉", "九如鄉", "里港鄉", "鹽埔鄉", "高樹鄉", "萬巒鄉",
        "內埔鄉", "竹田鄉", "新埤鄉", "枋寮鄉", "新園鄉", "崁頂鄉",
        "林邊鄉", "南州鄉", "佳冬鄉", "琉球鄉", "車城鄉", "滿州鄉",
        "枋山鄉", "三地門鄉", "霧臺鄉", "瑪家鄉", "泰武鄉", "來義鄉",
        "春日鄉", "獅子鄉", "牡丹鄉"
    ],
    "宜蘭縣": [
        "宜蘭市", "羅東鎮", "蘇澳鎮", "頭城鎮", "礁溪鄉", "壯圍鄉",
        "員山鄉", "冬山鄉", "五結鄉", "三星鄉", "大同鄉", "南澳鄉"
    ],
    "花蓮縣": [
        "花蓮市", "鳳林鎮", "玉里鎮", "新城鄉", "吉安鄉", "壽豐鄉",
        "光復鄉", "豐濱鄉", "瑞穗鄉", "富里鄉", "秀林鄉", "萬榮鄉", "卓溪鄉"
    ],
    "臺東縣": [
        "臺東市", "成功鎮", "關山鎮", "卑南鄉", "鹿野鄉", "池上鄉",
        "東河鄉", "長濱鄉", "太麻里鄉", "大武鄉", "綠島鄉", "海端鄉",
        "延平鄉", "金峰鄉", "達仁鄉", "蘭嶼鄉"
    ],
    "澎湖縣": ["馬公市", "湖西鄉", "白沙鄉", "西嶼鄉", "望安鄉", "七美鄉"],
    "金門縣": ["金城鎮", "金湖鎮", "金沙鎮", "金寧鄉", "烈嶼鄉", "烏坵鄉"],
    "連江縣": ["南竿鄉", "北竿鄉", "莒光鄉", "東引鄉"],
}


# =========================================================
# 天氣代碼
# =========================================================

WEATHER_CODES = {
    0: ("☀️", "晴朗"),
    1: ("🌤️", "大致晴朗"),
    2: ("⛅", "局部多雲"),
    3: ("☁️", "陰天"),
    45: ("🌫️", "有霧"),
    48: ("🌫️", "霧凇"),
    51: ("🌦️", "小毛毛雨"),
    53: ("🌦️", "毛毛雨"),
    55: ("🌧️", "強毛毛雨"),
    56: ("🌧️", "凍毛毛雨"),
    57: ("🌧️", "強凍毛毛雨"),
    61: ("🌦️", "小雨"),
    63: ("🌧️", "中雨"),
    65: ("🌧️", "大雨"),
    66: ("🌧️", "凍雨"),
    67: ("🌧️", "強凍雨"),
    71: ("🌨️", "小雪"),
    73: ("🌨️", "中雪"),
    75: ("❄️", "大雪"),
    77: ("🌨️", "雪粒"),
    80: ("🌦️", "小陣雨"),
    81: ("🌧️", "中陣雨"),
    82: ("⛈️", "強陣雨"),
    85: ("🌨️", "小陣雪"),
    86: ("❄️", "強陣雪"),
    95: ("⛈️", "雷雨"),
    96: ("⛈️", "雷雨伴小冰雹"),
    99: ("⛈️", "雷雨伴大冰雹"),
}


def weather_text(code):
    return WEATHER_CODES.get(int(code), ("🌡️", "未知天氣"))


# =========================================================
# API
# =========================================================

@st.cache_data(ttl=86400)
def geocode_location(city, district):
    """
    將台灣行政區轉成經緯度。

    台灣有大量「東區、北區、中正區」等重複行政區名稱，
    單獨交給 Open-Meteo Geocoding 容易找不到或找錯地方。

    因此採用：
    1. OpenStreetMap Nominatim：用「行政區 + 縣市 + 台灣」精準定位
    2. Open-Meteo Geocoding：作為備援
    """

    normalized_city = city.replace("臺", "台")
    normalized_district = district.replace("臺", "台")

    # -----------------------------------------------------
    # 方法 1：OpenStreetMap Nominatim
    # -----------------------------------------------------
    nominatim_queries = [
        f"{district}, {city}, 台灣",
        f"{normalized_district}, {normalized_city}, 台灣",
        f"{city}{district}, 台灣",
    ]

    headers = {
        "User-Agent": "TaiwanWeatherDashboard/1.0"
    }

    for query in nominatim_queries:
        try:
            response = requests.get(
                NOMINATIM_API,
                params={
                    "q": query,
                    "format": "jsonv2",
                    "limit": 10,
                    "countrycodes": "tw",
                    "addressdetails": 1,
                },
                headers=headers,
                timeout=12,
            )
            response.raise_for_status()
            results = response.json()

            for item in results:
                display_name = item.get("display_name", "")
                normalized_display = display_name.replace("臺", "台")

                city_ok = normalized_city.replace("市", "").replace("縣", "") in normalized_display
                district_core = (
                    normalized_district
                    .replace("區", "")
                    .replace("鄉", "")
                    .replace("鎮", "")
                    .replace("市", "")
                )
                district_ok = district_core in normalized_display

                if city_ok and district_ok:
                    return {
                        "latitude": float(item["lat"]),
                        "longitude": float(item["lon"]),
                        "source": "OpenStreetMap",
                    }

            # 若只有一筆結果，也接受，但仍需確認縣市
            for item in results:
                normalized_display = item.get("display_name", "").replace("臺", "台")
                city_core = normalized_city.replace("市", "").replace("縣", "")
                if city_core in normalized_display:
                    return {
                        "latitude": float(item["lat"]),
                        "longitude": float(item["lon"]),
                        "source": "OpenStreetMap",
                    }

        except (requests.RequestException, ValueError, TypeError):
            pass

    # -----------------------------------------------------
    # 方法 2：Open-Meteo Geocoding 備援
    # -----------------------------------------------------
    aliases = {
        "臺北市": "Taipei",
        "新北市": "New Taipei",
        "桃園市": "Taoyuan",
        "臺中市": "Taichung",
        "臺南市": "Tainan",
        "高雄市": "Kaohsiung",
        "基隆市": "Keelung",
        "新竹市": "Hsinchu",
        "嘉義市": "Chiayi",
        "新竹縣": "Hsinchu County",
        "苗栗縣": "Miaoli",
        "彰化縣": "Changhua",
        "南投縣": "Nantou",
        "雲林縣": "Yunlin",
        "嘉義縣": "Chiayi County",
        "屏東縣": "Pingtung",
        "宜蘭縣": "Yilan",
        "花蓮縣": "Hualien",
        "臺東縣": "Taitung",
        "澎湖縣": "Penghu",
        "金門縣": "Kinmen",
        "連江縣": "Lienchiang",
    }

    district_core = (
        district
        .replace("區", "")
        .replace("鄉", "")
        .replace("鎮", "")
        .replace("市", "")
    )

    candidates = [
        f"{district_core} {aliases.get(city, city)}",
        f"{district} {aliases.get(city, city)}",
        aliases.get(city, city),
    ]

    for query in candidates:
        try:
            response = requests.get(
                GEOCODING_API,
                params={
                    "name": query,
                    "count": 20,
                    "language": "zh",
                    "format": "json",
                    "countryCode": "TW",
                },
                timeout=12,
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            if not results:
                continue

            city_core = normalized_city.replace("市", "").replace("縣", "")
            district_core_norm = normalized_district.replace("區", "").replace("鄉", "").replace("鎮", "").replace("市", "")

            # 同時比對縣市與行政區，避免「東區」跑到錯的縣市
            for item in results:
                all_admin = " ".join(
                    str(item.get(key, ""))
                    for key in ["name", "admin1", "admin2", "admin3", "admin4"]
                ).replace("臺", "台")

                if city_core in all_admin and district_core_norm in all_admin:
                    return {
                        "latitude": float(item["latitude"]),
                        "longitude": float(item["longitude"]),
                        "source": "Open-Meteo",
                    }

        except (requests.RequestException, ValueError, TypeError):
            pass

    return None


@st.cache_data(ttl=600)
def get_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "Asia/Taipei",
        "forecast_days": 7,
        "current": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
        ]),
        "hourly": ",".join([
            "temperature_2m",
            "precipitation_probability",
            "precipitation",
            "weather_code",
        ]),
        "daily": ",".join([
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "precipitation_sum",
        ]),
    }

    response = requests.get(WEATHER_API, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


# =========================================================
# 我的最愛
# =========================================================

def load_favorites():
    if not FAVORITES_FILE.exists():
        return {}

    try:
        return json.loads(FAVORITES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_favorites(data):
    FAVORITES_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


if "favorites" not in st.session_state:
    st.session_state.favorites = load_favorites()

if "location_name" not in st.session_state:
    st.session_state.location_name = "高雄市 三民區"

if "latitude" not in st.session_state:
    st.session_state.latitude = 22.6499

if "longitude" not in st.session_state:
    st.session_state.longitude = 120.3179


def set_location(name, latitude, longitude):
    st.session_state.location_name = name
    st.session_state.latitude = float(latitude)
    st.session_state.longitude = float(longitude)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

.weather-title {
    font-size: 2.15rem;
    font-weight: 800;
    margin-bottom: 0.15rem;
}

.location-subtitle {
    color: #6b7280;
    margin-bottom: 1.5rem;
}

.weather-hero {
    padding: 1.5rem;
    border: 1px solid rgba(128,128,128,0.18);
    border-radius: 22px;
    background: rgba(128,128,128,0.05);
    margin-bottom: 1rem;
}

.big-temp {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
}

.weather-status {
    font-size: 1.2rem;
    margin-top: 0.5rem;
}

.favorite-card {
    padding: 0.8rem 1rem;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.18);
    margin-bottom: 0.5rem;
}

[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.15);
    padding: 14px;
    border-radius: 15px;
    background: rgba(128,128,128,0.03);
    min-width: 0;
}

[data-testid="stMetricValue"] {
    font-size: clamp(1.45rem, 1.8vw, 2rem) !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

[data-testid="stMetricLabel"] {
    white-space: nowrap !important;
}

@media (max-width: 1100px) {
    [data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:
    st.header("🔎 地點查詢")

    query_mode = st.radio(
        "查詢方式",
        ["縣市 / 行政區", "經緯度"],
        horizontal=True,
    )

    if query_mode == "縣市 / 行政區":
        city = st.selectbox("縣市", list(TAIWAN_DISTRICTS.keys()), index=5)
        district = st.selectbox("行政區", TAIWAN_DISTRICTS[city])

        if st.button("查詢行政區天氣", use_container_width=True, type="primary"):
            with st.spinner("正在定位行政區..."):
                result = geocode_location(city, district)

            if result:
                set_location(
                    f"{city} {district}",
                    result["latitude"],
                    result["longitude"],
                )
                st.success(f"已定位：{city} {district}")
                st.rerun()
            else:
                st.error(
                    f"暫時無法定位「{city} {district}」。"
                    "請稍後再試，或改用經緯度查詢。"
                )

    else:
        latitude_input = st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=float(st.session_state.latitude),
            format="%.6f",
        )

        longitude_input = st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=float(st.session_state.longitude),
            format="%.6f",
        )

        custom_name = st.text_input("地點名稱", value="自訂座標")

        if st.button("查詢座標天氣", use_container_width=True, type="primary"):
            set_location(custom_name or "自訂座標", latitude_input, longitude_input)
            st.rerun()

    st.divider()
    st.subheader("⭐ 我的最愛")

    favorites = st.session_state.favorites

    if favorites:
        for fav_name, fav in list(favorites.items()):
            c1, c2 = st.columns([4, 1])

            with c1:
                if st.button(
                    fav_name,
                    key=f"open_{fav_name}",
                    use_container_width=True
                ):
                    set_location(
                        fav_name,
                        fav["latitude"],
                        fav["longitude"],
                    )
                    st.rerun()

            with c2:
                if st.button("🗑️", key=f"delete_{fav_name}"):
                    del st.session_state.favorites[fav_name]
                    save_favorites(st.session_state.favorites)
                    st.rerun()
    else:
        st.caption("目前還沒有最愛地點。")


# =========================================================
# 取得天氣
# =========================================================

lat = st.session_state.latitude
lon = st.session_state.longitude
location_name = st.session_state.location_name

try:
    weather = get_weather(lat, lon)
except requests.RequestException as exc:
    st.error(f"Open-Meteo API 查詢失敗：{exc}")
    st.stop()


current = weather["current"]
current_units = weather.get("current_units", {})
icon, status = weather_text(current["weather_code"])


# =========================================================
# Header
# =========================================================

head_col, fav_col = st.columns([4, 1])

with head_col:
    st.markdown(
        f'<div class="weather-title">🌤️ 台灣即時天氣查詢系統</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="location-subtitle">📍 {location_name} ｜ '
        f'{lat:.5f}, {lon:.5f}</div>',
        unsafe_allow_html=True
    )

with fav_col:
    with st.popover("⭐ 加入最愛", use_container_width=True):
        fav_name = st.text_input(
            "自訂名稱",
            value=location_name,
            key="favorite_name",
        )

        if st.button("儲存最愛", use_container_width=True):
            name = fav_name.strip()

            if not name:
                st.warning("請輸入最愛名稱。")
            else:
                st.session_state.favorites[name] = {
                    "latitude": lat,
                    "longitude": lon,
                }
                save_favorites(st.session_state.favorites)
                st.success(f"已加入：{name}")


# =========================================================
# 目前天氣 Hero
# =========================================================

st.markdown('<div class="weather-hero">', unsafe_allow_html=True)

left, right = st.columns([1.0, 3.4], vertical_alignment="center")

with left:
    st.markdown(
        f'<div class="big-temp">{current["temperature_2m"]:.1f}°</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="weather-status">{icon} {status}</div>',
        unsafe_allow_html=True
    )

with right:
    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "體感溫度",
        f'{current["apparent_temperature"]:.1f} °C'
    )
    m2.metric(
        "相對濕度",
        f'{current["relative_humidity_2m"]:.0f} %'
    )
    m3.metric(
        "目前降雨",
        f'{current["precipitation"]:.1f} mm'
    )
    m4.metric(
        "風速",
        f'{current["wind_speed_10m"]:.1f} km/h'
    )

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 地圖
# =========================================================

with st.expander("🗺️ 查看目前位置", expanded=False):
    map_df = pd.DataFrame({
        "lat": [lat],
        "lon": [lon],
    })
    st.map(map_df, latitude="lat", longitude="lon", zoom=11)


# =========================================================
# Tabs
# =========================================================

tab_current, tab_24h, tab_week = st.tabs(
    ["🌤️ 即時", "🌧️ 24 小時", "📅 一週"]
)


# -------------------------
# 即時
# -------------------------

with tab_current:
    st.subheader(f"{icon} {status}")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("目前氣溫", f'{current["temperature_2m"]:.1f} °C')
    c2.metric("體感溫度", f'{current["apparent_temperature"]:.1f} °C')
    c3.metric("濕度", f'{current["relative_humidity_2m"]:.0f} %')
    c4.metric("降雨量", f'{current["precipitation"]:.1f} mm')
    c5.metric("風速", f'{current["wind_speed_10m"]:.1f} km/h')

    st.caption(f'資料時間：{current["time"]} (Asia/Taipei)')


# -------------------------
# 24 小時
# -------------------------

with tab_24h:
    hourly = pd.DataFrame(weather["hourly"])
    hourly["time"] = pd.to_datetime(hourly["time"])

    now_tw = pd.Timestamp.now(tz="Asia/Taipei").tz_localize(None)
    future_24 = hourly[hourly["time"] >= now_tw.floor("h")].head(24).copy()

    st.subheader("未來 24 小時氣溫")

    fig_temp = go.Figure()
    fig_temp.add_trace(
        go.Scatter(
            x=future_24["time"],
            y=future_24["temperature_2m"],
            mode="lines+markers",
            name="氣溫",
            hovertemplate="%{x|%m/%d %H:%M}<br>%{y:.1f} °C<extra></extra>",
        )
    )
    fig_temp.update_layout(
        xaxis_title="時間",
        yaxis_title="氣溫 (°C)",
        margin=dict(l=10, r=10, t=20, b=10),
        height=350,
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    st.subheader("降雨機率 / 降雨量")

    fig_rain = go.Figure()

    fig_rain.add_trace(
        go.Bar(
            x=future_24["time"],
            y=future_24["precipitation"],
            name="降雨量 (mm)",
            yaxis="y",
            hovertemplate="%{x|%m/%d %H:%M}<br>%{y:.1f} mm<extra></extra>",
        )
    )

    fig_rain.add_trace(
        go.Scatter(
            x=future_24["time"],
            y=future_24["precipitation_probability"],
            name="降雨機率 (%)",
            mode="lines+markers",
            yaxis="y2",
            hovertemplate="%{x|%m/%d %H:%M}<br>%{y:.0f}%<extra></extra>",
        )
    )

    fig_rain.update_layout(
        yaxis=dict(title="降雨量 (mm)"),
        yaxis2=dict(
            title="降雨機率 (%)",
            overlaying="y",
            side="right",
            range=[0, 100],
        ),
        legend=dict(orientation="h"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=380,
    )

    st.plotly_chart(fig_rain, use_container_width=True)

    display_24 = future_24[
        ["time", "temperature_2m", "precipitation_probability", "precipitation"]
    ].copy()

    display_24.columns = ["時間", "氣溫 (°C)", "降雨機率 (%)", "降雨量 (mm)"]
    display_24["時間"] = display_24["時間"].dt.strftime("%m/%d %H:%M")

    with st.expander("查看 24 小時詳細資料"):
        st.dataframe(display_24, use_container_width=True, hide_index=True)


# -------------------------
# 一週
# -------------------------

with tab_week:
    daily = pd.DataFrame(weather["daily"])
    daily["time"] = pd.to_datetime(daily["time"])

    st.subheader("未來一週")

    for _, row in daily.iterrows():
        day_icon, day_status = weather_text(row["weather_code"])

        with st.container(border=True):
            date_col, weather_col, temp_col, rain_col = st.columns(
                [1.1, 1.5, 2, 2]
            )

            with date_col:
                st.markdown(
                    f"### {row['time'].strftime('%m/%d')}"
                )
                st.caption(
                    ["一", "二", "三", "四", "五", "六", "日"][
                        row["time"].weekday()
                    ]
                )

            with weather_col:
                st.markdown(f"### {day_icon}")
                st.write(day_status)

            with temp_col:
                st.write(
                    f"🌡️ **{row['temperature_2m_min']:.1f}°C "
                    f"～ {row['temperature_2m_max']:.1f}°C**"
                )

            with rain_col:
                rain_probability = row.get(
                    "precipitation_probability_max",
                    0,
                )
                rain_sum = row.get("precipitation_sum", 0)

                st.write(f"☔ 降雨機率：**{rain_probability:.0f}%**")
                st.write(f"💧 降雨量：**{rain_sum:.1f} mm**")

    fig_week = go.Figure()

    fig_week.add_trace(
        go.Scatter(
            x=daily["time"],
            y=daily["temperature_2m_max"],
            mode="lines+markers",
            name="最高溫",
        )
    )

    fig_week.add_trace(
        go.Scatter(
            x=daily["time"],
            y=daily["temperature_2m_min"],
            mode="lines+markers",
            name="最低溫",
        )
    )

    fig_week.update_layout(
        xaxis_title="日期",
        yaxis_title="氣溫 (°C)",
        legend=dict(orientation="h"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=350,
    )

    st.plotly_chart(fig_week, use_container_width=True)


# =========================================================
# Footer
# =========================================================

st.divider()
st.caption(
    "Weather data: Open-Meteo ｜ "
    "行政區定位使用 Open-Meteo Geocoding API ｜ "
    "時區：Asia/Taipei"
)
```
