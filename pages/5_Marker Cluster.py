import leafmap
import pandas as pd

# 建立地圖並聚焦在南美洲
m = leafmap.Map(center=[-15, -60], zoom=3)

# 南美洲國界 GeoJSON，可用 Natural Earth 或 GEE 導出
regions = "south_america_countries.geojson"

# 南美洲國家及首都位置資料 CSV 格式
cities = "south_america_capitals.csv"  # 必需包含 `longitude`, `latitude`, `country` 欄位

# 加入國界 GeoJSON
m.add_geojson(regions, layer_name="South America Countries")

# 標示各國首都
m.add_points_from_xy(
    cities,
    x="longitude",
    y="latitude",
    color_column="country",  # 可依國家區分顏色
    icon_names=["flag", "map", "leaf", "globe"],  # 可自由調整 icon
    spin=True,
    add_legend=True,
)

m.to_streamlit()  # 若在 Streamlit 中顯示，否則用 m.show()
