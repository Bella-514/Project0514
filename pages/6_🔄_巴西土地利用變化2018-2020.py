import streamlit as st
import ee
import geemap.foliumap as geemap

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# Streamlit 基本設定
st.set_page_config(layout="wide")
st.title("🔄 中南美洲土地利用變化觀察")

# 側欄：選擇年份
year = st.sidebar.selectbox("📅 選擇觀察年份", [2018, 2019, 2020])

# MODIS MCD12Q1 的年度資料識別格式
dataset_id = f"MODIS/006/MCD12Q1"

# ROI：中南美洲區域（包含墨西哥、巴西、哥倫比亞等）
roi = ee.Geometry.BBox(-120, -60, -30, 30)

# 載入 MODIS 土地覆蓋資料
image = ee.ImageCollection(dataset_id) \
    .filter(ee.Filter.calendarRange(year, year, "year")) \
    .first() \
    .select('LC_Type1') \
    .clip(roi)

# ---- 計算耕地與雨林面積 ----
# MODIS 的每像素面積（單位：平方公里）
pixel_area_km2 = 0.25

# 建立耕地與雨林的掩膜
cropland_mask = image.eq(9)
forest_mask = image.eq(2)

# 計算每種類別的像素總數
cropland_stats = cropland_mask.reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=roi,
    scale=500,
    maxPixels=1e13
)

forest_stats = forest_mask.reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=roi,
    scale=500,
    maxPixels=1e13
)

# 取回像素數並換算面積
cropland_pixels = cropland_stats.getNumber('LC_Type1')
forest_pixels = forest_stats.getNumber('LC_Type1')

cropland_area_km2 = cropland_pixels.multiply(pixel_area_km2)
forest_area_km2 = forest_pixels.multiply(pixel_area_km2)

# 將面積數據取出為 Python 數值
cropland_area = cropland_area_km2.getInfo()
forest_area = forest_area_km2.getInfo()


# MODIS IGBP 類別顏色與標籤（共17類）
modis_palette = [
    "05450a", "086a10", "54a708", "78d203", "009900",
    "c6b044", "dcd159", "dade48", "fbff13", "b6ff05",
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
    6: "灌木",
    7: "草地",
    8: "稀疏植被",
    9: "農田",
    10: "濕地",
    11: "城市",
    12: "裸地",
    13: "苔原",
    14: "雪地",
    15: "水體",
    16: "未分類"
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
    f"{year} 土地利用（MODIS）"
)

# 準備圖例資料（去除 index 0）
label_list = list(modis_labels.values())[1:17]
color_list = modis_palette[1:17]

Map.add_legend(title="MODIS 土地類別", labels=label_list, colors=color_list)
Map.to_streamlit(height=600)

# 顯示面積資訊
st.markdown(f"### 📊 {year} 年面積統計")
st.write(f"🌾 耕地面積：約 **{cropland_area:,.0f}** 平方公里")
st.write(f"🌳 雨林（常綠闊葉林）面積：約 **{forest_area:,.0f}** 平方公里")



