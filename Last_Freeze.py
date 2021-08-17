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
folder = 'LastFreezeDaymet'
reg = [[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]]
scl = 4638.23937
dataset = 'NASA/ORNL/DAYMET'
year = range(1980, 2016)
y = len(year)

def lastFreeze(Temperature):
    date = ee.Date(Temperature.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)
    I = ee.Image(I)
    imag = ee.Image(0).And(Temperature)
    crs = Temperature.projection()
    Temperature = Temperature.expression('b(0) *1.8 + 32').reproject(crs, None, scl)
    Tfreeze = imag.where(Temperature.lte(28),I)
    return Tfreeze.uint8()
    
for yr in range(35, y):
    
    # ############# PART 1 - SELECTION THE DAYMET IMAGE COLLECTION #################
    collection = ee.ImageCollection(dataset).filterDate(datetime.datetime(year[yr], 01, 01), datetime.datetime(year[yr], 12, 31))
    doy_filter = ee.Filter.calendarRange(startdate,enddate,'day_of_year')
    sub_collection = collection.filter(doy_filter).select('tmin')
    # ############################### END PART 1 ###################################
    
    LastFreezeIndex = sub_collection.map(lastFreeze).max()
    
    task = ee.batch.Export.image(LastFreezeIndex, 'LastFreeze_' + str(year[yr]), {'maxPixels': 9999999999, 'driveFolder': folder, 'scale': scl, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
             print 'Running...'
             time.sleep(1)
    print 'Done.', task.status()