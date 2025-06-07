import streamlit as st
import ee
import geemap
import tempfile
import os

st.set_page_config(layout="wide")
st.title("🔥 2018-2020 年森林火災變化觀察（每日火點 + 時間標示）")

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# 選擇年份
year = st.sidebar.slider("選擇年份", 2018, 2020, 2018)
start_date = f"{year}-07-01"
end_date = f"{year}-08-31"

# 定義區域
roi = ee.Geometry.BBox(-75, -15, -45, 5)

# 取得每日 MODIS 火點影像
collection = ee.ImageCollection('MODIS/006/MCD14DL') \
    .filterDate(start_date, end_date) \
    .filterBounds(roi)

# 將每筆火點轉為栅格，並加入時間
def fire_image(feature):
    image = ee.Image(0).float().paint(feature, 1).selfMask()
    time = feature.get('system:time_start')
    return image.set({'system:time_start': time})

fire_images = collection.map(fire_image)

# 動畫參數
video_args = {
    'dimensions': 768,
    'region': roi,
    'framesPerSecond': 2,
    'format': 'gif',
    'palette': ['red'],
    'label': 'YYYY-MM-dd',
    'labelPosition': 'top-right',
    'fontSize': 16,
    'fontColor': 'white',
}

# 建立儲存資料夾
output_dir = "./tmp"
os.makedirs(output_dir, exist_ok=True)
gif_path = os.path.join(output_dir, f"fire_{year}.gif")

with st.spinner("正在生成火災動畫..."):
    geemap.download_ee_video(fire_images, video_args, gif_path)

# 檢查檔案存在再顯示
if os.path.exists(gif_path):
    st.markdown(f"### 🎞️ {year} 年火災動畫（每日，含時間標籤）")
    st.image(gif_path)
else:
    st.error("❌ 無法生成 GIF，請檢查資料是否存在或資料集是否過小。")


# 顯示定位圖
st.markdown("### 📍 區域對照地圖")
st.image("定位區域圖示.jpg", caption="分析區域：南美巴西亞馬遜", use_container_width=True)
