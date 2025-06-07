import streamlit as st
import ee
import geemap
import os
import tempfile

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
dataset = (
    ee.ImageCollection('MODIS/006/MCD64A1')
    .filterBounds(roi)
    .filterDate(start_date, end_date)
    .select('BurnDate')
)

# 設定 GIF 視覺參數
vis_params = {
    'bands': ['BurnDate'],
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red'],
}

# 建立暫存資料夾
temp_dir = tempfile.TemporaryDirectory()
gif_path = os.path.join(temp_dir.name, f"fire_{year}.gif")

# 設定影片參數
video_args = {
    'dimensions': 768,
    'region': roi,
    'framesPerSecond': 2,
    'format': 'gif',
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red'],
    'label': 'YYYY-MM-dd',
    'labelPosition': 'top-right',
    'fontSize': 16,
    'fontColor': 'white',
}

# 下載帶時間標籤的 GIF
with st.spinner("生成火災動畫中，請稍候..."):
    geemap.download_ee_video(dataset, video_args, gif_path)

# 顯示動畫
st.markdown(f"### 🎞️ {year} 年火災變化動畫（含時間標籤）")
st.image(gif_path)

# 顯示靜態區域對照圖
st.markdown("### 🖼️ 區域對照地圖")
st.image("定位區域圖示.jpg", caption="分析區域: 南美地區（巴西亞馬遜）", use_container_width=True)
