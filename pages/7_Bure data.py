import ee
import geemap
import streamlit as st


# 設定 Streamlit 頁面標題
st.title("FireCCI 2019 Burn Date vs Confidence Level")

# 建立 Map 對象
Map = geemap.Map()
Map.add_basemap('HYBRID')

# 載入 2020 火災資料集
dataset = ee.ImageCollection('ESA/CCI/FireCCI/5_1').filterDate('2019-01-01', '2019-12-31')
fire_cover = dataset.select('BurnDate')
maxBA = fire_cover.max()

# BurnDate 可視化樣式
baVis = {
    'min': 1,
    'max': 366,
    'palette': [
        '7209f6', '3a0dfb', '0210ff', '0052ff', '0098ff', '00ddff',
        '00ffdd', '00ff99', '00ff55', '02ff15', '3eff0f', '7aff0a',
        'b6ff05', 'f2ff00', 'f9c400', 'fb8200', 'fd4100', 'ff0000',
    ],
}

# 信心水準圖層：BurnDate >= 50
threshold = 50
ConfidenceLevel_bin = maxBA.gte(threshold).selfMask()

ConfidenceLevelVisParam = {
    'palette': ['red']
}

# 建立左右分割地圖
left_layer = geemap.ee_tile_layer(maxBA, baVis, 'BurnDate')
right_layer = geemap.ee_tile_layer(ConfidenceLevel_bin, ConfidenceLevelVisParam, 'ConfidenceLevel >= 50')

Map.split_map(left_layer, right_layer)

# 顯示地圖於 Streamlit
Map.to_streamlit()
