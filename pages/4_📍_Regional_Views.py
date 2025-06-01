my_point = ee.Geometry.BBox(-63.0, -15.0, -47.0, -2.0)

my_img = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(my_point)
    .filterDate('2018-01-01', '2024-12-31')
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)

vis_params = {'min':100, 'max': 3500, 'bands': ['B11',  'B8',  'B3']}


my_Map.addLayer(my_img, vis_params, "Sentinel-2")
my_Map

my_lc = ee.Image('ESA/WorldCover/v200/2021')
# ESA WorldCover 10m v200
# https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100#bands

classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
label = 'lc'
my_lc = my_lc.remap(classValues, remapValues, bandName='Map').rename(label).toByte()

# ee.Image.remap() https://developers.google.com/earth-engine/apidocs/ee-image-remap#colab-python
# ee.Iamge.rename() https://developers.google.com/earth-engine/apidocs/ee-image-rename
# ee.Image.toByte() 把影像像素值轉換為unsigned 8-bit integer （即0~255） https://developers.google.com/earth-engine/apidocs/ee-image-tobyte

geemap.get_info(my_lc)

classVis = {
  'min': 0,
  'max': 10,
  'palette': ['006400' ,'ffbb22', 'ffff4c', 'f096ff', 'fa0000', 'b4b4b4',
            'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0']
}


my_Map.addLayer(my_lc, classVis, "ESA WorldCover 10m v200")
my_Map.add_legend(title='ESA Land Cover Type', builtin_legend='ESA_WorldCover')
my_Map
