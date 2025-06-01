import leafmap.foliumap as leafmap  # 建議用 folium backend 相容性更佳
import pandas as pd
import os

# === 檢查檔案是否存在 ===
geojson_path = "custom.geo.json"
csv_path = "south_america_capitals.csv"

if not os.path.exists(geojson_path):
    raise FileNotFoundError(f"找不到 GeoJSON 檔案：{geojson_path}")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"找不到 CSV 檔案：{csv_path}")

# === 載入 CSV ===
cities = pd.read_csv(csv_path)

required_columns = {"longitude", "latitude", "country"}
if not required_columns.issubset(cities.columns):
    raise ValueError(f"CSV 缺少必要欄位：{required_columns - set(cities.columns)}")

# === 建立地圖 ===
m = leafmap.Map(center=[-15, -60], zoom=3)

# === 加入南美洲國界 ===
m.add_geojson(geojson_path, layer_name="South America Countries")

# === 加入首都位置點 ===
m.add_points_from_xy(
    cities,
    x="longitude",
    y="latitude",
    color_column="country",
    icon_names=["flag", "map", "leaf", "globe"],
    spin=True,
    add_legend=True,
)

# === 顯示地圖 ===
m.to_streamlit()  # 如果是在 Jupyter 可用 m.show()
