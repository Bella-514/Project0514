import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import ee

st.set_page_config(layout="wide")

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# Sidebar
markdown = """
中南美洲土地覆蓋地圖應用  
資料來源：ESA WorldCover 2021  
<https://geo3w.ncue.edu.tw/?Lang=zh-tw>
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("🌎 中南美洲土地覆蓋 + 國界 + 首都標記")

# 建立地圖
m = leafmap.Map(center=[-15, -60], zoom=4)

# --- 加入 ESA WorldCover ---
worldcover = ee.Image('ESA/WorldCover/v200/2021')
classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
worldcover_remapped = worldcover.remap(classValues, remapValues, bandName='Map').rename('lc').toByte()

palette = [
    '006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
    'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0'
]
vis_params = {
    'min': 0,
    'max': 10,
    'palette': palette
}
m.add_ee_layer(worldcover_remapped, vis_params, 'WorldCover 2021')

# --- 加入國界 GeoJSON ---
m.add_geojson("custom.geo.json", layer_name="South America Borders")

# --- 加入首都資料並標記 ---
capital_data = [
    {"country": "Brazil", "capital": "Brasilia", "latitude": -15.793889, "longitude": -47.882778},
    {"country": "Argentina", "capital": "Buenos Aires", "latitude": -34.603722, "longitude": -58.381592},
    {"country": "Peru", "capital": "Lima", "latitude": -12.046374, "longitude": -77.042793},
    {"country": "Colombia", "capital": "Bogotá", "latitude": 4.7110, "longitude": -74.0721},
    {"country": "Chile", "capital": "Santiago", "latitude": -33.4489, "longitude": -70.6693},
    {"country": "Ecuador", "capital": "Quito", "latitude": -0.1807, "longitude": -78.4678},
    {"country": "Venezuela", "capital": "Caracas", "latitude": 10.4806, "longitude": -66.9036},
    {"country": "Paraguay", "capital": "Asunción", "latitude": -25.2637, "longitude": -57.5759},
    {"country": "Uruguay", "capital": "Montevideo", "latitude": -34.9011, "longitude": -56.1645},
    {"country": "Bolivia", "capital": "Sucre", "latitude": -19.0196, "longitude": -65.2619},
    {"country": "Guyana", "capital": "Georgetown", "latitude": 6.8013, "longitude": -58.1551},
    {"country": "Suriname", "capital": "Paramaribo", "latitude": 5.8520, "longitude": -55.2038},
    {"country": "French Guiana", "capital": "Cayenne", "latitude": 4.9224, "longitude": -52.3135}
]
df = pd.DataFrame(capital_data)

icon_list = [
    "flag", "star", "cloud", "home", "leaf", "fire", "heart", 
    "gift", "bell", "camera", "music", "glass", "phone"
]

# 加入城市群集點
m.add_points_from_xy(
    df,
    x="longitude",
    y="latitude",
    color_column="country",
    icon_names=icon_list,
    spin=True,
    add_legend=True,
    popup=["country", "capital"],
)

# 顯示地圖
m.to_streamlit(height=700)
