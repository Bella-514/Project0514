import streamlit as st
import ee
import geemap.foliumap as geemap

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

st.set_page_config(layout="wide")
st.title("🌍 中南美洲：土地覆蓋 vs 國界（分割視圖）")

# 建立地圖物件
my_Map = geemap.Map()

# --- 自訂中南美洲區域 ---
region = ee.Geometry.BBox(-85, -55, -30, 15)  # 約略包含整個中南美洲

# --- 左圖：ESA WorldCover 2021 ---
left_layer = geemap.Map(center=[-15, -60], zoom=4)

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

# 套用圖層
left_layer.addLayer(
    modis_img,
    {
        "min": 1,
        "max": 16,
        "palette": modis_palette[1:17]
    },
    "2019 MODIS 土地覆蓋"
)

# 圖例標籤（可選）
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

left_layer.add_legend(
    title="MODIS 土地類型 (2019)",
    labels=list(modis_labels.values()),
    colors=modis_palette[1:17]
)

# --- 右圖：透明背景 + 疊加 GeoJSON 國界 ---
empty_image = ee.Image(0).visualize(**{'palette': ['ffffff00']})
right_layer = geemap.ee_tile_layer(empty_image, {}, 'Transparent Layer')

# 地圖以中南美洲為中心
my_Map.centerObject(region, 4)

# 從 left_layer 和 right_layer 取出圖層（通常是第 0 個圖層）
left_tile = left_layer.layers[-1]  # 或 left_layer.ee_layers[0]['ee_object']
right_tile = right_layer

my_Map.split_map(left_tile, right_tile)


# 加入國界 GeoJSON（請確認 custom.geo.json 存在）
my_Map.add_geojson("custom.geo.json", layer_name="South America Borders")

# 加入圖例
legend_dict = {
    'Tree cover': '006400',
    'Shrubland': 'ffbb22',
    'Grassland': 'ffff4c',
    'Cropland': 'f096ff',
    'Built-up': 'fa0000',
    'Bare / sparse vegetation': 'b4b4b4',
    'Snow and ice': 'f0f0f0',
    'Permanent water bodies': '0064c8',
    'Herbaceous wetland': '0096a0',
    'Mangroves': '00cf75',
    'Moss and lichen': 'fae6a0'
}
my_Map.add_legend(title='ESA WorldCover (2021)', legend_dict=legend_dict, position='bottomright')

# 顯示地圖
my_Map.to_streamlit(height=650)
