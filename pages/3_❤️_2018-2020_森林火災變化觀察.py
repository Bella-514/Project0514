import streamlit as st
import ee
import geemap
import datetime

st.set_page_config(layout="wide")
st.title("🔥 2018-2020 年森林火災變化觀察")

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# 側欄參數
st.sidebar.title("📅 選擇觀察年份")
year = st.sidebar.slider("選擇年份", 2018, 2020, 2018)
start_date = f"{year}-01-01"
end_date = f"{year}-12-31"

st.sidebar.write("📌 使用 MODIS 火災資料")

# ROI：亞馬遜某區塊（可自訂）
roi = ee.Geometry.BBox(-75, -15, -45, 5)

# ➕ 取得 ROI 中心點並顯示位置
centroid = roi.centroid()
lon, lat = centroid.coordinates().getInfo()
st.markdown(f"📍 **目前分析中心位置：** 緯度 `{lat:.4f}`，經度 `{lon:.4f}`")

# 抓取 MODIS 火災資料
dataset = ee.ImageCollection('MODIS/006/MCD64A1') \
    .filterBounds(roi) \
    .filterDate(start_date, end_date) \
    .select('BurnDate')

# 組合成動畫 GIF
gif_url = dataset.getVideoThumbURL({
    'dimensions': 768,
    'region': roi,
    'framesPerSecond': 2,
    'bands': ['BurnDate'],
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red']
