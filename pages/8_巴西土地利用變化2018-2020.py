import streamlit as st
import ee
import geemap.foliumap as geemap

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# Streamlit 基本設定
st.set_page_config(layout="wide")
st.title("🌎 中南美洲土地利用變化觀察（2018–2022）")

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

# 顯示圖例說明
st.markdown(f"### 📋 {year} 年土地類型對照表")
for code, label in modis_labels.items():
    st.write(f"- **{code}**: {label}")
