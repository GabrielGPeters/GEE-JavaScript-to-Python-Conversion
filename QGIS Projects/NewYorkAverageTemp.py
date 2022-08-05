import ee 
from ee_plugin import Map

#*
 #
 # Author:          Gabriel Peters, ugrad (ggp2366@rit.edu)
 # Latest Version:  0.1.6, 2022-7-20
 # Affiliation:     CIS, Rochester Institute of Technology
 #
 # Purpose:         Gathers and plots ST_B10 data from Landsat 8 L2 data
 #                  from 2013 to present over the state of New York.
 #
 # Notes: for use on other states "scale" for the chart, "max" and "min" for the maplayer, and the actual name of the state will have to be changed
 #
 #
 #

 #IMPORTS
Landsat8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2"),
Landsat7 = ee.ImageCollection("LANDSAT/LE07/C02/T2_L2")

#     ----------------- Collecting Data -----------------

# load US states dataset and isolating New York
stateData = ee.FeatureCollection('TIGER/2018/States')
NewYork = stateData.filter(ee.Filter.eq('NAME', 'New York'))

# print new "NewYork" object and explorer features and properties
print(NewYork)

# add New York outline to the Map as a layer
Map.centerObject(NewYork, 6)
Map.addLayer(NewYork)

# filtering the Landsat 8 image collection
Landsat_8 = Landsat8 \
              .filterDate('2013-1-1', '2022-7-1') \
              .filterMetadata('CLOUD_COVER', 'less_than', 10)

# print size of collection to console
print('Landsat8 collection size: ', Landsat_8.size())

# select only the surface temperature band
STB10 = Landsat_8.select('ST_B10')

# scale to Fahrenheit, set image acquisition time

def func_TEST(img):
  return img \
    .multiply(0.00341802) \
    .add(149.0) \
    .subtract(273) \
    .multiply(1.8) \
    .add(32) \
    .copyProperties(img, ['system:time_start'])

STB10_F = STB10.map(func_TEST)


# scale to Kelvin, set image acquisition time

def func_TEST(img):
  return img \
    .multiply(0.00341802) \
    .add(149.0) \
    .copyProperties(img, ['system:time_start'])

STB10_K = STB10.map(func_TEST)

#     ----------------- Making a Chart ------------------


# chart time series of surface temperature
ts1 = ui.Chart.image.series({
  'imageCollection': STB10_K,
  'region': NewYork,
  'reducer': ee.Reducer.mean(),
  'scale': 200,
  'xProperty': 'system:time_start'
  }) \
  .setOptions({
     'title': 'STB10_K New York Time Series (2013-2021)',
     'vAxis': {'title': 'ST Kelvin'},
     'lineWidth': 1.5,
     'colors': ['red'],
     'trendlines': {
            '0': {  # add a trend line to the 1st series
              'type': 'linear',  # or 'polynomial', 'exponential'
              'color': 'black',
              'pointSize': 0,
              'lineWidth': 2,
              'opacity': 1,
              'visibleInLegend': False,
              }}
  })
print(ts1)

# calculate mean surface temperature for New York in date range
clippedSTB10 = STB10_K.mean().clip(NewYork)


#     ----------------- Adding Map Layers ------------------

# add clipped image layer to the map.
Map.addLayer(clippedSTB10, {
  'min': 283, 'max': 300,
  'palette': ['darkblue', 'blue', 'limegreen', 'yellow', 'orange', 'red', 'darkred', 'black']},
  'Mean temperature (2013-2021)')

#     --------------- Exporting ---------------


# Load Landsat image collection.
allImages = Landsat_8.filterMetadata('CLOUD_COVER', 'less_than', 0.01) \
 .select(['ST_B10'])
 # Make the data 8-bit.

def func_TEST(image):
  return image.multiply(512).uint8() \
 .map(func_TEST)




finalVis = {'min': 283, 'max': 300, 'palette': ['black', 'blue', 'limegreen', 'yellow', 'orange', 'red', 'darkred', 'white']}
def Func(image):
  return image.visualize(finalVis)


finalImage = allImages.map(Func)



