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
//*****************              Spring Index Model over Europe Script v6.0            *****************/
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
from six_functions import gdh_leaf_func
from six_functions import predLeaf
from six_functions import cumsumfunct_leaf
from six_functions import LinRegressLeaf

ee.Initialize()

user = 'users/Emma/'
area = 'conus'

if area == 'europe':
    years = list(np.linspace(1950, 2020, num=71))
    data = 'E_Obs'
    folder = 'SIx_products/LeafEuropev3'

    bandmaxT = 1
    bandminT = 2

elif area == 'conus':
    years = list(np.linspace(1980, 2022, num=43))
    data = 'NASA/ORNL/DAYMET_V4'
    folder = 'SIx_products/LeafDaymetv4'

    bandmaxT = 4
    bandminT = 5

startdate = 1
enddate = 300
thr_max = enddate + 5

if area == 'europe':
    reg = ee.Geometry.Polygon([[[-10.5833, 71.2583], [-10.5833, 35.99], [44.816, 35.99], [44.816, 71.2583]]])

elif area == 'conus':
    reg = ee.Geometry.Polygon([[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]])

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
    gdh_col = sub_collection.map(gdh_leaf_func)

    difference = 7 * 24 * 3600 * 1000
    filter1b = ee.Filter.maxDifference(difference, 'system:time_start', None, 'system:time_start')
    filterb = ee.Filter.And(filter1b, filter2)
    gdh_col = ee.ImageCollection(join.apply(gdh_col, gdh_col, filterb))
    # *********************************END OF PART 2*****************************************/

    # *****************************PART 3--- CALCULATING PREDICTORS**************************/
    predictors1 = gdh_col.map(predLeaf)
    predictors = ee.ImageCollection(join.apply(predictors1, predictors1, filter2))\
        .map(cumsumfunct_leaf)
    # *********************************END OF PART 3*****************************************/

    # ***************PART 4 --- Calculate the predictors and the Leaf DOY********************/
    ones = LinRegressLeaf(predictors, thr_max).min()
    leaf = ones.where(ones.eq(thr_max), 0)

    num = leaf.select(0).neq(0).add(leaf.select(1).neq(0)).add(leaf.select(2).neq(0))

    Final_Leaf = leaf.toFloat().addBands(((leaf.select(0).add(leaf.select(1)).add(leaf.select(2)))
                                          .divide(num)).rename('leaf').round().toFloat())
    # *********************************END OF PART 4*****************************************/

    # ************************PART 5 --- Export to Assets folder*****************************/
    imageAsset = user + folder + '/' + str(yr)
    task = ee.batch.Export.image.toAsset(image=Final_Leaf, description=str(yr), assetId=imageAsset,
                                         region=reg, scale=scl, maxPixels=1.0E13)

    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.', task.status())
    # *********************************END OF PART 5*****************************************/
