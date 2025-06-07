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
roi = ee.Geometry.BBox(-75, -15, -45, 5)  # 南美地區（巴西亞馬遜）

# 抓取 MODIS 火災資料
dataset = ee.ImageCollection('MODIS/006/MCD64A1') \
    .filterBounds(roi) \
    .filterDate(start_date, end_date) \
    .select('BurnDate')

# 組合成動畫 GIF
vis_params = {
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red']
}

gif_url = dataset.getVideoThumbURL({
    'dimensions': 768,
    'region': roi,
    'framesPerSecond': 2,
    'bands': ['BurnDate'],
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red'],
    'format': 'gif'
})

# 顯示動畫
st.markdown(f"### {year} 年火災變化 GIF")
st.image(gif_url)

# 顯示地圖 + ROI
m = geemap.Map()
m.centerObject(roi, 6)
m.addLayer(roi, {"color": "gray"}, "分析區域")
m.to_streamlit(height=400)

# === 顯示 JPG 圖片 ===
st.markdown("### 🖼️ 區域對照地圖")
st.image("定位區域圖示.jpg", caption="分析區域示意圖", use_container_width=True) 
