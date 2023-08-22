# -*- coding: utf-8 -*-
"""

********************************************************************************************************/
//*****************       Authors: Emma Izquierdo-Verdiguier and Raúl Zurita-Milla     *****************/
//*****************     Contact: emma.izquierdo@boku.ac.at,r.zurita-milla@utwente.nl   *****************/
//******************************************************************************************************/
//******************************************************************************************************/
//*****************                       Institute of Geomatics                       *****************/
//*****************        University of Natural Resources and Life Sciences (BOKU)    *****************/
//*****************             Peter Jordan Strasse 82, 1190 Vienna, Austria          *****************/
//******************************************************************************************************/
//******************************************************************************************************/
//*****************    ITC -- Faculty of Geo-information Science & Earth Observation   *****************/
//*****************               Dept of Geoinformation Processing (GIP)              *****************/
//*****************                         University of Twente                       *****************/
//*****************         Hengelosestraat 99, 7500 AA Enschede, The Netherlands      *****************/
//******************************************************************************************************/
//******************************************************************************************************/

//******************************************************************************************************/
//*****************      Acknowledgments to I.Garcia-Martí, D. Romano and R. Munde     *****************/
//******************************************************************************************************/

//******************************************************************************************************/
//*****************              Spring Index Model over Europe Script v5.0            *****************/
//******************************************************************************************************/

//If you use the software, please cite this paper: E. Izquierdo-Verdiguier, R. Zurita-Milla, T. R. Ault,
M. D. Schwartz; "Development and analysis of spring plant phenology products: 36 years of 1-km grids over
the conterminous US", Agricultural and Forest Meteorology, Vol. 262, pp. 34-41, 2018.

// Copyright (c) 2022  Emma Izquierdo-Verdiguier and Raúl Zurita-Milla

"""

import ee
import time
import numpy as np
from six_functions import timeStart
from six_functions import daylength_func
from six_functions import thr_temperature
from six_functions import gdh_bloom_func
from six_functions import predBloom
from six_functions import LinRegressBloom

ee.Initialize()

user = 'users/Emma/'
years = list(np.linspace(1980, 2021, num=42))
area = 'conus'

if area == 'europe':
    data = 'E_Obs'
    Leaf_folder = 'SIx_products/LeafEuropev3'
    folder = 'SIx_products/BloomEuropev3'

    bandmaxT = 1
    bandminT = 2

elif area == 'conus':
    data = 'NASA/ORNL/DAYMET_V4'
    Leaf_folder = 'SIx_products/LeafDaymetv4'
    folder = 'SIx_products/BloomDaymetv4'

    bandmaxT = 4
    bandminT = 5

root = user + Leaf_folder

startdate = 1
enddate = 300
thr_max = enddate + 5
reg = ee.Geometry.Polygon([[[-10.5833, 71.2583], [-10.5833, 35.99], [44.816, 35.99], [44.816, 71.2583]]])

for yr in years:
    yr = int(yr)
    print(yr)

    # *******PART 1--- Selection the daily temperature and length day ImageCollection*******/
    doy_filter = ee.Filter.calendarRange(startdate, enddate, 'day_of_year')
    if area == 'europe':
        collection = ee.ImageCollection(user + data + '/' + str(yr))
        collection = collection.map(timeStart)
        collection = collection.sort('system:time_start')
        sub_collection = collection.filter(doy_filter)
        sub_collection = daylength_func(sub_collection, bandmaxT)

    elif area == 'conus':
        date1 = str(yr) + '-01-01'
        date2 = str(yr) + '-09-30'
        collection = ee.ImageCollection(data).filterDate(date1, date2)
        sub_collection = collection.filter(doy_filter)

    crs = collection.first().projection()
    scl = crs.nominalScale().getInfo()

    join = ee.Join.saveAll(matchesKey='match', ordering='system:time_start')
    difference = 24 * 3600 * 1000
    filter1 = ee.Filter.maxDifference(difference, 'system:time_start', None, 'system:time_start')
    filter2 = ee.Filter.greaterThanOrEquals('system:time_start', None, 'system:time_start')
    filter = ee.Filter.And(filter1, filter2)

    sub_collection = ee.ImageCollection(join.apply(sub_collection, sub_collection, filter))
    sub_collection = thr_temperature(sub_collection, bandmaxT, bandminT, area)
    # *********************************END OF PART 1*****************************************/

    # **************PART 2--- Mapping the GDH function to the ImageCollection****************/
    leaf_yr = ee.Image(root + '/' + str(yr)).select(['lilac', 'red', 'zabeli'])\
        .reproject(crs, None, scl)
    gdh_col = gdh_bloom_func(sub_collection, leaf_yr)
    gdh_col = ee.ImageCollection(join.apply(gdh_col, gdh_col, filter2))
    # *********************************END OF PART 2*****************************************/

    # *****************************PART 3--- CALCULATING PREDICTORS**************************/
    predictors = predBloom(gdh_col, leaf_yr)
    # *********************************END OF PART 3*****************************************/

    # ***************PART 4 --- Calculate the predictors and the Leaf DOY********************/
    ones = LinRegressBloom(predictors, thr_max).min()
    bloom = ones.where(ones.eq(thr_max), 0)
    bloom = bloom.add(leaf_yr)

    num = bloom.select(0).neq(0).add(bloom.select(1).neq(0)).add(bloom.select(2).neq(0))

    Final_Bloom = bloom.toFloat().addBands(((bloom.select(0).add(bloom.select(1)).add(bloom.select(2)))
                                            .divide(num)).rename('bloom').round().toFloat())
    # *********************************END OF PART 4*****************************************/

    # ************************PART 5 --- Export to Assets folder*****************************/
    imageAsset = user + folder + '/' + str(yr)
    task = ee.batch.Export.image.toAsset(image=Final_Bloom, description=str(yr),
                                         assetId=imageAsset, region=reg,
                                         scale=scl, maxPixels=1.0E13,
                                         crs='EPSG:4326')

    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.', task.status())
    # *********************************END OF PART 5*****************************************/
