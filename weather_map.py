import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="글로벌 도시 날씨 & 공기질 대시보드", page_icon="🌤️")

st.title("🌤️ 전 세계 도시별 날씨 & 미세먼지 정보 조회")
st.caption("Open-Meteo Open API를 활용한 실시간 기상 모니터링")

# 도시 기본 좌표 (위도, 경도)
CITY_COORDS = {
    "서울 (Seoul)": (37.5665, 126.9780),
    "도쿄 (Tokyo)": (35.6762, 139.6503),
    "런던 (London)": (51.5074, -0.1278),
    "뉴욕 (New York)": (40.7128, -74.0060),
    "파리 (Paris)": (48.8566, 2.3522),
    "시드니 (Sydney)": (-33.8688, 151.2093),
}

selected_city = st.selectbox("조회할 도시를 선택하세요:", list(CITY_COORDS.keys()))
lat, lon = CITY_COORDS[selected_city]

# 1. Open-Meteo Weather API 호출
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m"
w_res = requests.get(weather_url).json()

# 2. Open-Meteo Air Quality API 호출
air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5"
a_res = requests.get(air_url).json()

if "current_weather" in w_res:
    curr_w = w_res["current_weather"]
    curr_a = a_res.get("current", {})

    st.subheader(f"📌 {selected_city} 현재 기상 상황")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 기온", f"{curr_w['temperature']} °C")
    col2.metric("풍속", f"{curr_w['windspeed']} km/h")
    col3.metric("미세먼지 (PM10)", f"{curr_a.get('pm10', 'N/A')} µg/m³")

    # 시간대별 기온 변화 차트
    st.write("---")
    st.subheader("📈 향후 시간대별 예상 기온 변화")
    
    hourly_time = w_res["hourly"]["time"][:24]
    hourly_temp = w_res["hourly"]["temperature_2m"][:24]
    
    df = pd.DataFrame({
        "시간": [t.split("T")[1] for t in hourly_time],
        "기온 (°C)": hourly_temp
    })
    
    st.line_chart(df.set_index("시간"))
else:
    st.error("기상 데이터를 불러오는 데 실패했습니다.")
