# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 12:22:57 2015

@author: :************************************************************************************************
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
import math
import time

ee.Initialize()

def defcoll(im):
    crs = im.projection()
    date = ee.Date(im.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)
    ind = ee.Number(ee.Algorithms.If(I.gt(1), I.subtract(1), 1))
    tminband1 = ee.Image(sub_collection.select(5).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
                         .first())
    tmaxband1 = ee.Image(sub_collection.select(4).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
                         .first())

    tminband = im.select(5).where(im.select(5).gt(tmaxband1), tmaxband1)
    tminband = ee.Image(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), tminband.reproject(crs, None, scl), tminband))

    tmaxband = im.select(4).where(im.select(4).lt(tminband1), tminband1)
    tmaxband = ee.Image(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), tmaxband.reproject(crs, None, scl), tmaxband))
    leng = ee.Image(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), im.select(0).reproject(crs, None, scl), im.select(0)))

    return leng.addBands(tmaxband).addBands(tminband).copyProperties(im, ['system:index', 'system:time_start'])

# *************************************** GROWING DEGREE HOUR*******************************************/
def GDH(im):
    # convert temperature minimum from Celsius to Fahrenheit
    tminband = im.expression('(b(2) *1.8) + 32')
    temp_diff = im.expression('(b(1) * 1.8) + 32').subtract(tminband)

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
scl = 4638.23937
folder = 'BloomDaymet1'
reg = [[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]]

Image1 = [ee.Image('users/Emma/LeafDaymet/1980'), ee.Image('users/Emma/LeafDaymet/1981'),
        ee.Image('users/Emma/LeafDaymet/1982'), ee.Image('users/Emma/LeafDaymet/1983'),
        ee.Image('users/Emma/LeafDaymet/1984'), ee.Image('users/Emma/LeafDaymet/1985'),
        ee.Image('users/Emma/LeafDaymet/1986'), ee.Image('users/Emma/LeafDaymet/1987'),
        ee.Image('users/Emma/LeafDaymet/1988'), ee.Image('users/Emma/LeafDaymet/1989'),
        ee.Image('users/Emma/LeafDaymet/1990'), ee.Image('users/Emma/LeafDaymet/1991'),
        ee.Image('users/Emma/LeafDaymet/1992'), ee.Image('users/Emma/LeafDaymet/1993'),
        ee.Image('users/Emma/LeafDaymet/1994'), ee.Image('users/Emma/LeafDaymet/1995'),
        ee.Image('users/Emma/LeafDaymet/1996'), ee.Image('users/Emma/LeafDaymet/1997'),
        ee.Image('users/Emma/LeafDaymet/1998'), ee.Image('users/Emma/LeafDaymet/1999'),
        ee.Image('users/Emma/LeafDaymet/2000'), ee.Image('users/Emma/LeafDaymet/2001'),
        ee.Image('users/Emma/LeafDaymet/2002'), ee.Image('users/Emma/LeafDaymet/2003'),
        ee.Image('users/Emma/LeafDaymet/2004'), ee.Image('users/Emma/LeafDaymet/2005'),
        ee.Image('users/Emma/LeafDaymet/2006'), ee.Image('users/Emma/LeafDaymet/2007'),
        ee.Image('users/Emma/LeafDaymet/2008'), ee.Image('users/Emma/LeafDaymet/2009'),
        ee.Image('users/Emma/LeafDaymet/2010'), ee.Image('users/Emma/LeafDaymet/2011'),
        ee.Image('users/Emma/LeafDaymet/2012'), ee.Image('users/Emma/LeafDaymet/2013'),
        ee.Image('users/Emma/LeafDaymet/2014'), ee.Image('users/Emma/LeafDaymet/2015')]

