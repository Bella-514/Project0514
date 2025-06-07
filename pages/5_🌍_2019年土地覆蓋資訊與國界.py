import streamlit as st
import ee
import geemap.foliumap as geemap

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

st.set_page_config(layout="wide")
st.title("🌍 中南美洲：土地覆蓋 vs 國界")

# 主地圖
my_Map = geemap.Map()

# 中南美洲區域
region = ee.Geometry.BBox(-85, -55, -30, 15)

# MODIS MCD12Q1 土地覆蓋資料 (2019)
year = 2019
brazil_roi = ee.Geometry.BBox(-74.0, -34.0, -34.0, 5.5)

modis_img = (
    ee.ImageCollection("MODIS/006/MCD12Q1")
    .filter(ee.Filter.calendarRange(year, year, "year"))
    .first()
    .select("LC_Type1")
    .clip(brazil_roi)
)

# MODIS 類別顏色（農田為紅色）
modis_palette = [
    "05450a", "086a10", "54a708", "78d203", "009900",   # 1–5 林
    "c6b044", "dcd159", "dade48", "fbff13", "ff0000",   # 6–10 草、灌木、農田（紅）
    "27ff87", "c24f44", "a5a5a5", "ff6d4c", "69fff8",   # 11–15 城市、裸地、水
    "f9ffa4", "1c0dff"                                  # 16–17
]

# 建立左圖圖層 (MODIS)
left_tile = geemap.ee_tile_layer(
    modis_img,
    {
        "min": 1,
        "max": 16,
        "palette": modis_palette[1:17]
    },
    "2019 MODIS 土地覆蓋"
)

# 建立右圖圖層（透明）
empty_image = ee.Image(0).visualize(**{'palette': ['ffffff00']})
right_tile = geemap.ee_tile_layer(empty_image, {}, 'Transparent Layer')

# 設定分割地圖（使用圖層）
my_Map.split_map(left_tile, right_tile)

# 加入國界 GeoJSON（需事先放置 custom.geo.json 檔案於專案中）
my_Map.add_geojson("custom.geo.json", layer_name="South America Borders")

# MODIS 圖例
modis_labels = {
    1: "常綠針葉林",
    2: "常綠闊葉林",
    3: "落葉針葉林",
    4: "落葉闊葉林",
    5: "混合林",
    6: "灌木叢",
    7: "草地",
    8: "稀疏植被",
    9: "農田",
    10: "永久濕地",
    11: "城市",
    12: "裸地",
    13: "苔原",
    14: "雪地",
    15: "水體",
    16: "未分類"
}
my_Map.add_legend(
    title="MODIS 土地類型 (2019)",
    labels=list(modis_labels.values()),
    colors=modis_palette[1:17]
)

# 顯示地圖
my_Map.centerObject(region, 4)
my_Map.to_streamlit(height=650)
