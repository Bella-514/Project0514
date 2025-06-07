import streamlit as st
import ee
import pandas as pd
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# 側邊欄參數
st.sidebar.title("🔧 選擇參數")
years = st.sidebar.slider("選擇影像年份區間", 2018, 2020, (2018, 2020))
start_date = f"{years[0]}-01-01"
end_date = f"{years[1]}-12-31"

# 國家選擇下拉選單
capital_data = [
    {"country": "Brazil", "capital": "Brasilia", "latitude": -15.793889, "longitude": -47.882778},
    {"country": "Peru", "capital": "Lima", "latitude": -12.0464, "longitude": -77.0428},
    {"country": "Colombia", "capital": "Bogotá", "latitude": 4.7110, "longitude": -74.0721},
    {"country": "Bolivia", "capital": "Sucre", "latitude": -19.0196, "longitude": -65.2619},
]
df = pd.DataFrame(capital_data)
selected_country = st.sidebar.selectbox("選擇國家聚焦", df["country"])
coords = df[df["country"] == selected_country][["latitude", "longitude"]].values[0]

# 建立地圖
Map = leafmap.Map(center=[coords[0], coords[1]], zoom=6)

# 處理 ROI 區域
roi = Map.user_roi
if roi is None:
    roi = ee.Geometry.BBox(-59.67, -4.48, -56.74, -1.78)

# 在 ROI 畫灰色方框 (改用 add_ee_layer)
Map.add_ee_layer(roi, {"color": "gray"}, "ROI 區域")
Map.set_center(coords[1], coords[0], 7)

# Sentinel-2 影像
sentinel_img = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(roi)
    .filterDate(start_date, end_date)
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)
sentinel_vis = {'min': 100, 'max': 3500, 'bands': ['B11', 'B8', 'B3']}

# WorldCover 資料
lc = ee.Image('ESA/WorldCover/v200/2021')
classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
lc = lc.remap(classValues, remapValues, bandName='Map').rename('lc').toByte()
classVis = {
    'min': 0,
    'max': 10,
    'palette': [
        '006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
        'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0'
    ]
}

# 使用 split map 功能互動比較
Map.split_map(
    left_layer=(sentinel_img, sentinel_vis),
    right_layer=(lc, classVis)
)

# 顯示地圖在 Streamlit 中
st.subheader("🆚 Sentinel-2 vs WorldCover 土地覆蓋滑動比較")
Map.to_streamlit(height=650)
