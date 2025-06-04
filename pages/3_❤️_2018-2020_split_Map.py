import streamlit as st
import ee
import geemap.foliumap as geemap
import pandas as pd
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# --- 側邊欄控制元件 ---
st.sidebar.title("🔧 選擇參數")

# 年份選擇器（2018-2020）
years = st.sidebar.slider("選擇影像年份區間", 2018, 2020, (2018, 2020))
start_date = f"{years[0]}-01-01"
end_date = f"{years[1]}-12-31"

# 國家選擇器
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
selected_country = st.sidebar.selectbox("選擇國家聚焦", df["country"])
coords = df[df["country"] == selected_country][["latitude", "longitude"]].values[0]

# 區域設定（Amazon 地區）
region = ee.Geometry.BBox(-63.0, -15.0, -47.0, -2.0)

# --- 左側地圖：Sentinel-2 + WorldCover ---
left_map = geemap.Map(center=[coords[0], coords[1]], zoom=5)

# Sentinel-2 資料
sentinel_img = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(region)
    .filterDate(start_date, end_date)
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)
sentinel_vis = {'min': 100, 'max': 3500, 'bands': ['B11', 'B8', 'B3']}
left_map.addLayer(sentinel_img, sentinel_vis, f"Sentinel-2 ({years[0]}–{years[1]})")

# WorldCover 資料
my_lc = ee.Image('ESA/WorldCover/v200/2021')
classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
my_lc = my_lc.remap(classValues, remapValues, bandName='Map').rename('lc').toByte()
classVis = {
    'min': 0,
    'max': 10,
    'palette': [
        '006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
        'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0'
    ]
}
left_map.addLayer(my_lc, classVis, "WorldCover")
left_map.add_legend(title='Land Cover', builtin_legend='ESA_WorldCover')

# --- 右側地圖：國界 + 首都標記 ---
right_map = leafmap.Map(center=[coords[0], coords[1]], zoom=5)
right_map.add_geojson("custom.geo.json", layer_name="South America Countries")

# 加入首都點圖層
icon_list = [
    "flag", "star", "cloud", "home", "leaf", "fire", "heart",
    "gift", "bell", "camera", "music", "glass", "phone"
]
right_map.add_points_from_xy(
    df,
    x="longitude",
    y="latitude",
    color_column="country",
    icon_names=icon_list,
    spin=True,
    add_legend=True,
    popup=["country", "capital"]
)

# --- 版面配置 ---
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Sentinel-2 ({years[0]}–{years[1]}) + WorldCover")
    left_map.to_streamlit(height=600)

with col2:
    st.subheader("South America Capitals")
    right_map.to_streamlit(height=600)
