import streamlit as st
from datetime import date

st.set_page_config(layout="wide", page_title="這是Streamlit App第二次練習！")

st.title("巴西森林大火2018-2020觀察")

st.header("選擇日期區間")

# 初始化 session_state
#if 'start_date' not in st.session_state:
#    st.session_state['start_date'] = date(2024, 1, 1)
#if 'end_date' not in st.session_state:
#    st.session_state['end_date'] = date.today()

st.session_state['start_date'] = date(2018, 1, 1)
st.session_state['end_date'] = date(2020, 12, 31)


# 日期選擇器
start_date = st.date_input(label = "選擇起始日期", value = st.session_state['start_date'], min_value = date(2018, 1, 1), max_value = date.today())
end_date = st.date_input(label = "選擇結束日期", value = st.session_state['end_date'], min_value = start_date, max_value = date.today())

# 儲存使用者選擇
st.session_state['start_date'] = start_date
st.session_state['end_date'] = end_date

st.success(f"目前選擇的日期區間為：{start_date} 到 {end_date}")


st.title("2019亞馬遜森林大火")

with st.expander("展示gif檔"):
    st.image("Amazon_Fire_2019.gif")

with st.expander("播放mp4檔"):
    video_file = open("Amazon_Fire_2019.mp4", "rb")  # "rb"指的是讀取二進位檔案（圖片、影片）
    video_bytes = video_file.read()
    st.video(video_bytes)
    
