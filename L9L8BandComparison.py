import ee 
from ee_plugin import Map

 #
 # Author:          Gabriel Peters, ugrad (ggp2366@rit.edu)
 # Latest Version:  0.1.3
 # Affiliation:     CIS, Rochester Institute of Technology
 #
 #

#IMPORTS
Landsat9 = ee.ImageCollection("LANDSAT/LC09/C02/T1_TOA")
Landsat8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")
area = ee.Geometry.Polygon(
        [[[48.238778763727375, 20.8346492143266],
          [48.238778763727375, 19.822650696815533],
          [50.032296830133625, 19.822650696815533],
          [50.032296830133625, 20.8346492143266]]])


# filtering the Landsat 9 image collection
Landsat_9 = Landsat9 \
              .filterDate('2021-12-1', '2022-7-6') \
              .filterMetadata('CLOUD_COVER', 'less_than', 20) \
              .filterBounds(area)

# filtering the Landsat 8 image collection
Landsat_8 = Landsat8 \
              .filterDate('2021-12-1', '2022-7-6') \
              .filterMetadata('CLOUD_COVER', 'less_than', 20) \
              .filterBounds(area)

# print size to console
print('Filtered Image Collections: ')
print('Landsat9: ', Landsat_9.size().getInfo())
print('Landsat8: ', Landsat_8.size().getInfo())

# show image collections on the map
Map.addLayer(
    Landsat_9,
    {'min':0, 'max':0.5, 'bands':['B1']},
    'Landsat9_B1'
  )

Map.addLayer(
    Landsat_8,
    {'min':0, 'max':0.5, 'bands':['B1']},
    'Landsat8_B1'
  )
Map.centerObject(area, 5)

#    ----------------- Landsat 9 -----------------

# converting the collection to a list
L9CollectionList = Landsat_9.toList(Landsat_9.size())

# making a list of sequenced numbers to later fill in
Landsat9List = ee.List.sequence(0, Landsat_9.size().subtract(1))

# function to map over "Landsat9List"
def func(number):
  index = Landsat9List.get(number)
  return (ee.Number(number)).subtract(ee.Number(number)) \
         .add(ee.Number(ee.Image(L9CollectionList.get(index)) \
    .select("B1") \
    .reduceRegion(**{
          'reducer': ee.Reducer.mean().unweighted(),
          'geometry': area,
          'maxPixels': 1e15
          }) \
    .get("B1")))
           


# mapping function over list to get the band 1 values from
# all the images and put them in a list
Landsat9Values = ee.Array(Landsat9List.map(func))
#print('Landsat9Values: ', Landsat9Values)

#     ----------------- Landsat 8 ------------------
     
# converting the collection to a list
L8CollectionList = Landsat_8.toList(Landsat_8.size())

# making a list of sequenced numbers to later fill in
Landsat8List = ee.List.sequence(0, Landsat_8.size().subtract(1))

# function to map over "Landsat8List"
def func(number):
  index = Landsat8List.get(number)
  return (ee.Number(number)).subtract(ee.Number(number)) \
         .add(ee.Number(ee.Image(L8CollectionList.get(index)) \
    .select("B1") \
    .reduceRegion(**{
          'reducer': ee.Reducer.mean().unweighted(),
          'geometry': area,
          'maxPixels': 1e15
          }) \
    .get("B1")))


# mapping function over list to get the band 1 values from
# all the images and put them in a list
Landsat8Values = ee.Array(Landsat8List.map(func))
# print('Landsat8Values: ', Landsat8Values)

#    ----------------- Plotting ------------------

# isolating band 1
L9B1 = Landsat_9.select('B1')
L8B1 = Landsat_8.select('B1')

# plotting functions
def func9(image):
  b1 = image.select('B1')
  return image.addBands(b1.rename('L9_B1'))

def func8(image):
  b1 = image.select('B1')
  return image.addBands(b1.rename('L8_B1'))


# mapping functions over image collections
dataL9 = Landsat_9.map(func9)
dataL8 = Landsat_8.map(func8)

# merge the collections
merged = dataL9.select('L9_B1').merge(dataL8.select('L8_B1'))

