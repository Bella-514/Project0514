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
image_left = ee.Image('ESA/WorldCover/v200/2021')
classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
image_left = image_left.remap(classValues, remapValues, bandName='Map').rename('lc').toByte()

vis_params_left = {
    'min': 0,
    'max': 10,
    'palette': [
        '006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
        'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0'
    ]
}
left_layer = geemap.ee_tile_layer(image_left, vis_params_left, 'WorldCover')

# --- 右圖：透明背景 + 疊加 GeoJSON 國界 ---
empty_image = ee.Image(0).visualize(**{'palette': ['ffffff00']})
right_layer = geemap.ee_tile_layer(empty_image, {}, 'Transparent Layer')

# 地圖以中南美洲為中心
my_Map.centerObject(region, 4)

# 設定分割地圖
my_Map.split_map(left_layer, right_layer)

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
