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
roi = ee.Geometry.BBox(-59.67, -4.48, -56.74, -1.78)

# 顯示觀測位置資訊（用 ROI 的幾何中心）
centroid = roi.centroid()
coords = centroid.coordinates().getInfo()
lon, lat = coords

location_name = "亞馬遜雨林區域"
st.markdown(f"📍 **觀測地點：{location_name}**　（經度：`{lon:.2f}`，緯度：`{lat:.2f}`）")

# 抓取 MODIS 火災資料
dataset = (
    ee.ImageCollection('MODIS/006/MCD64A1')
    .filterBounds(roi)
    .filterDate(start_date, end_date)
    .select('BurnDate')
)

# 可視化參數
vis_params = {
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red']
}

# 建立 GIF 動畫參數
gif_params = {
    'dimensions': 768,
    'region': roi,
    'framesPerSecond': 2,
    'bands': ['BurnDate'],
    'min': 30,
    'max': 365,
    'palette': ['black', 'orange', 'red'],
    'format': 'gif',
    'label': 'YYYY-MM-dd',
    'fontSize': 18,
    'fontColor': 'white',
    'labelPosition': 'top-right'
}

# 取得動畫網址
gif_url = dataset.getVideoThumbURL(gif_params)

# 建立地圖並顯示 ROI
Map = geemap.Map(center=[lat, lon], zoom=7)
Map.addLayer(dataset.mean(), vis_params, f"{year} 年火災平均")
Map.addLayer(roi, {"color": "gray"}, "分析區域")
Map.to_streamlit(height=450)

# 顯示動畫
st.markdown(f"### 🎞️ {year} 年火災變化動畫（含日期）")
st.image(gif_url)
