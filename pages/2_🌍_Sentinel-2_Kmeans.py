import ee
import geemap
import streamlit as st

# 初始化 Earth Engine（確保你已經用 ee.Initialize(...) 驗證過）
# ee.Initialize(...)

# 假設你已經準備好 image、result001、legend_dict
# image: 原始 Sentinel-2 影像
# result001: KMeans 聚類後影像
# legend_dict: 類別與顏色的對應，例如：{'Water': 'blue', 'Forest': 'green', 'Urban': 'red'}

# 可視化參數
vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}  # 假設是 RGB 的原始影像
palette = list(legend_dict.values())
vis_params_001 = {'min': 0, 'max': 10, 'palette': palette}

# 建立左右地圖圖層
left_layer = geemap.ee_tile_layer(image, vis_params, name="Sentinel-2")
right_layer = geemap.ee_tile_layer(result001, vis_params_001, name="KMeans Clustered")

# 建立地圖
Map = geemap.Map(center=[24.08, 120.56], zoom=10)
Map.split_map(left_layer, right_layer)

# 加入圖例到右下角
Map.add_legend(title='Land Cover Cluster (KMeans)', legend_dict=legend_dict, position='bottomright')

# 顯示到 Streamlit
Map.to_streamlit(height=600)
