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

# ROI：南美亞馬遜區域
roi = ee.Geometry.BBox(-75, -15, -45, 5)


# 抓取 MODIS 火災資料
dataset = ee.ImageCollection('MODIS/006/MCD64A1') \
    .filterBounds(roi) \
    .filterDate(start_date, end_date) \
    .select('BurnDate')

# 可視化參數
vis_params = {
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red']
}

# 建立 GIF
gif_params = {
    'dimensions': 768,
    'region': roi,
    'framesPerSecond': 2,
    'bands': ['BurnDate'],
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red'],
    'format': 'gif',
    'label': 'YYYY-MM-dd',  # ✅ 顯示時間標籤於右上角
    'fontSize': 18,
    'fontColor': 'white',
    'labelPosition': 'top-right'
}

gif_url = dataset.getVideoThumbURL(gif_params)



# 顯示動畫 GIF
st.markdown(f"### 🎞️ {year} 年火災變化動畫（含日期）")
st.image(gif_url)
