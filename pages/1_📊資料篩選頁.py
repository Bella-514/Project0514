import streamlit as st 
import ee
import geemap

st.title("📊 子頁面：資料篩選")

# 檢查是否有日期資訊
if 'start_date' in st.session_state and 'end_date' in st.session_state:
    # 取得主頁選擇的日期
    start = st.session_state['start_date']
    end = st.session_state['end_date']

    st.write(f"你在 *主頁* 選擇的日期區間是：{start} 到 {end}")

    # Earth Engine 火災影像資料集
    dataset = ee.ImageCollection('ESA/CCI/FireCCI/5_1').filterDate(str(start), str(end))
    fire_cover = dataset.select('BurnDate')
    maxBA = fire_cover.max()

    # 火災日期視覺化參數
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
    layer_name = 'BurnDate'

    # 建立互動地圖
    my_Map = geemap.Map()
    my_Map.addLayer(maxBA, baVis, layer_name)
    my_Map.add_colorbar(baVisParam, label=layer_name, layer_name=layer_name)
    my_Map.to_streamlit()

else:
    st.warning("請先回主頁選擇日期區間！")
