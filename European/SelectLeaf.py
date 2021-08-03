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
scl = 1000 # 27829.87269831839 1000  4638.23937

root1 = user + 'Leaf' + data + '_1/'
root2 = user + 'Leaf' + data + '_2/'
folder = 'Leaf' + data

reg = ee.Geometry.Polygon([[[-10.5833, 71.2583], [-10.5833, 35.99],
                            [44.816, 35.99], [44.816, 71.2583]]])

Image11 = []
Image21 = []
for yr in years:
    Image11.append(ee.Image(root1 + str(yr)))
    Image21.append(ee.Image(root2 + str(yr)))

leaf = ee.List(Image11)
leaf2 = ee.List(Image21)

for m in range(0, len(years)):
    yr = years[m]
    leaf_yr = ee.Image(ee.List(leaf).get(m))
    leaf_yr2 = ee.Image(ee.List(leaf2).get(m))
    Final_Leaf = leaf_yr.where(leaf_yr.eq(0), leaf_yr2)
    Final_Leaf = Final_Leaf.addBands(((Final_Leaf.select(0).add(Final_Leaf.select(1)).add(Final_Leaf.select(2))).divide(ee.Image(3))).round())

    imageAsset = user + folder + '/' + str(yr)
    task = ee.batch.Export.image.toAsset(image=Final_Leaf, description=str(yr), assetId=imageAsset,
                                         region=reg,
                                         scale=scl, maxPixels=9999999999)
    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.'), task.status()

    nameImage = str(yr)
    task = ee.batch.Export.image.toDrive(Final_Leaf, nameImage,
                                         {'maxPixels': 9999999999,
                                          'driveFolder': folder,
                                          'scale': scl, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        time.sleep(1)
    print('Done.'), task.status()

