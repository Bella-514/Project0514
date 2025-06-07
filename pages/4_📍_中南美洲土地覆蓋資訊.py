import streamlit as st
import ee
import geemap.foliumap as geemap

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# 頁面設定
st.set_page_config(layout="wide")
st.title("🌱 2019 年巴西土地覆蓋觀察（MODIS MCD12Q1）")

# 指定年份
year = 2019

# ROI：巴西國土範圍（近似 BBox）
brazil_roi = ee.Geometry.BBox(-74.0, -34.0, -34.0, 5.5)

# 載入 MODIS MCD12Q1 資料
image = (
    ee.ImageCollection("MODIS/006/MCD12Q1")
    .filter(ee.Filter.calendarRange(year, year, "year"))
    .first()
    .select("LC_Type1")
    .clip(brazil_roi)
)

# MODIS IGBP 顏色與標籤（17 類）
modis_palette = [
    "05450a", "086a10", "54a708", "78d203", "009900",
    "c6b044", "dcd159", "dade48", "fbff13", "ff0000",
    "27ff87", "c24f44", "a5a5a5", "ff6d4c", "69fff8",
    "f9ffa4", "1c0dff"
]
modis_labels = {
    0: "無資料",
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
    16: "未分類",
}

# 顯示地圖
Map = geemap.Map(center=[-10, -55], zoom=4)
Map.addLayer(
    image,
    {
        "min": 1,
        "max": 16,
        "palette": modis_palette[1:17]
    },
    f"2019 MODIS 土地覆蓋"
)

# 顯示圖例
Map.add_legend(
    title="MODIS 土地類型",
    labels=list(modis_labels.values())[1:17],
    colors=modis_palette[1:17]
)
Map.to_streamlit(height=600)

