import streamlit as st
import ee
import geemap.foliumap as geemap

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

st.set_page_config(layout="wide")
st.title("🌎 巴西土地利用變化觀察（2018–2020）")

# 側欄：選擇年份
year = st.sidebar.radio("📅 選擇年份", [2018, 2019, 2020])

# ROI：巴西區域（BBox 約略範圍）
roi = ee.Geometry.BBox(-74.0, -34.0, -34.0, 6.0)

# 對應年份的 WorldCover 影像 ID（ESA WorldCover）
dataset_dict = {
    2020: 'ESA/WorldCover/v100/2020',
    2019: 'ESA/WorldCover/v100/2019',
    2018: 'ESA/WorldCover/v100/2018',  # 若未提供，會 fallback（WorldCover 是從2020開始）
}

# 土地類別對應顏色（ESA 預設顏色表）
landcover_palette = [
    "006400",  # 10 Tree cover
    "ffbb22",  # 20 Shrubland
    "ffff4c",  # 30 Grassland
    "f096ff",  # 40 Cropland
    "fa0000",  # 50 Built-up
    "b4b4b4",  # 60 Bare / sparse vegetation
    "f0f0f0",  # 70 Snow and ice
    "0032c8",  # 80 Permanent water bodies
    "0096a0",  # 90 Herbaceous wetland
    "c6b044",  # 95 Mangroves
    "dcd159",  # 100 Moss and lichen
]

landcover_labels = {
    10: "樹林",
    20: "灌木叢",
    30: "草原",
    40: "農地",
    50: "建成區",
    60: "裸地",
    70: "雪地",
    80: "水體",
    90: "濕地",
    95: "紅樹林",
    100: "苔原地",
}

# 取得該年份資料
dataset_id = dataset_dict.get(year, dataset_dict[2020])  # fallback to 2020
landcover = ee.Image(dataset_id).clip(roi)

# 建立地圖
Map = geemap.Map(center=[-10, -52], zoom=4)
Map.addLayer(
    landcover,
    {
        "min": 10,
        "max": 100,
        "palette": landcover_palette,
    },
    f"{year} 土地覆蓋"
)

# 加入圖例
Map.add_legend(title="土地覆蓋分類", builtin_legend="ESA_WorldCover")

# 顯示地圖
Map.to_streamlit(height=600)

# 顯示說明
st.markdown(f"""
### 🗂️ {year} 年土地利用分類說明
以下為各顏色所代表的土地類型：
""")

for code, label in landcover_labels.items():
    st.write(f"- **{code}**: {label}")
