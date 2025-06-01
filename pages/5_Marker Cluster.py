import leafmap
import pandas as pd

# 建立地圖並聚焦在南美洲
m = leafmap.Map(center=[-15, -60], zoom=3)

# 讀取 GeoJSON 和 CSV
regions = "south_america.geojson"
cities = pd.read_csv("south_america_capitals.csv")  # ✅ 要讀成 DataFrame

# 加入南美洲國界
m.add_geojson(regions, layer_name="South America Countries")

# 加入首都位置標記
m.add_points_from_xy(
    cities,
    x="longitude",
    y="latitude",
    color_column="country",
    icon_names=["flag", "map", "leaf", "globe"],
    spin=True,
    add_legend=True,
)

m.to_streamlit()
