import ee 
from ee_plugin import Map

#*
 #
 # Author:         Gabriel Peters, ugrad (ggp2366@rit.edu)
 # Latest Version: 0.1.3
 # Affiliation:    CIS, Rochester Institute of Technology
 #
 #

#
     ------------------- READ ME ------------------
#
{
#*
 #  Important info:
 #  1. This code is designed to provide estimated surface temperature data
 #     from Landsat 9 Level 2 data, for a specific set of manually selected
 #     coordinates
 #  2. Each section of the code is collapsable, click the arrow by the code
 #     line under each title to view
 #  3. Verbose settings are utilized to make the output easy to understand.
 #     To see fine details set these settings to "True"
 #
 #
 #
}

# Verbose settings:

Verbose = False

Console = False

#
     ----------- Defining TidbiT Geometry ----------
#
{
# Define a Point object.
point1 = ee.Geometry.Point(-76.1646402, 43.6596454); # #1148
point2 = ee.Geometry.Point(-76.1776992, 43.6428234); # #5977
point3 = ee.Geometry.Point(-76.1669502, 43.6500498); # #5967
point4 = ee.Geometry.Point(-76.1839152, 43.6623287); # #3512
point5 = ee.Geometry.Point(-76.1880032, 43.6675437); # #3515

# Print the result to the console.

if (Console === True){
  print('Tidbit Coordinates: ')
  print('point1 = (-76.1646402, 43.6596454)')
  print('point2 = (-76.1776992, 43.6428234)')
  print('point3 = (-76.1669502, 43.6500498)')
  print('point4 = (-76.1839152, 43.6623287)')
  print('point5 = (-76.1880032, 43.6675437)')
}

Map.addLayer(point1,
             {'color': 'red'},
             'Geometry [red]: point1')

Map.addLayer(point2,
             {'color': 'green'},
             'Geometry [green]: point2')

Map.addLayer(point3,
             {'color': 'blue'},
             'Geometry [blue]: point3')

Map.addLayer(point4,
             {'color': 'yellow'},
             'Geometry [yellow]: point4')

Map.addLayer(point5,
             {'color': 'black'},
             'Geometry [black]: point5')



Map.centerObject(point4, 13)
}

#
     --------------- Making a Legend ---------------
#
{
# set position of panel
legend = ui.Panel({
  'style': {
    'position': 'bottom-left',
    'padding': '8px 15px'
  }
})

# Create legend title
legendTitle = ui.Label({
  'value': 'TidbiT Legend',
  'style': {
    'fontSize': '18px',
    'margin': '0 0 4px 0',
    'padding': '0'
    }
})

# Add the title to the panel
legend.add(legendTitle)

# Creates and styles 1 row of the legend.
def makeRow(color, name):

      # Create the label that is actually the colored box.
      colorBox = ui.Label({
        'style': {
          'backgroundColor': '#' + color,
          # Use padding to give the box height and width.
          'padding': '8px',
          'margin': '0 0 4px 0'
        }
      })

      # Create the label filled with the description text.
      description = ui.Label({
        'value': name,
        'style': '{margin': '0 0 4px 6px'}
      })

      # return the panel
      return ui.Panel({
        'widgets': [colorBox, description],
        'layout': ui.Panel.Layout.Flow('horizontal')
      })


#  Palette with the colors
palette =['FF0000', '22ff00', '1500ff', 'FFFF00', '000000']

# name of the legend
names = ['Point1 - #1148','Point2 - #5977','Point3 - #5967',
             'Point4 - #3512','Point5 - #3515']

# Add color and and names
for i in range(0, 5, 1):
  legend.add(makeRow(palette[i], names[i]))


# add legend to map (alternatively you can also print the legend to the console)
Map.add(legend)
}

#
     ------------ Filtering Collection -------------
