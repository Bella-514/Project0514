import leafmap
import pandas as pd
import geopandas as gpd
import os
import streamlit as st

# 建立地圖並聚焦在南美洲
m = leafmap.Map(center=[-15, -60], zoom=3)

# 使用你的 GeoJSON 檔案
geojson_path = "custom.geo.json"

# 檢查 GeoJSON 檔案是否存在
if not os.path.exists(geojson_path):
    st.error("❌ 找不到 custom.geo.json 檔案，請確認檔案路徑是否正確")
else:
    try:
        regions = gpd.read_file(geojson_path)
        m.add_geojson(regions, layer_name="South America Countries")
    except Exception as e:
        st.error(f"❌ 載入 GeoJSON 檔案失敗：{e}")

# 首都位置 CSV（需包含 longitude, latitude, country 欄位）
csv_path = "south_america_capitals.csv"

if not os.path.exists(csv_path):
    st.error("❌ 找不到 south_america_capitals.csv 檔案")
else:
    try:
        cities = pd.read_csv(csv_path)
        m.add_points_from_xy(
            cities,
            x="longitude",
            y="latitude",
            color_column="country",
            icon_names=["flag", "map", "leaf", "globe"],
            spin=True,
            add_legend=True,
        )
    except Exception as e:
        st.error(f"❌ 載入 CSV 點資料失敗：{e}")

# 顯示地圖
m.to_streamlit()
