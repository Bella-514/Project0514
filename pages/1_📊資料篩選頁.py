import streamlit as st
import ee
import leafmap.foliumap as geemap
import json

# 初始化 Earth Engine（防呆處理）
try:
    ee.Initialize()
except ee.EEException:
    # 從 secrets 初始化（使用 Service Account 或 refresh token）
    key_dict = json.loads(st.secrets["ee_service_account"])  # 如果你是用 service account
    credentials = ee.ServiceAccountCredentials(email=key_dict["client_email"], key_data=key_dict)
    ee.Initialize(credentials)

st.title("📊 子頁面：2018–2020 森林火災資料")

# 讀取 2018–2020 的影像資料集
dataset = ee.ImageCollection('ESA/CCI/FireCCI/5_1').filterDate('2018-01-01', '2020-12-31')
fire_cover = dataset.select('BurnDate')
maxBA = fire_cover.max()

# 配色參數
baVis = {
    'min': 1,
    'max': 366,
    'palette': [
        '7209f6', '3a0dfb', '0210ff', '0052ff', '0098ff', '00ddff',
        '00ffdd', '00ff99', '00ff55', '02ff15', '3eff0f', '7aff0a',
        'b6ff05', 'f2ff00', 'f9c400', 'fb8200', 'fd4100', 'ff0000',
    ],
}

baVisParam = {
    'min': 0,
    'max': 23,
    'palette': ['yellow', 'red']
}
layer_name = 'BurnDate'

# 建立地圖
my_Map = geemap.Map()
my_Map.addLayer(maxBA, baVis, layer_name)
my_Map.add_colorbar(baVisParam, label=layer_name, layer_name=layer_name)

# 顯示地圖
my_Map.to_streamlit(height=600)
