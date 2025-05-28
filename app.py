import streamlit as st
from datetime import date

st.set_page_config(layout="wide", page_title="這是Streamlit App第二次練習！")

st.title("應用程式主頁")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io), [GEE](https://earthengine.google.com/), 
    [geemap](https://leafmap.org) and [leafmap](https://leafmap.org). 
    """
)

st.header("Instructions")

markdown = """
1. You can use it as a template for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python file.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.
"""

st.markdown(markdown)

# ------------------------
# 日期區間選擇
# ------------------------
st.title("選擇日期區間")

# 避免初始化錯誤：使用 st.session_state.get()
start_date_default = st.session_state.get("start_date", date(2024, 1, 1))
end_date_default = st.session_state.get("end_date", date.today())

# 日期選擇器
start_date = st.date_input("選擇起始日期", value=start_date_default, min_value=date(2018, 1, 1), max_value=date.today())
end_date = st.date_input("選擇結束日期", value=end_date_default, min_value=start_date, max_value=date.today())

# 儲存使用者選擇
st.session_state["start_date"] = start_date
st.session_state["end_date"] = end_date

st.success(f"目前選擇的日期區間為：{start_date} 到 {end_date}")

# ------------------------
# 多媒體區
# ------------------------
st.title("利用擴充器示範")

with st.expander("展示gif檔"):
    try:
        st.image("Amazone_Fire_2019.gif")
    except FileNotFoundError:
        st.error("找不到 GIF 檔案 Amazone_Fire_2019.gif")
