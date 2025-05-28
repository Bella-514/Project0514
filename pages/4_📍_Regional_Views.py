import streamlit as st
import leafmap.foliumap as leafmap
import ee

st.set_page_config(layout="wide")

st.title("📍 巴西土地利用：子區域檢視")

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# 使用者選擇地區
regions = {
    "亞馬遜州": ee.Geometry.BBox(-70, -5, -60, 0),
    "聖保羅州": ee.Geometry.BBox(-48, -24, -45, -22),
    "馬托格羅索州": ee.Geometry.BBox(-58, -15, -54, -12)
}
region_name = st.selectbox("選擇區域", list(regions.keys()))
region = regions[region_name]

# GEE 土地覆蓋資料（例如 MODIS）
dataset = ee.ImageCollection("MODIS/006/MCD12Q1").filterDate("2020-01-01", "2020-12-31").first()
landcover = dataset.select("LC_Type1")

# 建立地圖
m = leafmap.Map(center=[-10, -55], zoom=4)
m.addLayer(landcover.clip(region), {}, f"{region_name} 土地覆蓋 (2020)")
m.addLayer(region, {"color": "red"}, "選擇區域邊界")
m.to_streamlit(width=1000, height=600)
