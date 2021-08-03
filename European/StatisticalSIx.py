# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:05:21 2015

@author: emma
"""

import ee
import time
ee.Initialize()

maskEurope = ee.Image("users/Emma/MaskEurope2")

image22Bl = ee.Image('users/Emma/BloomEuropean/2002').set({'system:time_start': (ee.Number(1009843200000))})
image23Bl = ee.Image('users/Emma/BloomEuropean/2003').set({'system:time_start': (ee.Number(1041379200000))})
image24Bl = ee.Image('users/Emma/BloomEuropean/2004').set({'system:time_start': (ee.Number(1072915200000))})
image25Bl = ee.Image('users/Emma/BloomEuropean/2005').set({'system:time_start': (ee.Number(1104537600000))})
image26Bl = ee.Image('users/Emma/BloomEuropean/2006').set({'system:time_start': (ee.Number(1136073600000))})
image27Bl = ee.Image('users/Emma/BloomEuropean/2007').set({'system:time_start': (ee.Number(1167609600000))})
image28Bl = ee.Image('users/Emma/BloomEuropean/2008').set({'system:time_start': (ee.Number(1199145600000))})
image29Bl = ee.Image('users/Emma/BloomEuropean/2009').set({'system:time_start': (ee.Number(1230768000000))})
image30Bl = ee.Image('users/Emma/BloomEuropean/2010').set({'system:time_start': (ee.Number(1262304000000))})
image31Bl = ee.Image('users/Emma/BloomEuropean/2011').set({'system:time_start': (ee.Number(1293840000000))})
image32Bl = ee.Image('users/Emma/BloomEuropean/2012').set({'system:time_start': (ee.Number(1325376000000))})
image33Bl = ee.Image('users/Emma/BloomEuropean/2013').set({'system:time_start': (ee.Number(1356998400000))})
image34Bl = ee.Image('users/Emma/BloomEuropean/2014').set({'system:time_start': (ee.Number(1388534400000))})
image35Bl = ee.Image('users/Emma/BloomEuropean/2015').set({'system:time_start': (ee.Number(1420070400000))})
image36Bl = ee.Image('users/Emma/BloomEuropean/2016').set({'system:time_start': (ee.Number(1451606400000))})
image37Bl = ee.Image('users/Emma/BloomEuropean/2017').set({'system:time_start': (ee.Number(1483228800000))})
#
#
image22SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2002').set({'system:time_start': (ee.Number(1009843200000))})
image23SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2003').set({'system:time_start': (ee.Number(1041379200000))})
image24SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2004').set({'system:time_start': (ee.Number(1072915200000))})
image25SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2005').set({'system:time_start': (ee.Number(1104537600000))})
image26SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2006').set({'system:time_start': (ee.Number(1136073600000))})
image27SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2007').set({'system:time_start': (ee.Number(1167609600000))})
image28SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2008').set({'system:time_start': (ee.Number(1199145600000))})
image29SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2009').set({'system:time_start': (ee.Number(1230768000000))})
image30SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2010').set({'system:time_start': (ee.Number(1262304000000))})
image31SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2011').set({'system:time_start': (ee.Number(1293840000000))})
image32SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2012').set({'system:time_start': (ee.Number(1325376000000))})
image33SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2013').set({'system:time_start': (ee.Number(1356998400000))})
image34SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2014').set({'system:time_start': (ee.Number(1388534400000))})
image35SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2015').set({'system:time_start': (ee.Number(1420070400000))})
image36SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2016').set({'system:time_start': (ee.Number(1451606400000))})
image37SOS = ee.Image('users/Emma/SOS_MODIS/MCD13A2_2017').set({'system:time_start': (ee.Number(1483228800000))})

image22Lf = ee.Image('users/Emma/LeafEuropean/2002').set({'system:time_start': (ee.Number(1009843200000))})
image23Lf = ee.Image('users/Emma/LeafEuropean/2003').set({'system:time_start': (ee.Number(1041379200000))})
image24Lf = ee.Image('users/Emma/LeafEuropean/2004').set({'system:time_start': (ee.Number(1072915200000))})
image25Lf = ee.Image('users/Emma/LeafEuropean/2005').set({'system:time_start': (ee.Number(1104537600000))})
image26Lf = ee.Image('users/Emma/LeafEuropean/2006').set({'system:time_start': (ee.Number(1136073600000))})
image27Lf = ee.Image('users/Emma/LeafEuropean/2007').set({'system:time_start': (ee.Number(1167609600000))})
image28Lf = ee.Image('users/Emma/LeafEuropean/2008').set({'system:time_start': (ee.Number(1199145600000))})
image29Lf = ee.Image('users/Emma/LeafEuropean/2009').set({'system:time_start': (ee.Number(1230768000000))})
image30Lf = ee.Image('users/Emma/LeafEuropean/2010').set({'system:time_start': (ee.Number(1262304000000))})
image31Lf = ee.Image('users/Emma/LeafEuropean/2011').set({'system:time_start': (ee.Number(1293840000000))})
image32Lf = ee.Image('users/Emma/LeafEuropean/2012').set({'system:time_start': (ee.Number(1325376000000))})
image33Lf = ee.Image('users/Emma/LeafEuropean/2013').set({'system:time_start': (ee.Number(1356998400000))})
image34Lf = ee.Image('users/Emma/LeafEuropean/2014').set({'system:time_start': (ee.Number(1388534400000))})
image35Lf = ee.Image('users/Emma/LeafEuropean/2015').set({'system:time_start': (ee.Number(1420070400000))})
image36Lf = ee.Image('users/Emma/LeafEuropean/2016').set({'system:time_start': (ee.Number(1451606400000))})
image37Lf = ee.Image('users/Emma/LeafEuropean/2017').set({'system:time_start': (ee.Number(1483228800000))})

ImageCollectionBl = ee.ImageCollection([image22Bl, image23Bl, image24Bl, image25Bl,
                                        image26Bl, image27Bl, image28Bl, image29Bl, image30Bl, image31Bl, image32Bl,
                                        image33Bl, image34Bl, image35Bl, image36Bl, image37Bl])

ImageCollectionLf = ee.ImageCollection([image22Lf, image23Lf, image24Lf, image25Lf, image26Lf, image27Lf, image28Lf,
                                        image29Lf, image30Lf, image31Lf, image32Lf, image33Lf, image34Lf, image35Lf,
                                        image36Lf, image37Lf])

ImageCollectionSOS = ee.ImageCollection([image22SOS, image23SOS, image24SOS, image25SOS, image26SOS, image27SOS,
                                         image28SOS, image29SOS, image30SOS, image31SOS, image32SOS, image33SOS,
                                         image34SOS, image35SOS, image36SOS, image37SOS])




def maskimages(img):
    return img.multiply(maskEurope)


ImageCollectionLf = ImageCollectionLf.map(maskimages)
ImageCollectionBl = ImageCollectionBl.map(maskimages)
ImageCollectionSOS = ImageCollectionSOS.map(maskimages)

# ImageCollectionDI = ee.ImageCollection([imageLf.subtract(imageLastF).copyProperties(imageLf, ['system:index','system:time_start']),
#                                         image1Lf.subtract(image1LastF).copyProperties(image1Lf, ['system:index','system:time_start']),
#                                         image2Lf.subtract(image2LastF).copyProperties(image2Lf, ['system:index','system:time_start']),
#                                         image3Lf.subtract(image3LastF).copyProperties(image3Lf, ['system:index','system:time_start']),
#                                         image4Lf.subtract(image4LastF).copyProperties(image4Lf, ['system:index','system:time_start']),
#                                         image5Lf.subtract(image5LastF).copyProperties(image5Lf, ['system:index','system:time_start']),
# image6Lf.subtract(image6LastF).copyProperties(image6Lf, ['system:index','system:time_start']),
#                                         image7Lf.subtract(image7LastF).copyProperties(image7Lf, ['system:index','system:time_start']),
#                                         image8Lf.subtract(image8LastF).copyProperties(image8Lf, ['system:index','system:time_start']),
#                                         image9Lf.subtract(image9LastF).copyProperties(image9Lf, ['system:index','system:time_start']),
#                                         image10Lf.subtract(image10LastF).copyProperties(image10Lf, ['system:index','system:time_start']),
#                                         image11Lf.subtract(image11LastF).copyProperties(image11Lf, ['system:index','system:time_start']),
#                                         image12Lf.subtract(image12LastF).copyProperties(image12Lf, ['system:index','system:time_start']),
#                                         image13Lf.subtract(image13LastF).copyProperties(image13Lf, ['system:index','system:time_start']),
# image14Lf.subtract(image14LastF).copyProperties(image14Lf, ['system:index','system:time_start']),
#                                         image15Lf.subtract(image15LastF).copyProperties(image15Lf, ['system:index','system:time_start']),
#                                         image16Lf.subtract(image16LastF).copyProperties(image16Lf, ['system:index','system:time_start']),
#                                         image17Lf.subtract(image17LastF).copyProperties(image17Lf, ['system:index','system:time_start']),
# image18Lf.subtract(image18LastF).copyProperties(image18Lf, ['system:index','system:time_start']),
#                                         image19Lf.subtract(image19LastF).copyProperties(image19Lf, ['system:index','system:time_start']),
#                                         image20Lf.subtract(image20LastF).copyProperties(image20Lf, ['system:index','system:time_start']),
#                                         image21Lf.subtract(image21LastF).copyProperties(image21Lf, ['system:index','system:time_start']),
# image22Lf.subtract(image22LastF).copyProperties(image22Lf, ['system:index','system:time_start']),
#                                         image23Lf.subtract(image23LastF).copyProperties(image23Lf, ['system:index','system:time_start']),
#                                         image24Lf.subtract(image24LastF).copyProperties(image24Lf, ['system:index','system:time_start']),
#                                         image25Lf.subtract(image25LastF).copyProperties(image25Lf, ['system:index','system:time_start']),
# image26Lf.subtract(image26LastF).copyProperties(image26Lf, ['system:index','system:time_start']),
#                                         image27Lf.subtract(image27LastF).copyProperties(image27Lf, ['system:index','system:time_start']),
#                                         image28Lf.subtract(image28LastF).copyProperties(image28Lf, ['system:index','system:time_start']),
#                                         image29Lf.subtract(image29LastF).copyProperties(image29Lf, ['system:index','system:time_start']),
# image30Lf.subtract(image30LastF).copyProperties(image30Lf, ['system:index','system:time_start']),
#                                         image31Lf.subtract(image31LastF).copyProperties(image31Lf, ['system:index','system:time_start']),
#                                         image32Lf.subtract(image32LastF).copyProperties(image32Lf, ['system:index','system:time_start']),
#                                         image33Lf.subtract(image33LastF).copyProperties(image33Lf, ['system:index','system:time_start']),
#                                         image34Lf.subtract(image34LastF).copyProperties(image34Lf, ['system:index','system:time_start']),
#                                         image35Lf.subtract(image35LastF).copyProperties(image35Lf, ['system:index','system:time_start'])])

# climaticMean = ee.Image(ee.ImageCollection([image1Lf.subtract(image1LastF).copyProperties(image1Lf, ['system:index','system:time_start']),
#                                         image2Lf.subtract(image2LastF).copyProperties(image2Lf, ['system:index','system:time_start']),
#                                         image3Lf.subtract(image3LastF).copyProperties(image3Lf, ['system:index','system:time_start']),
#                                         image4Lf.subtract(image4LastF).copyProperties(image4Lf, ['system:index','system:time_start']),
#                                         image5Lf.subtract(image5LastF).copyProperties(image5Lf, ['system:index','system:time_start']),
#                                         image6Lf.subtract(image6LastF).copyProperties(image6Lf, ['system:index','system:time_start']),
#                                         image7Lf.subtract(image7LastF).copyProperties(image7Lf, ['system:index','system:time_start']),
#                                         image8Lf.subtract(image8LastF).copyProperties(image8Lf, ['system:index','system:time_start']),
#                                         image9Lf.subtract(image9LastF).copyProperties(image9Lf, ['system:index','system:time_start']),
#                                         image10Lf.subtract(image10LastF).copyProperties(image10Lf, ['system:index','system:time_start']),
#                                         image11Lf.subtract(image11LastF).copyProperties(image11Lf, ['system:index','system:time_start']),
#                                         image12Lf.subtract(image12LastF).copyProperties(image12Lf, ['system:index','system:time_start']),
#                                         image13Lf.subtract(image13LastF).copyProperties(image13Lf, ['system:index','system:time_start']),
#                                         image14Lf.subtract(image14LastF).copyProperties(image14Lf, ['system:index','system:time_start']),
#                                         image15Lf.subtract(image15LastF).copyProperties(image15Lf, ['system:index','system:time_start']),
#                                         image16Lf.subtract(image16LastF).copyProperties(image16Lf, ['system:index','system:time_start']),
#                                         image17Lf.subtract(image17LastF).copyProperties(image17Lf, ['system:index','system:time_start']),
#                                         image18Lf.subtract(image18LastF).copyProperties(image18Lf, ['system:index','system:time_start']),
#                                         image19Lf.subtract(image19LastF).copyProperties(image19Lf, ['system:index','system:time_start']),
#                                         image20Lf.subtract(image20LastF).copyProperties(image20Lf, ['system:index','system:time_start']),
#                                         image21Lf.subtract(image21LastF).copyProperties(image21Lf, ['system:index','system:time_start']),
#                                         image22Lf.subtract(image22LastF).copyProperties(image22Lf, ['system:index','system:time_start']),
#                                         image23Lf.subtract(image23LastF).copyProperties(image23Lf, ['system:index','system:time_start']),
#                                         image24Lf.subtract(image24LastF).copyProperties(image24Lf, ['system:index','system:time_start']),
#                                         image25Lf.subtract(image25LastF).copyProperties(image25Lf, ['system:index','system:time_start']),
#                                         image26Lf.subtract(image26LastF).copyProperties(image26Lf, ['system:index','system:time_start']),
#                                         image27Lf.subtract(image27LastF).copyProperties(image27Lf, ['system:index','system:time_start']),
#                                         image28Lf.subtract(image28LastF).copyProperties(image28Lf, ['system:index','system:time_start']),
#                                         image29Lf.subtract(image29LastF).copyProperties(image29Lf, ['system:index','system:time_start']),
#                                         image30Lf.subtract(image30LastF).copyProperties(image30Lf, ['system:index','system:time_start'])]).mean())
# def meanValueImage(image):
#     # meanValue = image.reduceRegion(reducer=ee.Reducer.mean(), bestEffort=True, maxPixels=100000000)
#     pr = image.select('b1').subtract(climaticMean.select('b1'))\
#     .addBands(image.select('b2').subtract(climaticMean.select('b2')))\
#     .addBands(image.select('b3').subtract(climaticMean.select('b3')))\
#     .addBands(image.select('b4').subtract(climaticMean.select('b4'))).\
#         copyProperties(image,['system:index','system:time_start'])
#     return pr
#
# DI_center = ImageCollectionDI.map(meanValueImage)
#
# def FSI(image):
#     false = image.where(image.lte(7),1)
#     false =false.where(false.gt(7),0)
#     return false
#
# falseSpring = ImageCollectionDI.map(FSI)

scl = 1000
reg =ee.Geometry.Polygon([[[-10.5833, 71.2583], [-10.5833, 35.99],
                           [44.816, 35.99], [44.816, 71.2583]]])

# Leaf_Collection_mean = ImageCollectionLf.mean()
# task = ee.batch.Export.image(Leaf_Collection_mean.multiply(maskEurope), 'Leaf_mean', {'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#          print 'Running...'
#          time.sleep(1)
# print 'Done.', task.status()
#
# Leaf_Collection_std = ImageCollectionLf.reduce(ee.Reducer.sampleStdDev())
# task = ee.batch.Export.image(Leaf_Collection_std.multiply(maskEurope), 'Leaf_std', {'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#          print 'Running...'
#          time.sleep(1)
# print 'Done.', task.status()

# Leaf_Collection_trend = ImageCollectionLf.select(3).formaTrend()
# task = ee.batch.Export.image(Leaf_Collection_trend.select(0).multiply(maskEurope), 'Leaf_trend', {'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#          print 'Running...'
#          time.sleep(1)
# print 'Done.', task.status()

# Leaf_Collection_max = ImageCollectionLf.max()
# task = ee.batch.Export.image(Leaf_Collection_max.multiply(maskEurope),'Leaf_max',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# Leaf_Collection_min =ImageCollectionLf.min();
# task = ee.batch.Export.image(Leaf_Collection_min.multiply(maskEurope),'Leaf_min',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# Leaf_Collection_median = ImageCollectionLf.median();
# task = ee.batch.Export.image(Leaf_Collection_median.multiply(maskEurope),'Leaf_median',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# Leaf_Collection_mode = ImageCollectionLf.mode();
# task = ee.batch.Export.image(Leaf_Collection_mode.multiply(maskEurope),'Leaf_mode',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()

# Bloom_Collection_mean = ImageCollectionBl.mean()
# task = ee.batch.Export.image(Bloom_Collection_mean.multiply(maskEurope),'Bloom_mean',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#          print 'Running...'
#          time.sleep(1)
# print 'Done.', task.status()
#
# Bloom_Collection_std = ImageCollectionBl.reduce(ee.Reducer.sampleStdDev())
# task = ee.batch.Export.image(Bloom_Collection_std.multiply(maskEurope),'Bloom_std',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#          print 'Running...'
#          time.sleep(1)
# print 'Done.', task.status()

# Leaf_Collection_trend = ImageCollectionBl.select(3).formaTrend()
# task = ee.batch.Export.image(Leaf_Collection_trend.select(0).multiply(maskEurope),'Bloom_trend',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#          print 'Running...'
#          time.sleep(1)
# print 'Done.', task.status()

# Bloom_Collection_max = ImageCollectionBl.max()
# task = ee.batch.Export.image(Bloom_Collection_max.multiply(maskEurope),'Bloom_max',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# Bloom_Collection_min =ImageCollectionBl.min()
# task = ee.batch.Export.image(Bloom_Collection_min.multiply(maskEurope),'Bloom_min',{'Bloom_min':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# Bloom_Collection_median = ImageCollectionBl.median()
# task = ee.batch.Export.image(Bloom_Collection_median.multiply(maskEurope),'Bloom_median',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()

# Bloom_Collection_mode = ImageCollectionBl.mode()
# task = ee.batch.Export.image(Bloom_Collection_mode.multiply(maskEurope),'Bloom_mode',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
SOS_Collection_mean = ImageCollectionSOS.mean()
task = ee.batch.Export.image(SOS_Collection_mean.multiply(maskEurope), 'SOS_mean', {'maxPixels':9999999999,'scale':scl,'region':reg})
task.start()
while task.status()['state'] == 'RUNNING':
         print ('Running...')
         time.sleep(1)
print ('Done.'), task.status()

SOS_Collection_std = ImageCollectionSOS.reduce(ee.Reducer.sampleStdDev())
task = ee.batch.Export.image(SOS_Collection_std.multiply(maskEurope), 'SOS_std', {'maxPixels':9999999999,'scale':scl,'region':reg})
task.start()
while task.status()['state'] == 'RUNNING':
         print ('Running...')
         time.sleep(1)
print ('Done.'), task.status()

# SOS_Collection_trend = ImageCollectionSOS.formaTrend()
# task = ee.batch.Export.image(SOS_Collection_trend.select(0).multiply(maskEurope), 'SOS_trend', {'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#          print 'Running...'
#          time.sleep(1)
# print 'Done.', task.status()
#
# SOS_Collection_max = ImageCollectionSOS.max()
# task = ee.batch.Export.image(SOS_Collection_max.multiply(maskEurope),'SOS_max',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# SOS_Collection_min =ImageCollectionSOS.min()
# task = ee.batch.Export.image(SOS_Collection_min.multiply(maskEurope),'SOS_min',{'Bloom_min':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# SOS_Collection_median = ImageCollectionSOS.median()
# task = ee.batch.Export.image(SOS_Collection_median.multiply(maskEurope),'SOS_median',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
#
# SOS_Collection_mode = ImageCollectionSOS.mode()
# task = ee.batch.Export.image(SOS_Collection_mode.multiply(maskEurope),'SOS_mode',{'maxPixels':9999999999,'scale':scl,'region':reg})
# task.start()
# while task.status()['state'] == 'RUNNING':
#         print 'Running...'
#         time.sleep(1)
# print 'Done.', task.status()
