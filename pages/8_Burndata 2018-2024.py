import ee
import geemap
import streamlit as st

# 建立地圖
Map = geemap.Map()
Map.add_basemap('HYBRID')

# 1. 載入全球國界資料（內建 geemap 資源）
countries = ee.FeatureCollection(geemap.examples.get_ee_path('countries'))

# 2. 定義中南美洲國家名稱（可視情況擴充）
latin_america_countries = [
    "Mexico", "Guatemala", "Belize", "El Salvador", "Honduras", "Nicaragua", "Costa Rica", "Panama",
    "Colombia", "Venezuela", "Ecuador", "Peru", "Bolivia", "Brazil", "Paraguay", "Uruguay", "Argentina", "Chile", "Guyana", "Suriname", "French Guiana"
]

# 3. 過濾國家資料為中南美洲區域
latin_america = countries.filter(ee.Filter.inList('name', latin_america_countries))

# 4. 載入火災資料集 (2018–2024)
dataset = ee.ImageCollection('ESA/CCI/FireCCI/5_1').filterDate('2018-01-01', '2018-12-31')
fire_cover = dataset.select('BurnDate')
maxBA = fire_cover.max()

# 5. 將火災資料裁切至中南美洲區域
maxBA_latin = maxBA.clip(latin_america)

# 6. 可視化設定
baVis = {
    'min': 1,
    'max': 366,
    'palette': [
        '7209f6', '3a0dfb', '0210ff', '0052ff', '0098ff', '00ddff',
        '00ffdd', '00ff99', '00ff55', '02ff15', '3eff0f', '7aff0a',
        'b6ff05', 'f2ff00', 'f9c400', 'fb8200', 'fd4100', 'ff0000',
    ],
}
baVisParam = {'min': 0, 'max': 23, 'palette': ['yellow', 'red']}
layer_name = 'BurnDate (Latin America)'

# 7. 加到地圖上
Map.addLayer(maxBA_latin, baVis, layer_name)

# 8. 顯示地圖於 Streamlit
st.title("FireCCI Burn Date (2018) - Latin America Only")
Map.to_streamlit()
