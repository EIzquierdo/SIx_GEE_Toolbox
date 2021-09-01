# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 10:39:20 2016

@author:************************************************************************************************
//*****************       Authors: Emma Izquierdo-Verdiguier and Raúl Zurita-Milla     *****************/
//*****************      Contact: {e.izquierdoverdiguier,r.zurita-milla}@utwente.nl    *****************/
//*****************    ITC -- Faculty of Geo-information Science & Earth Observation   *****************/
//*****************               Dept of Geoinformation Processing (GIP)              *****************/
//*****************                         University of Twente                       *****************/
//*****************         Hengelosestraat 99, 7500 AA Enschede, The Netherlands      *****************/
//******************************************************************************************************/

//******************************************************************************************************/
//*****************      Acknowledgments to I.Garcia-Martí, D. Romano and R. Munde     *****************/
//******************************************************************************************************/

//******************************************************************************************************/
//*****************                   Spring Index Model Script v1.0                   *****************/
//******************************************************************************************************/

//If you use the software, please cite this paper: E. Izquierdo-Verdiguier, R. Zurita-Milla, T. R. Ault,
M. D. Schwartz; "Development and analysis of spring plant phenology: 36 years of 1-km grids over the
conterminous US", (submitted) Environmental Modeling and Software journal, 2017.

// Copyright (c) 2017  Emma Izquierdo-Verdiguier and Raúl Zurita-Milla

"""

import ee
import time
import datetime 
ee.Initialize()

startdate = 1
enddate = 250
user = 'users/Emma/'
folder = 'LastFreeze_European'
reg = ee.Geometry.Polygon([[[-10.5833, 71.2583], [-10.5833, 35.99],
                            [44.816, 35.99], [44.816, 71.2583]]])
scl = 1000
dataset = 'users/Emma/E_Obs/' 
year = range(1980, 2016)
y = len(year)

# #************************************** ADDING syste:time_start property ******************************************/

def timeStart(img):
    I = ee.String(img.id().split('_').get(1))
    I = ee.Number.parse(I)
    const = 24 * 60 * 60 * 1000
    sys_time = ee.Number(946684800000).add(ee.Number(const).multiply(I.subtract(ee.Number(1))))
    return img.set({"system:time_start": sys_time})


def lastFreeze(Temperature):
    date = ee.Date(Temperature.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)
    I = ee.Image(I)
    Temperature = Temperature.select(1)
    imag = ee.Image(0).And(Temperature)
    Temperature = Temperature.expression('b(0) *1.8/100 + 32')
    Tfreeze = imag.where(Temperature.lte(28),I)
    return Tfreeze.uint8()
    
for yr in range(35, y):
    print(yr)
    # ############# PART 1 - SELECTION THE DAYMET IMAGE COLLECTION #################
    collection = ee.ImageCollection('users/Emma/E_Obs/' + str(yr))
    collection = collection.map(timeStart)
    collection = collection.sort('system:time_start')
    # ############################### END PART 1 ###################################
    
    LastFreezeIndex = collection.map(lastFreeze).max()
    
     imageAsset = user + folder + '/' + str(yr)
     task = ee.batch.Export.image.toAsset(image=LastFreezeIndex, description=str(yr), assetId=imageAsset, region=reg, scale=scl, maxPixels=9999999999)
    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.'), task.status()

    nameImage = str(yr)
    task = ee.batch.Export.image.toDrive(image=LastFreezeIndex, description=nameImage,
                                         maxPixels=9999999999, driveFolder=folder,
                                         scale=scl, region=reg)
    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.'), task.status()
