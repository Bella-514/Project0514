import streamlit as st
import ee
import geemap
import os
import tempfile
import datetime

st.set_page_config(layout="wide")
st.title("🔥 2018-2020 年森林火災變化觀察（含時間標籤）")

if not ee.data._initialized:
    ee.Initialize()

# 使用者選擇年份
st.sidebar.title("📅 選擇觀察年份")
year = st.sidebar.slider("選擇年份", 2018, 2020, 2018)

# ROI
roi = ee.Geometry.BBox(-75, -15, -45, 5)

# 建立每月火災影像集合
def create_monthly_burn_image(month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')
    image = ee.ImageCollection('MODIS/006/MCD64A1') \
        .filterDate(start, end) \
        .select('BurnDate') \
        .mean() \
        .set({'system:time_start': start.millis()})  # 必須加上這個才會有時間標籤
    return image

months = ee.List.sequence(1, 12)
monthly_images = ee.ImageCollection(months.map(create_monthly_burn_image))

# 設定 GIF 視覺與參數
video_args = {
    'dimensions': 768,
    'region': roi,
    'framesPerSecond': 2,
    'format': 'gif',
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red'],
    'label': 'YYYY-MM',
    'labelPosition': 'top-right',
    'fontSize': 16,
    'fontColor': 'white',
}

# 暫存檔路徑
temp_dir = tempfile.TemporaryDirectory()
gif_path = os.path.join(temp_dir.name, f"fire_{year}.gif")

# 建立動畫 GIF
with st.spinner("生成火災動畫中，請稍候..."):
    geemap.download_ee_video(monthly_images, video_args, gif_path)

# 顯示動畫
st.markdown(f"### 🎞️ {year} 年火災變化動畫（含時間標籤）")
st.image(gif_path)

# 顯示參考區域圖
st.markdown("### 🖼️ 區域對照地圖")
st.image("定位區域圖示.jpg", caption="分析區域: 南美地區（巴西亞馬遜）", use_container_width=True)
