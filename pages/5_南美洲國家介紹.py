import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")

markdown = """
中南美洲國家
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://emojiisland.com/cdn/shop/products/Earth_Globe_Americas_Emoji_grande.png?v=1571606063"
st.sidebar.image(logo)

st.title("South America Marker Cluster")

with st.expander("See source code"):
    with st.echo():

        # 建立地圖，南美洲中心座標
        m = leafmap.Map(center=[-15, -60], zoom=8)

        # 南美洲國界 GeoJSON 路徑
        geojson_path = "custom.geo.json"

        # 南美洲首都資料
        data = [
            {"country": "Brazil", "capital": "Brasilia", "latitude": -15.793889, "longitude": -47.882778},
            {"country": "Argentina", "capital": "Buenos Aires", "latitude": -34.603722, "longitude": -58.381592},
            {"country": "Peru", "capital": "Lima", "latitude": -12.046374, "longitude": -77.042793},
            {"country": "Colombia", "capital": "Bogotá", "latitude": 4.7110, "longitude": -74.0721},
            {"country": "Chile", "capital": "Santiago", "latitude": -33.4489, "longitude": -70.6693},
            {"country": "Ecuador", "capital": "Quito", "latitude": -0.1807, "longitude": -78.4678},
            {"country": "Venezuela", "capital": "Caracas", "latitude": 10.4806, "longitude": -66.9036},
            {"country": "Paraguay", "capital": "Asunción", "latitude": -25.2637, "longitude": -57.5759},
            {"country": "Uruguay", "capital": "Montevideo", "latitude": -34.9011, "longitude": -56.1645},
            {"country": "Bolivia", "capital": "Sucre", "latitude": -19.0196, "longitude": -65.2619},
            {"country": "Guyana", "capital": "Georgetown", "latitude": 6.8013, "longitude": -58.1551},
            {"country": "Suriname", "capital": "Paramaribo", "latitude": 5.8520, "longitude": -55.2038},
            {"country": "French Guiana", "capital": "Cayenne", "latitude": 4.9224, "longitude": -52.3135}
        ]
        df = pd.DataFrame(data)

        # 加入國界圖層
        m.add_geojson(geojson_path, layer_name="South America Countries")

        # 定義 icon 名稱（數量與資料列數相符）
        icon_list = [
            "flag", "star", "cloud", "home", "leaf", "fire", "heart", 
            "gift", "bell", "camera", "music", "glass", "phone"
        ]

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

        # 顯示地圖
        m.to_streamlit(height=700)
