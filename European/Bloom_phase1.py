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
import math
import time

ee.Initialize()

user = 'users/Emma/'
years = [2003, 2004, 2005, 2006]
# data = 'users/Emma/E_Obs25km/'   # 'NASA/ORNL/DAYMET_V3'   'IDAHO_EPSCOR/GRIDMET'  'IDAHO_EPSCOR/MACAv2_METDATA'
scl = 1000  # 1000  4638.23937 27829.87269831839

Leaf_folder = 'LeafEuropean'
folder_puentea = 'puenteaEurope'
folder = 'BloomEuropean_1'

bandmaxT = 1
bandminT = 2

root = user + Leaf_folder

# #************************************** ADDING syste:time_start property ******************************************/


def timeStart(img):
    I = ee.String(img.id().split('_').get(1))
    I = ee.Number.parse(I)
    const = 24 * 60 * 60 * 1000
    sys_time = ee.Number(946684800000).add(ee.Number(const).multiply(I.subtract(ee.Number(1))))
    return img.set({"system:time_start": sys_time})


# #*************************************** ADDING day light length BAND *******************************************/

def calc_daylen(img):
    image = ee.Image(img.select(bandmaxT).reduce(ee.Reducer.sum()))
    LonLat = ee.Image.pixelLonLat()
    Latitude = LonLat.select('latitude').And(image)
    latitude = Latitude.where(Latitude.eq(1), LonLat.select('latitude'))

    CDAY = ee.List(
        [307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328,
         329, 330, 331,
         332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353,
         354, 355, 356,
         357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
         18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
         43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
         68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92,
         93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
         114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133,
         134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153,
         154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173,
         174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193,
         194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213,
         214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233,
         234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255,
         256, 257, 258,
         259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280,
         281, 282, 283,
         284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305,
         306])

    date = ee.Date(img.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year'))

    #  //CALCULATE SOLAR VALUES
    cosine = ((ee.Image(0.0172).multiply(ee.Image(ee.Number(CDAY.get(ee.Number(I)))))).subtract(ee.Image(1.95))).cos()
    tangent = (latitude.multiply(ee.Image(math.pi)).divide(180)).tan()
    DLL1 = ee.Image(12.14).add(ee.Image(3.34).multiply(tangent).multiply(cosine))
    DLL2 = ee.Image(12.25).add(
        (ee.Image(1.6164).add(ee.Image(1.7643).multiply(tangent.pow(ee.Image(2))))).multiply(cosine))
    DLL = ee.Image(ee.Algorithms.If(latitude.lt(ee.Image(40)), DLL1, DLL2))

    #  //SET DAYLENGTH TO 1 IF LESS 1 or to 23 if more than 23 (ACCOUNTS FOR HIGH LATITUDE LOCATIONS)
    DLL = DLL.where(DLL.lt(ee.Image(1)), 1)
    DLL = DLL.where(DLL.gt(ee.Image(23)), 23)
    DLL = DLL.select(['constant'], ['dayl']).float()
    return DLL.addBands(img).copyProperties(img, ['system:index', 'system:time_start'])


def defcoll(im):
    date = ee.Date(im.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)
    ind = ee.Number(ee.Algorithms.If(I.gt(1), I.subtract(1), 1))
    tminband1 = ee.Image(
        sub_collection.select(bandminT).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
        .first())
    tmaxband1 = ee.Image(
        sub_collection.select(bandmaxT).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
        .first())

    tminband = im.select(bandminT).where(im.select(bandminT).gt(tmaxband1), tmaxband1)

    tmaxband = im.select(bandmaxT).where(im.select(bandmaxT).lt(tminband1), tminband1)

    leng = ee.Image(im.select(0))

    return leng.addBands(tmaxband).addBands(tminband).copyProperties(im, ['system:index', 'system:time_start'])


# *************************************** GROWING DEGREE HOUR*******************************************/
def GDH(im):
    tminband = im.select(2)  # .expression('(b(2) *1.8) + 32')
    temp_diff = im.select(1).subtract(tminband)  # .expression('(b(1) * 1.8) + 32')

    # convert the daylength-convert from second to hours
    daylen = im.expression('b(0)/3600')
    ideal_dl = daylen.floor()

    bs_temp = ee.Image(31)
    t = tminband.subtract(bs_temp)
    t = t.where(t.lt(0), 0)

    constant = ee.Image(math.pi).divide(daylen.add(ee.Image(4)))
    sunset = (temp_diff.multiply((constant.multiply(daylen)).sin())).add(tminband)

    constant2 = sunset.subtract(tminband)
    constant3 = (ee.Image(24).subtract(daylen)).log()

    # *************Calculate of modeling hourly temperature for each image*********************/
    for i in range(2, 25):
        a = ideal_dl.add(ee.Image(1))
        b = ee.Image(i).subtract(a)
        log = b.where(b.gt(ee.Image(0)), b.log())

        eq1 = temp_diff.multiply(constant.multiply(ee.Image(i - 1)).sin()).add(tminband)
        eq2 = sunset.subtract(constant2.divide(constant3).multiply(log))
        temp = eq2.where(ee.Image(ee.Number(i)).lte(ideal_dl.add(ee.Image(1))), eq1)

        temp1 = temp.subtract(bs_temp)

        temp1 = temp1.where(temp1.lt(ee.Image(0)), 0)
        t = t.addBands(temp1)

    # growing degree hours  per day GDH
    gdh = t.reduce(ee.Reducer.sum())
    sys_time = im.get("system:time_start")
    I = ee.Number(ee.Date(sys_time).getRelative('day', 'year')).add(1)
    gdh1 = gdh.where(ee.Image(I).lt(leaf_yr.select(0)), 0)
    gdh2 = gdh.where(ee.Image(I).lt(leaf_yr.select(1)), 0)
    gdh3 = gdh.where(ee.Image(I).lt(leaf_yr.select(2)), 0)
    return gdh1.addBands(gdh2).addBands(gdh3).set({'system:time_start': sys_time})


join = ee.Join.saveAll(matchesKey='match', ordering='system:time_start')
filter1 = ee.Filter.greaterThanOrEquals(leftField='system:time_start', rightField='system:time_start')


# #*************************************** CUMULATIVE FUNCTION *******************************************/
def cumsumfunct(img):
    sys_time = img.get('system:time_start')
    I = ee.Number(ee.Date(sys_time).getRelative('day', 'year')).add(1)
    list_collection = ee.ImageCollection.fromImages(img.get('match'))
    acgdh = list_collection.sum()

    doy = ee.Image(I).subtract(leaf_yr)
    doy = doy.where(doy.lte(ee.Image(0)), 0).floor()
    return acgdh.addBands(doy).set({"system:time_start": sys_time})


# #*************************************** LINEAR COMBINATION *******************************************/
def LinRegress(im):
    regression = im.expression('b(3)*(-23.934)+b(0)*(0.116)>(999.5)')
    regression2 = im.expression('b(4)*(-24.825)+b(1)*(0.127)>(999.5)')
    regression3 = im.expression('b(5)*(-11.368)+b(2)*(0.096)>(999.5)')
    # Regression can be equal to zero or there is other possibility: regression eq 1 and mds0 equal 0 (Bloom day ==Leaf
    # day). The last case has not changed the value to thr_max
    doy_im = regression.where(regression.eq(0), thr_max)
    doy_im2 = regression2.where(regression2.eq(0), thr_max)
    doy_im3 = regression3.where(regression3.eq(0), thr_max)

    doy_im = doy_im.where(doy_im.eq(1), im.select(3))
    doy_im2 = doy_im2.where(doy_im2.eq(1), im.select(4))
    doy_im3 = doy_im3.where(doy_im3.eq(1), im.select(5))

    return doy_im.addBands(doy_im2).addBands(doy_im3).copyProperties(im, ['system:time_start'])


# Define constants
startdate = 1
enddate = 125
thr_max = enddate + 5
reg = [[[-10.5833, 71.2583], [-10.5833, 35.99], [44.816, 35.99], [44.816, 71.2583]]]

Image1 = []
for yr in years:
    Image1.append(ee.Image(root + '/' + str(yr)))

leaf = ee.List(Image1)

for m in range(0, len(years)):
    yr = years[m]
    print yr

    # *******PART 1--- Selection the daymet image collection********************/
    collection = ee.ImageCollection('users/Emma/E_Obs/' + str(yr))

    scl_d = ee.Image(collection.first()).projection().nominalScale()
    crs = ee.Image(collection.first()).projection()

    collection = collection.map(timeStart)
    collection = collection.sort('system:time_start')

    doy_filter = ee.Filter.calendarRange(startdate, enddate, 'day_of_year')
    sub_collection = collection.filter(doy_filter)

    sub_collection = sub_collection.map(calc_daylen)

    sub_collection = sub_collection.map(defcoll)
    # ****************************END OF PART 1**********************************/

    leaf_yr = ee.Image(ee.List(leaf).get(m)).reproject(crs, None, scl_d)

    # ***********PART 2--- Mapping the gdh function to the collection**********/
    gdh_col = sub_collection.map(GDH)
    # ****************************END OF PART 2**********************************/

    # *********************************PART 3--- CALCULATING PREDICTORS********************************/
    predictors = ee.ImageCollection(join.apply(gdh_col, gdh_col, filter1)).map(cumsumfunct)
    agdh = ee.Image(predictors.filter(ee.Filter.calendarRange(enddate, enddate, 'day_of_year')).first()).select(0, 1, 2)

    imageAsset = user + folder_puentea + '/aGDH' + str(yr)
    task = ee.batch.Export.image.toAsset(image=agdh, description='AGDH_' + str(yr),
                                         assetId=imageAsset,
                                         region=reg, scale=scl, maxPixels=9999999999)
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()
    # #****************************END OF PART 3**********************************/

    # #**********PART 4 --- linear regression to the predictors and filter values higher than 1000***/
    ones = predictors.map(LinRegress).min()
    bloom = ones.where(ones.eq(thr_max), 0)

    imageAsset = user + folder + '/' + str(yr)
    task = ee.batch.Export.image.toAsset(image=bloom, description=str(yr),
                                         assetId=imageAsset, region=reg,
                                         scale=scl, maxPixels=9999999999)

    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()