Image2 = [ee.Image('users/Emma/LeafDaymet4km/1980'), ee.Image('users/Emma/LeafDaymet4km/1981'),
        ee.Image('users/Emma/LeafDaymet4km/1982'), ee.Image('users/Emma/LeafDaymet4km/1983'),
        ee.Image('users/Emma/LeafDaymet4km/1984'), ee.Image('users/Emma/LeafDaymet4km/1985'),
        ee.Image('users/Emma/LeafDaymet4km/1986'), ee.Image('users/Emma/LeafDaymet4km/1987'),
        ee.Image('users/Emma/LeafDaymet4km/1988'), ee.Image('users/Emma/LeafDaymet4km/1989'),
        ee.Image('users/Emma/LeafDaymet4km/1990'), ee.Image('users/Emma/LeafDaymet4km/1991'),
        ee.Image('users/Emma/LeafDaymet4km/1992'), ee.Image('users/Emma/LeafDaymet4km/1993'),
        ee.Image('users/Emma/LeafDaymet4km/1994'), ee.Image('users/Emma/LeafDaymet4km/1995'),
        ee.Image('users/Emma/LeafDaymet4km/1996'), ee.Image('users/Emma/LeafDaymet4km/1997'),
        ee.Image('users/Emma/LeafDaymet4km/1998'), ee.Image('users/Emma/LeafDaymet4km/1999'),
        ee.Image('users/Emma/LeafDaymet4km/2000'), ee.Image('users/Emma/LeafDaymet4km/2001'),
        ee.Image('users/Emma/LeafDaymet4km/2002'), ee.Image('users/Emma/LeafDaymet4km/2003'),
        ee.Image('users/Emma/LeafDaymet4km/2004'), ee.Image('users/Emma/LeafDaymet4km/2005'),
        ee.Image('users/Emma/LeafDaymet4km/2006'), ee.Image('users/Emma/LeafDaymet4km/2007'),
        ee.Image('users/Emma/LeafDaymet4km/2008'), ee.Image('users/Emma/LeafDaymet4km/2009'),
        ee.Image('users/Emma/LeafDaymet4km/2010'), ee.Image('users/Emma/LeafDaymet4km/2011'),
        ee.Image('users/Emma/LeafDaymet4km/2012'), ee.Image('users/Emma/LeafDaymet4km/2013'),
        ee.Image('users/Emma/LeafDaymet4km/2014'), ee.Image('users/Emma/LeafDaymet4km/2015')]

leaf = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image2, Image1))

year = range(1980, 2016)

for m in range(0, 36):
    yr = year[m]
    print(yr)

    date1 = str(yr) + ('-01-01')

    date2 = str(yr) + ('-08-31')

    # *******PART 1--- Selection the daymet image collection********************/
    collection = ee.ImageCollection('NASA/ORNL/DAYMET').filterDate(date1, date2)
    doy_filter = ee.Filter.calendarRange(startdate, enddate, 'day_of_year')
    sub_collection = collection.filter(doy_filter)
    sub_collection = sub_collection.map(defcoll)

    scl_d = ee.Image(sub_collection.first()).projection().nominalScale()

    crs = ee.Image(sub_collection.first()).projection()
    # ****************************END OF PART 1**********************************/

    leaf_yr = ee.Image(ee.List(leaf).get(m)).reproject(crs, None, scl_d)

    # ***********PART 2--- Mapping the gdh function to the collection**********/
    gdh_col = sub_collection.map(GDH)
    # ****************************END OF PART 2**********************************/

    # *********************************PART 3--- CALCULATING PREDICTORS********************************/
    predictors = ee.ImageCollection(join.apply(gdh_col, gdh_col, filter1)).map(cumsumfunct)
    agdh = ee.Image(predictors.filter(ee.Filter.calendarRange(enddate, enddate, 'day_of_year')).first()).select(0, 1, 2)

    task = ee.batch.Export.image(agdh, 'aGDH' + str(yr), {'maxPixels': 9999999999, 'scale': scl,
                                                          'crs': 'EPSG:4326', 'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()
    # #****************************END OF PART 3**********************************/

    # #**********PART 4 --- linear regression to the predictors and filter values higher than 1000***/
    ones = predictors.map(LinRegress).min()
    bloom = ones.where(ones.eq(thr_max), 0)

    task = ee.batch.Export.image(bloom, str(yr), {'crs': 'EPSG:4326', 'maxPixels': 9999999999, 'scale': scl,
                                                  'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()
