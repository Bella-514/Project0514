import streamlit as st
import ee
import geemap.foliumap as geemap
import pandas as pd

st.set_page_config(layout="wide")

# --- 初始化 Earth Engine ---
if not ee.data._initialized:
    ee.Initialize()

# --- 左側地圖：Sentinel-2 + WorldCover ---
left_map = geemap.Map(center=[-15, -60], zoom=4)

# MODIS MCD12Q1 土地覆蓋資料 (2019)
year = 2019
brazil_roi = ee.Geometry.BBox(-74.0, -34.0, -34.0, 5.5)

modis_img = (
    ee.ImageCollection("MODIS/006/MCD12Q1")
    .filter(ee.Filter.calendarRange(year, year, "year"))
    .first()
    .select("LC_Type1")
    .clip(brazil_roi)
)

# MODIS 類別顏色（農田為紅色）
modis_palette = [
    "05450a", "086a10", "54a708", "78d203", "009900",   # 1–5 林
    "c6b044", "dcd159", "dade48", "fbff13", "ff0000",   # 6–10 草、灌木、農田（紅）
    "27ff87", "c24f44", "a5a5a5", "ff6d4c", "69fff8",   # 11–15 城市、裸地、水
    "f9ffa4", "1c0dff"                                  # 16–17
]

# 套用圖層
left_map.addLayer(
    modis_img,
    {
        "min": 1,
        "max": 16,
        "palette": modis_palette[1:17]
    },
    "2019 MODIS 土地覆蓋"
)

# 圖例標籤（可選）
modis_labels = {
    1: "常綠針葉林",
    2: "常綠闊葉林",
    3: "落葉針葉林",
    4: "落葉闊葉林",
    5: "混合林",
    6: "灌木叢",
    7: "草地",
    8: "稀疏植被",
    9: "農田",
    10: "永久濕地",
    11: "城市",
    12: "裸地",
    13: "苔原",
    14: "雪地",
    15: "水體",
    16: "未分類"
}

left_map.add_legend(
    title="MODIS 土地類型 (2019)",
    labels=list(modis_labels.values()),
    colors=modis_palette[1:17]
)

# --- 右側地圖：首都 + 國界 ---
import leafmap.foliumap as leafmap

right_map = leafmap.Map(center=[-15, -60], zoom=3)
right_map.add_geojson("custom.geo.json", layer_name="South America Countries")

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
right_map.add_points_from_xy(
    df,
    x="longitude",
    y="latitude",
    color_column="country",
    icon_names=icon_list,
    spin=True,
    add_legend=True,
)

# --- 使用 Streamlit columns 分兩欄顯示 ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Sentinel-2 + WorldCover")
    left_map.to_streamlit(height=600)

with col2:
    st.subheader("South America Capitals")
    right_map.to_streamlit(height=600)
