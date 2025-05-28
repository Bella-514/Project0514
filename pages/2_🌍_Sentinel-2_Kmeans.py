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


###############################################
st.set_page_config(layout="wide")
st.title("🌍 使用服務帳戶連接 GEE 的 Streamlit App")


# 地理區域
point = ee.Geometry.Point([120.56, 24.08])

# 擷取 
image = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterBounds(point) \
    .filterDate("2021-01-01", "2022-01-01") \
    .sort('CLOUDY_PIXEL_PERCENTAGE') \
    .first() \
    .select('B.*')
vis_params = {'min':100, 'max': 3500, 'bands': ['B4', 'B3', 'B2']}


# 取10000點
training001 = image.sample(
    **{
        'region': image.geometry(),  # 若不指定，則預設為影像my_image的幾何範圍。
        'scale': 10,
        'numPixels': 10000,
        'seed': 0,
        'geometries': True,  # 設為False表示取樣輸出的點將忽略其幾何屬性(即所屬網格的中心點)，無法作為圖層顯示，可節省記憶體。
    }
)

num_clusters = 11
clusterer = ee.Clusterer.wekaKMeans(num_clusters).train(training001)

# 應用分群器於影像
result001 = image.cluster(clusterer)

# 設置圖示
legend_dict = {
    'zero': '#ff0004',
    'one': '#868686',
    'two':'#774b0a',
    'three':'#10d22c',
    'four':'#ffff52',
    'five':'#0000ff',
    'six':'#818181',
    'seven':'#c0c0c0',
    'eight':'#f1f1f1',
    'nine':'#bac5eb',
    'ten':'#52fff9'
}
# 為分好的每一群賦予標籤

palette = list(legend_dict.values())
vis_params_001 = {'min': 0, 'max': 10, 'palette': palette}


# 顯示地圖
Map = geemap.Map(center=[24.08, 120.56], zoom=10)
left_layer = geemap.ee_tile_layer(image, vis_params, "Sentinel-2")
right_layer = geemap.ee_tile_layer(result001, vis_params_001, "KMeans clustered land cover")
Map.split_map(left_layer, right_layer)
Map.add_legend(title='Land Cover Cluster (KMeans)', legend_dict=legend_dict, draggable=False, position='bottomright')
Map.to_streamlit(height=600)
