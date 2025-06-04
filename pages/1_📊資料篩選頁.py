import streamlit as st
import pandas as pd

st.title("📊 子頁面：資料篩選")

# 檢查是否有日期資訊
if 'start_date' in st.session_state and 'end_date' in st.session_state:
    # 讀取資料
    df = pd.read_csv("2020fire_cover.csv", parse_dates=['日期'])

    # 取得篩選條件
    start = st.session_state['start_date']
    end = st.session_state['end_date']

    # 篩選
    filtered_df = df[(df['日期'] >= pd.to_datetime(start)) & (df['日期'] <= pd.to_datetime(end))]

    st.write(f"你在*主頁*選擇的日期區間是：{start} 到 {end}")
    st.dataframe(filtered_df)
    dataset = ee.ImageCollection('ESA/CCI/FireCCI/5_1').filterDate('2018-01-01', '2020-12-31')
fire_cover = dataset.select('BurnDate')
maxBA = fire_cover.max()

# Use a circular palette to assign colors to date of first detection
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


my_Map = geemap.Map()
my_Map.addLayer(maxBA, baVis, layer_name)
my_Map.add_colorbar(baVisParam, label=layer_name, layer_name=layer_name)
my_Map.streamlit

else:
    st.warning("請先回主頁選擇日期區間！")
