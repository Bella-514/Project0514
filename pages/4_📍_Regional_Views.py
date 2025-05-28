import streamlit as st
import ee
import leafmap

st.set_page_config(layout="wide")
st.title("📍 巴西土地利用：子區域檢視")

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Initialize()

# 區域選擇
regions = {
    "亞馬遜州": ee.Geometry.BBox(-70, -5, -60, 0),
    "聖保羅州": ee.Geometry.BBox(-48, -24, -45, -22),
    "馬托格羅索州": ee.Geometry.BBox(-58, -15, -54, -12)
}
region_name = st.selectbox("選擇區域", list(regions.keys()))
region = regions[region_name]

# 土地覆蓋資料
dataset = ee.ImageCollection("MODIS/006/MCD12Q1").filterDate("2020-01-01", "2020-12-31").first()
landcover = dataset.select("LC_Type1").clip(region)

# 建立地圖
m = leafmap.Map()
m.add_ee_layer(landcover, {}, f"{region_name} 土地覆蓋 (2020)")
m.add_ee_layer(region, {"color": "red"}, "選擇區域")
m.to_streamlit(width=1000, height=600)