# making combined collection chart
'''
print(ui.Chart.image \
  .series({
    'imageCollection': merged,
    'region': area,
    'reducer': ee.Reducer.mean().unweighted(),
    'scale': 5000
  }) \
  .setOptions({
          'title': 'Average Landsat 8/9 B1 Pixel Values Since December 2021',
          'hAxis': {'title': 'Date', 'titleTextStyle': {'italic': False, 'bold': True},
            'viewWindow': {'min': 1638316800000, 'max': 1654560000000}
          },
          'vAxis': {'title': 'TOA Reflectance', 'titleTextStyle': {'italic': False, 'bold': True},
            'viewWindow': {'min': 0.14, 'max': 0.26}},
          'lineWidth': 0,
          'colors': ['f0af07', '76b349'],
          'pointSize': 0.5,
          'opacity': 0.1,
          'trendlines': {
            '0': {  # add a trend line to the 1st series
              'type': 'linear',  # or 'polynomial', 'exponential'
              'color': 'orange',
              'pointSize': 0,
              'lineWidth': 2,
              'opacity': 1,
              'visibleInLegend': False,
              },
            '1': {  # add a trend line to the 2nd series
              'type': 'linear',
              'color': 'green',
              'pointSize': 0,
              'lineWidth': 2,
              'opacity': 1,
              'visibleInLegend': False,
              }
          }
          })

)
'''
#     ------ making list of values to fill in datatable -------

# Landsat 9 Dates
def func_TEST(image):
  return image.set('date', image.date())

datesFunc1 = Landsat_9.map(func_TEST)

# Get a list of the dates.
L9ListDates = datesFunc1.aggregate_array('date')
print('L9ListDates: ', L9ListDates.getInfo())

# Landsat 9 Band 1
L9B1PreList = ee.List.sequence(0, Landsat_9.size().subtract(1))

def funcL9B1(number):
  index = L9B1PreList.get(number)
  return (ee.Number(number)).subtract(ee.Number(number)) \
         .add(ee.Number(ee.Image(L9CollectionList.get(index)) \
    .select("B1") \
    .reduceRegion(**{
          'reducer': ee.Reducer.mean().unweighted(),
          'geometry': area,
          'maxPixels': 1e15
          }) \
    .get("B1")))

L9B1List = ee.List(L9B1PreList.map(funcL9B1))
print('L9B1', L9B1List.getInfo())

# Landsat 9 Band 2
L9B2PreList = ee.List.sequence(0, Landsat_9.size().subtract(1))

def funcL9B2(number):
  index = L9B2PreList.get(number)
  return (ee.Number(number)).subtract(ee.Number(number)) \
         .add(ee.Number(ee.Image(L9CollectionList.get(index)) \
    .select("B2") \
    .reduceRegion(**{
          'reducer': ee.Reducer.mean().unweighted(),
          'geometry': area,
          'maxPixels': 1e15
          }) \
    .get("B2")))

L9B2List = ee.List(L9B2PreList.map(funcL9B2))
print('L9B2', L9B2List.getInfo())

# Landsat 8 Dates

datesFunc2 = Landsat_8.map(func_TEST)

# Get a list of the dates.
L8ListDates = datesFunc2.aggregate_array('date')
print('L8ListDates: ', L8ListDates.getInfo())

# Landsat 8 Band 1
L8B1PreList = ee.List.sequence(0, Landsat_8.size().subtract(1))

def funcL8B1(number):
  index = L8B1PreList.get(number)
  return (ee.Number(number)).subtract(ee.Number(number)) \
         .add(ee.Number(ee.Image(L8CollectionList.get(index)) \
    .select("B1") \
    .reduceRegion(**{
          'reducer': ee.Reducer.mean().unweighted(),
          'geometry': area,
          'maxPixels': 1e15
          }) \
    .get("B1")))

L8B1List = ee.List(L8B1PreList.map(funcL8B1))
print('L8B1', L8B1List.getInfo())

# Landsat 8 Band 2
L8B2PreList = ee.List.sequence(0, Landsat_8.size().subtract(1))

def funcL8B2(number):
  index = L8B2PreList.get(number)
  return (ee.Number(number)).subtract(ee.Number(number)) \
         .add(ee.Number(ee.Image(L8CollectionList.get(index)) \
    .select("B2") \
    .reduceRegion(**{
          'reducer': ee.Reducer.mean().unweighted(),
          'geometry': area,
          'maxPixels': 1e15
          }) \
    .get("B2")))

L8B2List = ee.List(L8B2PreList.map(funcL8B2))
print('L8B2', L8B2List.getInfo())

#    ----------------- Making Downloadable ------------------

L9Size = ee.Number(L9B1List.size().getInfo())
L8Size = ee.Number(L8B1List.size().getInfo())

if (L9Size >= L8Size):
  ListSize = L9Size
elif (L9Size > L8Size):
  ListSize = L8Size


