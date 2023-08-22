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
//*****************              Spring Index Model over CONUS Script v5.0            *****************/
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
from six_functions import lastFreeze

ee.Initialize()

user = 'users/Emma/'
years = list(np.linspace(1980, 2021, num=42))
area = 'conus'

if area == 'europe':
    data = 'E_Obs'
    last_folder = 'LastF_Europev3'
    di_sc_folder = 'DI_Europev3_sc'
    di_folder = 'DI_Europev3'
    leaf_folder = 'SIx_products/LeafEuropev3'

    bandminT = 1

elif area == 'conus':
    data = 'NASA/ORNL/DAYMET_V4'
    last_folder = 'LastF_Daymetv4'
    di_sc_folder = 'DI_Daymetv4_sc'
    di_folder = 'DI_Daymetv4'
    leaf_folder = 'SIx_products/LeafDaymetv4'

    bandminT = 5

root_lastf = user + last_folder
root_leaf = user + leaf_folder
root_di_sc = user + di_sc_folder
root_di = user + di_folder

startdate = 1
enddate = 300

if area == 'europe':
    reg = ee.Geometry.Polygon([[[-10.5833, 71.2583], [-10.5833, 35.99], [44.816, 35.99], [44.816, 71.2583]]])

elif area == 'conus':
    reg = ee.Geometry.Polygon([[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]])

DI = []
for yr in years:
    yr = int(yr)
    print(yr)

    # *******PART 1--- Selection the daymet image collection********************/
    doy_filter = ee.Filter.calendarRange(startdate, enddate, 'day_of_year')
    if area == 'europe':
        collection = ee.ImageCollection(user + data + '/' + str(yr))
        collection = collection.map(timeStart)
        collection = collection.sort('system:time_start')

    elif area == 'conus':
        date1 = str(yr) + '-01-01'
        date2 = str(yr) + '-09-30'
        collection = ee.ImageCollection(data).filterDate(date1, date2)

    crs = collection.first().projection()
    scl = crs.nominalScale().getInfo()
    sub_collection = collection.filter(doy_filter).select(bandminT)
    # ****************************END OF PART 1**********************************/

    # ********PART 2--- Mapping the last freeze function to the collection*******/
    LastFIndex = lastFreeze(collection, area).max()

    imageAsset = root_lastf + str(yr)

    task = ee.batch.Export.image.toAsset(image=LastFIndex, description=str(yr),
                                         assetId=imageAsset, region=reg, scale=scl,
                                         maxPixels=1.0E13)

    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.', task.status())
    # ****************************END OF PART 2**********************************/

    # *********************PART 3--- Calculate damage index ********************/
    Leaf = ee.Image(root_leaf + str(yr))

    di = Leaf.subtract(LastFIndex)\
        .set({'system:time_start': ee.Date.fromYMD(ee.Number.parse(Leaf.id()), 1, 1).millis()})

    imageAsset = root_di_sc + str(yr)
    task = ee.batch.Export.image.toAsset(image=di, description=str(yr), assetId=imageAsset,
                                         region=reg, scale=scl, maxPixels=1.0E13)

    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.', task.status())
     # ****************************END OF PART 3**********************************/
