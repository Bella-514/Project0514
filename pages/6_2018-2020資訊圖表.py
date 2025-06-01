import ee
import geemap
import os

# 認證與初始化 Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-s1044013')

# 取得南美洲國家邊界資料（從 LSIB 選取南美洲國家）
south_america_countries = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador",
    "French Guiana", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"
]

# 過濾出南美洲國家
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
south_america = countries.filter(ee.Filter.inList('country_na', south_america_countries))

# 設定視覺化樣式
style = {'color': '#ffff0088', 'fillColor': '#00000000'}

# 取得 FireCCI 影像集並處理 2018–2020
for year in range(2018, 2021):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    dataset = ee.ImageCollection('ESA/CCI/FireCCI/5_1').filterDate(start_date, end_date)
    fire_cover = dataset.select('BurnDate')
    max_burn = fire_cover.max()

    # 設定視覺化參數
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
    layer_name = f"BurnDate {year}"

    # 二值化（如有需要）
    threshold = 50
    confidence_bin = max_burn.gte(threshold).selfMask()

    # 繪製地圖
    my_Map = geemap.Map()
    my_Map.add_basemap('HYBRID')
    my_Map.addLayer(south_america.style(**style), {}, 'South America')
    my_Map.addLayer(max_burn, baVis, layer_name)
    my_Map.add_colorbar(baVisParam, label='BurnDate', layer_name=layer_name)
    my_Map.addLayer(confidence_bin, {'palette': ['red']}, f'Confidence Level bin {year}')
    my_Map.centerObject(south_america, 4)
    my_Map

    # 輸出 zonal statistics 統計 CSV
    csv_name = f"burned_area_{year}.csv"
    geemap.zonal_stats_by_group(
        confidence_bin,
        south_america,
        csv_name,
        statistics_type='SUM',
        denominator=1e6,
        scale=1000,
        verbose=True
    )

    # 顯示圖表
    geemap.pie_chart(
        csv_name,
        names='NAME',
        values='Class_sum',
        max_rows=20,
        height=600,
        title=f"{year} Burned Area"
    )

    geemap.bar_chart(
        csv_name,
        x='NAME',
        y='Class_sum',
        max_rows=20,
        x_label='Country',
        y_label='Fire Area (km²)',
        title=f"{year} Burned Area by Country"
    )
