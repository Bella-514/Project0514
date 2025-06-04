import streamlit as st
import ee
from google.oauth2 import service_account
import geemap.foliumap as geemap

# 從 Streamlit Secrets 讀取 GEE 服務帳戶金鑰 JSON
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]

# 使用 google-auth 進行 GEE 授權
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)

# 初始化 GEE
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
