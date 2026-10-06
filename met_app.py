import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(page_title="Interactive Weather & Air Quality Map", page_icon="🗺️")

st.title("🗺️ Interactive Global Weather & Air Quality Map")
st.caption("Click anywhere on the map to get real-time weather and air quality data using Open-Meteo API.")

# 1. Initialize Folium Map (Default centered near Seoul)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=5)

# Render map in Streamlit and capture user click events
map_data = st_folium(m, width=700, height=400)

# 2. Extract latitude and longitude when user clicks on the map
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    st.success(f"📍 Selected Location: Latitude {lat:.4f}, Longitude {lon:.4f}")

    # Fetch Weather API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m"
    w_res = requests.get(weather_url).json()

    # Fetch Air Quality API
    air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5"
    a_res = requests.get(air_url).json()

    if "current_weather" in w_res:
        curr_w = w_res["current_weather"]
        curr_a = a_res.get("current", {})

        st.subheader("📌 Current Atmospheric Conditions")
        
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
        st.error("Failed to retrieve weather data for the selected point.")
else:
    st.info("💡 Click any point on the map above to view its weather and air quality forecast!")
