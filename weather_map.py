import streamlit as st
import requests
import pandas as pd

# Page configuration
st.set_page_config(page_title="Global Weather & Air Quality Dashboard", page_icon="🌤️")

st.title("🌤️ Global City Weather & Air Quality Dashboard")
st.caption("Real-time weather monitoring service using Open-Meteo Open API")

# Major cities coordinates (Latitude, Longitude)
CITY_COORDS = {
    "Seoul": (37.5665, 126.9780),
    "Tokyo": (35.6762, 139.6503),
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060),
    "Paris": (48.8566, 2.3522),
    "Sydney": (-33.8688, 151.2093),
}

selected_city = st.selectbox("Select a city to view weather data:", list(CITY_COORDS.keys()))
lat, lon = CITY_COORDS[selected_city]

# 1. Fetch data from Open-Meteo Weather API
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m"
w_res = requests.get(weather_url).json()

# 2. Fetch data from Open-Meteo Air Quality API
air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5"
a_res = requests.get(air_url).json()

if "current_weather" in w_res:
    curr_w = w_res["current_weather"]
    curr_a = a_res.get("current", {})

    st.subheader(f"📌 Current Conditions in {selected_city}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{curr_w['temperature']} °C")
    col2.metric("Wind Speed", f"{curr_w['windspeed']} km/h")
    col3.metric("Particulate Matter (PM10)", f"{curr_a.get('pm10', 'N/A')} µg/m³")

    # Hourly temperature forecast chart
    st.write("---")
    st.subheader("📈 Hourly Temperature Forecast (Next 24 Hours)")
    
    hourly_time = w_res["hourly"]["time"][:24]
    hourly_temp = w_res["hourly"]["temperature_2m"][:24]
    
    df = pd.DataFrame({
        "Time": [t.split("T")[1] for t in hourly_time],
        "Temperature (°C)": hourly_temp
    })
    
    st.line_chart(df.set_index("Time"))
else:
    st.error("Failed to retrieve weather data from API.")
