import leafmap
import pandas as pd

# 建立地圖並聚焦在南美洲
m = leafmap.Map(center=[-15, -60], zoom=3)

# GeoJSON 國界檔案
geojson_path = "custom.geo.json"

# 南美洲首都資料
csv_path = "south_america_capitals.csv"

# 載入 CSV
df = pd.read_csv(csv_path)

# 加入國界圖層
m.add_geojson(geojson_path, layer_name="South America Countries")

# 擴充 icon_names 至足夠數量
icon_list = ["flag", "map", "leaf", "globe", "star", "heart", "rocket", "car", "plane", "sun", "moon", "cloud", "camera"]

# 加入首都點資料
m.add_points_from_xy(
    df,
    x="longitude",
    y="latitude",
    color_column="country",
    icon_names=icon_list,
    spin=True,
    add_legend=True,
)

# 顯示地圖（Streamlit 用）
m.to_streamlit()
