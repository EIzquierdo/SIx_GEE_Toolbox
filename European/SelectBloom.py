# -*- coding: utf-8 -*-
"""

********************************************************************************************************/
//*****************       Authors: Emma Izquierdo-Verdiguier and Raúl Zurita-Milla     *****************/
//*****************     Contact: emma.izquierdo@boku.ac.at,r.zurita-milla@utwente.nl   *****************/
//******************************************************************************************************/
//******************************************************************************************************/
//*****************          Surveying, Remote Sensing &  Land Information (IVFL)      *****************/
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
//*****************              Spring Index Model over Europe Script v1.0            *****************/
//******************************************************************************************************/

//If you use the software, please cite this paper: E. Izquierdo-Verdiguier, R. Zurita-Milla, T. R. Ault,
M. D. Schwartz; "Development and analysis of spring plant phenology products: 36 years of 1-km grids over
the conterminous US", Agricultural and Forest Meteorology, Vol. 262, pp. 34-41, 2018.

// Copyright (c) 2019  Emma Izquierdo-Verdiguier and Raúl Zurita-Milla

"""

import ee
import time

ee.Initialize()

user = 'users/Emma/'
years = [2003, 2004, 2005, 2006]
data = 'European'  # 'Daymetv3', 'Gidmet', 'Maca'
scl = 1000  # 1000  4638.23937  27829.87269831839

root1 = user + 'Bloom' + data + '_1/'
root2 = user + 'Bloom' + data + '_2/'
folder = 'Bloom' + data

root_leaf = user + 'Leaf' + data

reg = [[[-10.5833, 71.2583], [-10.5833, 35.99], [44.816, 35.99], [44.816, 71.2583]]]

Image11 = []
Image21 = []
leaf1 = []
for yr in years:
    leaf1.append(ee.Image(root_leaf + '/' + str(yr)))
    Image11.append(ee.Image(root1 + str(yr)))
    Image21.append(ee.Image(root2 + str(yr)))

leaf = ee.List(leaf1)
bloom = ee.List(Image11)
bloom2 = ee.List(Image21)

for m in range(0, len(years)):
    yr = years[m]
    leaf_yr = ee.Image(ee.List(leaf).get(m)).select(0, 1, 2)
    bloom_yr = ee.Image(ee.List(bloom).get(m))
    bloom_yr2 = ee.Image(ee.List(bloom2).get(m))
    Final_Bloom = bloom_yr.where(bloom_yr.eq(0), bloom_yr2).add(leaf_yr)
    Final_Bloom = Final_Bloom.addBands(((Final_Bloom.select(0).add(Final_Bloom.select(1)).add(Final_Bloom.select(2))).divide(ee.Image(3))).round())

    imageAsset = user + folder + '/' + str(yr)
    task = ee.batch.Export.image.toAsset(image=Final_Bloom, description=str(yr), assetId=imageAsset,
                                         region=reg,
                                         scale=scl, maxPixels=9999999999)
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()

    nameImage = str(yr)
    task = ee.batch.Export.image(Final_Bloom, nameImage,
                                 {'maxPixels': 9999999999, 'scale': scl, 'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()

