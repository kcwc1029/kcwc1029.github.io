import streamlit as st
import requests
from deep_translator import GoogleTranslator


# =========================================================
# 1. 網頁基本設定
# =========================================================

st.set_page_config(
    page_title="星座運勢查詢",
    page_icon="🔮",
    layout="wide"
)


# =========================================================
# 2. 星座資料
# =========================================================

ZODIACS = {
    "♈ 牡羊座": {
        "sign": "aries",
        "date": "3/21－4/19",
        "symbol": "♈"
    },

    "♉ 金牛座": {
        "sign": "taurus",
        "date": "4/20－5/20",
        "symbol": "♉"
    },

    "♊ 雙子座": {
        "sign": "gemini",
        "date": "5/21－6/20",
        "symbol": "♊"
    },

    "♋ 巨蟹座": {
        "sign": "cancer",
        "date": "6/21－7/22",
        "symbol": "♋"
    },

    "♌ 獅子座": {
        "sign": "leo",
        "date": "7/23－8/22",
        "symbol": "♌"
    },

    "♍ 處女座": {
        "sign": "virgo",
        "date": "8/23－9/22",
        "symbol": "♍"
    },

    "♎ 天秤座": {
        "sign": "libra",
        "date": "9/23－10/22",
        "symbol": "♎"
    },

    "♏ 天蠍座": {
        "sign": "scorpio",
        "date": "10/23－11/21",
        "symbol": "♏"
    },

    "♐ 射手座": {
        "sign": "sagittarius",
        "date": "11/22－12/21",
        "symbol": "♐"
    },

    "♑ 摩羯座": {
        "sign": "capricorn",
        "date": "12/22－1/19",
        "symbol": "♑"
    },

    "♒ 水瓶座": {
        "sign": "aquarius",
        "date": "1/20－2/18",
        "symbol": "♒"
    },

    "♓ 雙魚座": {
        "sign": "pisces",
        "date": "2/19－3/20",
        "symbol": "♓"
    }
}


# =========================================================
# 3. 簡單美化
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        radial-gradient(
            circle at top left,
            rgba(115, 86, 255, 0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at top right,
            rgba(220, 100, 180, 0.15),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #11101c 0%,
            #171328 55%,
            #10101a 100%
        );

        color: white;
    }

    [data-testid="stSidebar"] {
        background-color: #11101a;
    }

    div[data-testid="stButton"] button {
        width: 100%;
        min-height: 50px;
        border-radius: 15px;
        border: none;
        font-weight: bold;
        font-size: 16px;
        color: white;
        background: linear-gradient(
            90deg,
            #765cff,
            #ce65cd
        );
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 4. API 函式
# =========================================================

def get_horoscope(sign, horoscope_type):

    if horoscope_type == "每日運勢":

        url = (
            "https://freehoroscopeapi.com/"
            "api/v1/get-horoscope/daily"
        )

    elif horoscope_type == "每週運勢":

        url = (
            "https://freehoroscopeapi.com/"
            "api/v1/get-horoscope/weekly"
        )

    else:

        return None, "運勢類型錯誤"


    params = {
        "sign": sign
    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        result = response.json()

        data = result.get("data", {})

        horoscope = data.get("horoscope")

        if not horoscope:

            return None, "沒有取得運勢內容"

        return data, None


    except requests.exceptions.Timeout:

        return None, "API 連線逾時"


    except requests.exceptions.RequestException as error:

        return None, f"API 連線失敗：{error}"


    except ValueError:

        return None, "API 回傳格式錯誤"


# =========================================================
# 5. 英文翻成繁體中文
# =========================================================

def translate_to_chinese(text):

    try:

        translator = GoogleTranslator(
            source="en",
            target="zh-TW"
        )

        return translator.translate(text)

    except Exception:

        return text


# =========================================================
# 6. 網站標題
# =========================================================

st.title("🔮 星座運勢查詢")

st.write(
    "選擇你的星座，查看每日或每週星座運勢"
)

st.divider()


# =========================================================
# 7. 側邊欄
# =========================================================

with st.sidebar:

    st.header("✨ 查詢設定")

    selected_zodiac = st.selectbox(
        "選擇你的星座",
        list(ZODIACS.keys())
    )

    horoscope_type = st.radio(
        "選擇運勢類型",
        [
            "每日運勢",
            "每週運勢"
        ]
    )


# =========================================================
# 8. 取得星座資料
# =========================================================

zodiac = ZODIACS[selected_zodiac]

english_sign = zodiac["sign"]

date_range = zodiac["date"]

symbol = zodiac["symbol"]

chinese_name = selected_zodiac.replace(
    symbol,
    ""
).strip()


# =========================================================
# 9. 顯示星座資料
# 這裡完全不用 HTML
# =========================================================

left, center, right = st.columns(
    [1, 2, 1]
)

with center:

    with st.container(
        border=True
    ):

        st.markdown(
            f"<h1 style='text-align:center'>{symbol}</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h2 style='text-align:center'>{chinese_name}</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p style='text-align:center'>{date_range}</p>",
            unsafe_allow_html=True
        )


st.write("")


# =========================================================
# 10. 查詢按鈕
# =========================================================

if st.button(
    "✨ 查看我的運勢",
    type="primary"
):

    with st.spinner(
        "正在查詢星座運勢..."
    ):

        data, error = get_horoscope(
            english_sign,
            horoscope_type
        )


    # =====================================================
    # 查詢失敗
    # =====================================================

    if error:

        st.error(error)


    # =====================================================
    # 查詢成功
    # =====================================================

    else:

        horoscope_english = data.get(
            "horoscope",
            ""
        )

        api_date = data.get(
            "date",
            ""
        )


        with st.spinner(
            "正在翻譯成繁體中文..."
        ):

            horoscope_chinese = (
                translate_to_chinese(
                    horoscope_english
                )
            )


        st.divider()


        st.header(
            f"🌟 {chinese_name}｜{horoscope_type}"
        )


        if api_date:

            st.caption(
                f"運勢日期：{api_date}"
            )


        # =================================================
        # 中文運勢
        # =================================================

        st.subheader(
            "中文運勢"
        )

        with st.container(
            border=True
        ):

            st.write(
                horoscope_chinese
            )


        # =================================================
        # 英文原文
        # =================================================

        with st.expander(
            "查看英文原文"
        ):

            st.write(
                horoscope_english
            )


# =========================================================
# 11. 頁尾
# =========================================================

st.divider()

st.caption(
    "Horoscope data provided by Free Horoscope API"
)