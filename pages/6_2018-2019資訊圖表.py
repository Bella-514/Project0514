import ee
import geemap.foliumap as geemap
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# --- 側邊欄說明 ---
markdown = """
A Streamlit map app exercise  
<https://geo3w.ncue.edu.tw/?Lang=zh-tw>
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

st.title("South America: Sentinel-2 vs Capitals Map (Split View)")

# --- 初始化 Earth Engine ---
if not ee.data._initialized:
    ee.Initialize()

# --- 定義區域 (亞馬遜附近) ---
region = ee.Geometry.BBox(-63.0, -15.0, -47.0, -2.0)

# --- Sentinel-2 影像 ---
sentinel_img = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(region)
    .filterDate('2018-01-01', '2019-12-31')
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)
sentinel_vis = {'min': 100, 'max': 3500, 'bands': ['B11', 'B8', 'B3']}
left_layer = geemap.ee_tile_layer(sentinel_img, sentinel_vis, name="Sentinel-2")

# --- 建立點資料（首都） ---
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

# --- 建立右側地圖圖層 ---
m_right = geemap.Map()
m_right.add_geojson("custom.geo.json", layer_name="South America Countries")

icon_list = [
    "flag", "star", "cloud", "home", "leaf", "fire", "heart", 
    "gift", "bell", "camera", "music", "glass", "phone"
]
m_right.add_points_from_xy(
    df,
    x="longitude",
    y="latitude",
    color_column="country",
    icon_names=icon_list,
    spin=True,
    add_legend=True,
)
right_layer = m_right.layers[-1]  # 取得加好點圖層

# --- 整合為 split view 地圖 ---
Map = geemap.Map(center=[-15, -60], zoom=4)
Map.split_map(left_layer, right_layer)
Map.to_streamlit(height=700)
