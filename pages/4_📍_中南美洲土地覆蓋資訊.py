import ee
import geemap.foliumap as geemap  # 或改成 leafmap 若你使用的是 leafmap
import streamlit as st

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# 建立地圖物件
my_Map = geemap.Map(center=[-10, -55], zoom=4)

# 定義區域（亞馬遜附近）
my_point = ee.Geometry.BBox(-63.0, -15.0, -47.0, -2.0)

# 載入 Sentinel-2 影像
my_img = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(my_point)
    .filterDate('2019-01-01', '2019-12-31')
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)

# 顯示 Sentinel-2
vis_params = {'min': 100, 'max': 3500, 'bands': ['B11', 'B8', 'B3']}
my_Map.addLayer(my_img, vis_params, "Sentinel-2")

# 載入 ESA WorldCover 土地覆蓋資料
my_lc = ee.Image('ESA/WorldCover/v200/2021')

# 重新分類土地覆蓋類別（Optional）
classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
label = 'lc'
my_lc = my_lc.remap(classValues, remapValues, bandName='Map').rename(label).toByte()

# 顯示 WorldCover 圖層
classVis = {
    'min': 0,
    'max': 10,
    'palette': [
        '006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
        'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0'
    ]
}
my_Map.addLayer(my_lc, classVis, "ESA WorldCover 10m v200")

# 加入圖例
my_Map.add_legend(title='ESA Land Cover Type', builtin_legend='ESA_WorldCover')

# 顯示地圖於 Streamlit
my_Map.to_streamlit(width=1000, height=600)
