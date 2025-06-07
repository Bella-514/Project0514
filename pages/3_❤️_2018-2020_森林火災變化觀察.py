import streamlit as st
import ee
import datetime
import time # For animation delay

st.set_page_config(layout="wide")
st.title("🔥 2018-2020 年森林火災變化觀察")

# Initialize Earth Engine
# Ensure Earth Engine is initialized only once.
if not ee.data._initialized:
    ee.Initialize()

# Sidebar parameters for year selection
st.sidebar.title("📅 選擇觀察年份")
# Slider to select the year between 2018 and 2020, defaulting to 2018.
year = st.sidebar.slider("選擇年份", 2018, 2020, 2018)

st.sidebar.write("📌 使用 MODIS 火災資料")

# Define the Region of Interest (ROI): South American Amazon
# Bounding box coordinates: [west, south, east, north]
roi = ee.Geometry.BBox(-75, -15, -45, 5)

# Visualization parameters for the burn date images
# 'BurnDate' band values typically range from 1 to 366 (day of year).
# Values outside this range (e.g., 0 for no burn) will be black due to 'min'.
vis_params = {
    'min': 30, # Minimum burn date (e.g., burn occurred after day 30 of the year)
    'max': 365, # Maximum burn date
    'palette': ['black', 'orange', 'red'] # Color palette for visualization
}

# Display a main title for the animation section
st.markdown(f"### 🎞️ {year} 年火災變化動畫（含日期）")

# Create a Streamlit empty placeholder. This placeholder will be updated dynamically
# with new date text and images to create the animation effect.
placeholder = st.empty()

# List to store the URLs of the monthly images and their corresponding dates.
image_data_frames = []

# Iterate through each month of the selected year (from 1 to 12).
for month in range(1, 13):
    # Construct the start date for the current month.
    month_start_date = datetime.datetime(year, month, 1)

    # Calculate the end date for the current month.
    # For December, it's explicitly the 31st.
    # For other months, it's the day before the 1st of the next month.
    if month == 12:
        month_end_date = datetime.datetime(year, month, 31)
    else:
        month_end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)

    # Filter the MODIS/006/MCD64A1 ImageCollection for the current month and ROI.
    # Select the 'BurnDate' band.
    # The MCD64A1 dataset provides monthly burn area composites.
    monthly_image_collection = ee.ImageCollection('MODIS/006/MCD64A1') \
        .filterBounds(roi) \
        .filterDate(month_start_date.strftime('%Y-%m-%d'), month_end_date.strftime('%Y-%m-%d')) \
        .select('BurnDate')

    # Check if there's any data for the current month.
    # .getInfo() is needed to execute the EE call and get the Python object.
    if monthly_image_collection.size().getInfo() > 0:
        # If there's data, take the maximum 'BurnDate' value within the month.
        # This aggregates potentially multiple burn events in a month into a single image,
        # representing the latest burn day for each pixel within that month.
        monthly_image = monthly_image_collection.max()
        
        # Apply a mask to only show valid burn data (BurnDate > 0).
        # Values of 0 in 'BurnDate' typically indicate no burn.
        monthly_image = monthly_image.updateMask(monthly_image.gt(0))
        
        # Get the thumbnail URL for the aggregated monthly image using the defined visualization parameters.
        # This generates a static image for the current month.
        thumb_url = monthly_image.getThumbURL(vis_params)
        
        # Add the generated URL and its corresponding date string to our list.
        image_data_frames.append({
            'url': thumb_url,
            'date_str': month_start_date.strftime('%Y-%m-%d') # Format date as YYYY-MM-DD
        })
    else:
        # If no burn data is found for the month, skip this month.
        # You could also add a placeholder image or a message here if desired.
        print(f"Skipping month {month} of {year} due to no data.")

# Play the animation if there are frames to display.
if len(image_data_frames) > 0:
    for frame in image_data_frames:
        # Use the placeholder to update the content dynamically.
        with placeholder.container():
            # Display the date above the image.
            st.write(f"### 日期: {frame['date_str']}")
            # Display the image, making it fill the column width.
            st.image(frame['url'], use_column_width=True)
            # Pause execution for a short duration to create the animation effect.
            # Adjust the delay (in seconds) as needed for desired speed.
            time.sleep(0.5) 
else:
    # Message displayed if no fire data is found for the selected year.
    st.write(f"在 {year} 年找不到火災資料。")
