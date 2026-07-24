Open-Meteo 提供各種氣象資料 API，讓你用程式直接取得：

- 即時天氣(Current Weather)
- 小時預報(Hourly Forecast)
- 每日預報(Daily Forecast)
- 歷史天氣(Historical Weather)
- 空氣品質(Air Quality)
- 海浪資料(Marine Weather)
- 地理編碼(城市名稱轉經緯度)

```
天氣 Forecast API
https://api.open-meteo.com/v1/forecast

空氣品質 Air Quality API
https://air-quality-api.open-meteo.com/v1/air-quality
```

```py
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# 中文設定
# ===============================
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
font_name = 'Microsoft JhengHei'

# ===============================
# 台南座標
# ===============================
LATITUDE = 22.9999
LONGITUDE = 120.2269
TIMEZONE = "Asia/Taipei"


# ===============================
# API 網址
# ===============================
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


# ===============================
# 取得台南天氣資料
# ===============================
weather_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
    "timezone": TIMEZONE
}

weather_response = requests.get(
    WEATHER_API_URL,
    params=weather_params,
    timeout=10
)

weather_response.raise_for_status()
weather_data = weather_response.json()


# ===============================
# 取得台南空氣品質資料
# ===============================
air_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
    "hourly": "us_aqi,pm10,pm2_5",
    "forecast_days": 1,
    "timezone": TIMEZONE
}

air_response = requests.get(
    AIR_QUALITY_API_URL,
    params=air_params,
    timeout=10
)

air_response.raise_for_status()
air_data = air_response.json()


# ===============================
# 顯示即時天氣
# ===============================
current_weather = weather_data["current"]

print("===== 台南即時天氣 =====")
print(f"時間：{current_weather['time']}")
print(f"溫度：{current_weather['temperature_2m']} °C")
print(f"濕度：{current_weather['relative_humidity_2m']} %")
print(f"風速：{current_weather['wind_speed_10m']} km/h")
print(f"天氣代碼：{current_weather['weather_code']}")


# ===============================
# 顯示目前空氣品質
# ===============================
current_air = air_data["current"]

print("\n===== 台南空氣品質 =====")
print(f"時間：{current_air['time']}")
print(f"US AQI：{current_air['us_aqi']}")
print(f"PM10：{current_air['pm10']} μg/m³")
print(f"PM2.5：{current_air['pm2_5']} μg/m³")
print(f"CO：{current_air['carbon_monoxide']} μg/m³")
print(f"NO2：{current_air['nitrogen_dioxide']} μg/m³")
print(f"O3：{current_air['ozone']} μg/m³")


# ===============================
# 整理每日預報成表格
# ===============================
daily = weather_data["daily"]

daily_df = pd.DataFrame({
    "日期": daily["time"],
    "最高溫": daily["temperature_2m_max"],
    "最低溫": daily["temperature_2m_min"],
    "最大降雨機率": daily["precipitation_probability_max"],
    "最大風速": daily["wind_speed_10m_max"]
})

print("\n===== 台南每日預報 =====")
print(daily_df)


# ===============================
# 整理空氣品質每小時資料
# ===============================
hourly_air = air_data["hourly"]

air_df = pd.DataFrame({
    "時間": hourly_air["time"],
    "US AQI": hourly_air["us_aqi"],
    "PM10": hourly_air["pm10"],
    "PM2.5": hourly_air["pm2_5"]
})

print("\n===== 台南每小時空氣品質 =====")
print(air_df.head())


# ===============================
# 畫圖：每日最高/最低溫
# ===============================
plt.figure(figsize=(10, 5))
plt.plot(daily_df["日期"], daily_df["最高溫"], marker="o", label="最高溫")
plt.plot(daily_df["日期"], daily_df["最低溫"], marker="o", label="最低溫")
plt.title("台南每日最高溫與最低溫")
plt.xlabel("日期")
plt.ylabel("溫度(°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# ===============================
# 畫圖：PM2.5 變化
# ===============================
plt.figure(figsize=(10, 5))
plt.plot(air_df["時間"], air_df["PM2.5"], marker="o")
plt.title("台南今日 PM2.5 每小時變化")
plt.xlabel("時間")
plt.ylabel("PM2.5 (μg/m³)")
plt.xticks(rotation=60)
plt.tight_layout()
plt.show()
```