#
{
#Imports
Landsat9_C2_T1_L2 = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")

# Create an image collection from surface reflectance dataset consisting of only images from days that had sampling occur somewhere

print('Images found...', Landsat9_C2_T1_L2.size())
print('--------------------------------------------------')

imageCollection = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2") \
              .filterDate('2022-6-9', '2022-6-23') \
              .filterMetadata('CLOUD_COVER', 'less_than', 50) \
              .filterBounds(point1)

print('Filtered Over Region: ', imageCollection.size())

if (Verbose === True){
  Map.addLayer(
    Landsat9_C2_T1_L2,
    {'min':0, 'max':65535, 'bands':['ST_B10']},
    'Cloud Filter'
  )
}

#  setting image variable:
#image = ee.Image( INSERT PRODUCT ID );        # get specific image
image = ee.Image(imageCollection.first())

# Get the timestamp and convert it to a date.
date = (ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')).getInfo()
if (Console === True){
  print('Timestamp:', date)
}
# setting surface temperature variable
ST_b10 = image.select('ST_B10')

image1 = ee.Image(image)

if (Verbose === True){
  Map.addLayer(               # adding map layer for surface temp image
      image,
      {'min':0, 'max':65535, 'bands':['ST_B10']},
      'ST_B10'
    )
}
}

#
   ------------ Extracting Pixel Values ------------
#
{
# extract the pixel value for point1
data = image \
.select("ST_B10") \
.reduceRegion(ee.Reducer.first(),point1,10) \
.get("ST_B10")

# convert to number
dataN = ee.Number(data)

scaleFactor = 0.00341802
constant = 149.0

print('--------------------------------------------------')

if (Console === True){
  print('Point1 (Dock): ')

  # pixel value
  print('Pixel Value: ', dataN)
}

# pixel value in Kelvin
surfTemp = dataN.multiply(scaleFactor).add(constant)

if (Console === True){
  print('Pixel Value (Kelvin): ', surfTemp)
}

# pixel value in Fahrenheit
surfTempF = (surfTemp.subtract(273)).multiply(1.8).add(32)

if (Console === True){
  print('Pixel Value (Fahrenheit): ', surfTempF)

  print('--------------------------------------------------')
  print('Point2 (Wigwam): ')
}

# extract the pixel value for point2
data2 = image \
.select("ST_B10") \
.reduceRegion(ee.Reducer.first(),point2,10) \
.get("ST_B10")

# convert to number
dataN2 = ee.Number(data2)

if (Console === True){
  # pixel value
  print('Pixel Value: ', dataN2)
}

# pixel value in Kelvin
surfTemp2 = dataN2.multiply(scaleFactor).add(constant)

if (Console === True){
  print('Pixel Value (Kelvin): ', surfTemp2)
}

# pixel value in Fahrenheit
surfTempF2 = (surfTemp2.subtract(273)).multiply(1.8).add(32)

if (Console === True){
  print('Pixel Value (Fahrenheit): ', surfTempF2)

  print('--------------------------------------------------')
  print('Point3 (Seber): ')
}

# extract the pixel value for point3
data3 = image \
.select("ST_B10") \
.reduceRegion(ee.Reducer.first(),point3,10) \
.get("ST_B10")

# convert to number
dataN3 = ee.Number(data3)

if (Console === True){
  # pixel value
  print('Pixel Value: ', dataN3)
}

# pixel value in Kelvin
surfTemp3 = dataN3.multiply(scaleFactor).add(constant)

if (Console === True){
  print('Pixel Value (Kelvin): ', surfTemp3)
}

# pixel value in Fahrenheit
surfTempF3 = (surfTemp3.subtract(273)).multiply(1.8).add(32)

if (Console === True){
  print('Pixel Value (Fahrenheit): ', surfTempF3)

  print('--------------------------------------------------')
  print('Point4 (South Carl): ')
}

# extract the pixel value for point4
data4 = image \
.select("ST_B10") \
.reduceRegion(ee.Reducer.first(),point4,10) \
.get("ST_B10")

# convert to number
dataN4 = ee.Number(data4)

if (Console === True){
  # pixel value
  print('Pixel Value: ', dataN4)
}

# pixel value in Kelvin
surfTemp4 = dataN4.multiply(scaleFactor).add(constant)

if (Console === True){
  print('Pixel Value (Kelvin): ', surfTemp4)
}

# pixel value in Fahrenheit
surfTempF4 = (surfTemp4.subtract(273)).multiply(1.8).add(32)

if (Console === True){
  print('Pixel Value (Fahrenheit): ', surfTempF4)

  print('--------------------------------------------------')
  print('Point5 (North Carl): ')
}

# extract the pixel value for point5
data5 = image \
.select("ST_B10") \
.reduceRegion(ee.Reducer.first(),point5,10) \
.get("ST_B10")

# convert to number
dataN5 = ee.Number(data5)

if (Console === True){
  # pixel value
  print('Pixel Value: ', dataN5)
}

# pixel value in Kelvin
surfTemp5 = dataN5.multiply(scaleFactor).add(constant)

if (Console === True){
  print('Pixel Value (Kelvin): ', surfTemp5)
}

# pixel value in Fahrenheit
surfTempF5 = (surfTemp5.subtract(273)).multiply(1.8).add(32)

if (Console === True){
  print('Pixel Value (Fahrenheit): ', surfTempF5)
}
}

#
   -------------- Making a Data Table --------------
#
{
# type conversion for table
value1 = dataN.getInfo()
value2 = dataN2.getInfo()
value3 = dataN3.getInfo()
value4 = dataN4.getInfo()
value5 = dataN5.getInfo()
SurfTemp1 = surfTemp.getInfo()
SurfTemp2 = surfTemp2.getInfo()
SurfTemp3 = surfTemp3.getInfo()
SurfTemp4 = surfTemp4.getInfo()
SurfTemp5 = surfTemp5.getInfo()
SurfTempF1 = surfTempF.getInfo()
SurfTempF2 = surfTempF2.getInfo()
SurfTempF3 = surfTempF3.getInfo()
SurfTempF4 = surfTempF4.getInfo()
SurfTempF5 = surfTempF5.getInfo()
time = (ee.Date(image.get('system:time_start')).format('H:'m':s')).getInfo()

print('Data Table:')

dataTable = [
  ['TidbiT', 'Location (Sandy Pond)', 'Pixel Value', 'Kelvin (K)', 'Fahrenheit (F)', '(year-month-day hour:'minute':second)'],
  ['#1148', '(-76.1646402, 43.6596454)', value1, SurfTemp1, SurfTempF1, date + ' ' + time],
  ['#5977', '(-76.1776992, 43.6428234)', value2, SurfTemp2, SurfTempF2, date + ' ' + time],
  ['#5967', '(-76.1669502, 43.6500498)', value3, SurfTemp3, SurfTempF3, date + ' ' + time],
  ['#3512', '(-76.1839152, 43.6623287)', value4, SurfTemp4, SurfTempF4, date + ' ' + time],
  ['#3515', '(-76.1880032, 43.6675437)', value5, SurfTemp5, SurfTempF5, date + ' ' + time],
]

chart = ui.Chart(dataTable).setChartType('Table')
print(chart)
chart.setDownloadable('CSV')
print('Chart is downloadable as: ', chart.getDownloadable())
}

#
   ------------------- Exporting -------------------
#
{
#date = (ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')).getInfo()
image_id = (image.getString('LANDSAT_PRODUCT_ID')).getInfo()
imageIndexId = (image.getString('system:index')).getInfo()
print('Name of export: ' + '"' + image_id  +  '"')
print('Image id: ' + image_id)
print('Image Index: ' + 'LANDSAT/LC09/C02/T1_L2/' + imageIndexId)

# exporting band 10 surface temperature IMAGE
Export.image.toDrive({
  'image': ST_b10,
  'folder': 'Landsat9: ' + date, # folder in your google drive
  'description': 'B10_Surface_Temp',
  'fileNamePrefix': 'B10 Surface Temp',     # name of file will be the date the image was taken
  'scale': 50,
  'maxPixels': 10000000000000
  });#
}
