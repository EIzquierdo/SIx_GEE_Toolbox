# -*- coding: utf-8 -*-
"""
Created on Thur Feb 25 12:22:57 2016

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
import datetime
import math
import time

ee.Initialize()

def defcoll(im):
    date = ee.Date(im.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)
    ind = ee.Number(ee.Algorithms.If(I.gt(startdate), I.subtract(1), startdate))
    tminband1 = ee.Image(collection.select(5).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
                         .first())
    tmaxband1 = ee.Image(collection.select(4).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
                         .first())

    tminband = im.select(5).where(im.select(5).gt(tmaxband1), tmaxband1)
    tmaxband = im.select(4).where(im.select(4).lt(tminband1), tminband1)

    return im.select(0).addBands(tmaxband).addBands(tminband).copyProperties(im, ['system:index', 'system:time_start'])

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
    acgdh = list_collection.sum().add(acgdh_prev_yr)

    doy = ee.Image(I).subtract(leaf_yr)
    doy = doy.where(doy.lte(ee.Image(0)), 0).floor()
    return acgdh.addBands(doy).set({"system:time_start": sys_time})


# #*************************************** LINEAR COMBINATION *******************************************/
def LinRegress(im):
    regression = im.expression('b(3)*(-23.934)+b(0)*(0.116)>(999.5)')
    regression2 = im.expression('b(4)*(-24.825)+b(1)*(0.127)>(999.5)')
    regression3 = im.expression('b(5)*(-11.368)+b(2)*(0.096)>(999.5)')
    # Regression can be equal to zero or there is other possibility: regression eq 1 and mds0 equal 0. The last case
    # has not changed the value to thr_max
    doy_im = regression.where(regression.eq(0), thr_max)
    doy_im2 = regression2.where(regression2.eq(0), thr_max)
    doy_im3 = regression3.where(regression3.eq(0), thr_max)

    doy_im = doy_im.where(regression.eq(1), im.select(3))
    doy_im2 = doy_im2.where(regression2.eq(1), im.select(4))
    doy_im3 = doy_im3.where(regression3.eq(1), im.select(5))

    return doy_im.addBands(doy_im2).addBands(doy_im3).copyProperties(im, ['system:time_start'])


# Define constants
startdate = 126
enddate = 250
thr_max = enddate + 5
scl = 4638.23937
folder = 'BloomDaymet2'
reg = [[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]]

Image11 = [ee.Image('users/Emma/puentea/aGDH1980'), ee.Image('users/Emma/puentea/aGDH1981'),
    ee.Image('users/Emma/puentea/aGDH1982'), ee.Image('users/Emma/puentea/aGDH1983'),
    ee.Image('users/Emma/puentea/aGDH1984'), ee.Image('users/Emma/puentea/aGDH1985'),
    ee.Image('users/Emma/puentea/aGDH1986'), ee.Image('users/Emma/puentea/aGDH1987'),
    ee.Image('users/Emma/puentea/aGDH1988'), ee.Image('users/Emma/puentea/aGDH1989'),
    ee.Image('users/Emma/puentea/aGDH1990'), ee.Image('users/Emma/puentea/aGDH1991'),
    ee.Image('users/Emma/puentea/aGDH1992'), ee.Image('users/Emma/puentea/aGDH1993'),
    ee.Image('users/Emma/puentea/aGDH1994'), ee.Image('users/Emma/puentea/aGDH1995'),
    ee.Image('users/Emma/puentea/aGDH1996'), ee.Image('users/Emma/puentea/aGDH1997'),
    ee.Image('users/Emma/puentea/aGDH1998'), ee.Image('users/Emma/puentea/aGDH1999'),
    ee.Image('users/Emma/puentea/aGDH2000'), ee.Image('users/Emma/puentea/aGDH2001'),
    ee.Image('users/Emma/puentea/aGDH2002'), ee.Image('users/Emma/puentea/aGDH2003'),
    ee.Image('users/Emma/puentea/aGDH2004'), ee.Image('users/Emma/puentea/aGDH2005'),
    ee.Image('users/Emma/puentea/aGDH2006'), ee.Image('users/Emma/puentea/aGDH2007'),
    ee.Image('users/Emma/puentea/aGDH2008'), ee.Image('users/Emma/puentea/aGDH2009'),
    ee.Image('users/Emma/puentea/aGDH2010'), ee.Image('users/Emma/puentea/aGDH2011'),
    ee.Image('users/Emma/puentea/aGDH2012'), ee.Image('users/Emma/puentea/aGDH2013'),
    ee.Image('users/Emma/puentea/aGDH2014'), ee.Image('users/Emma/puentea/aGDH2015')]

Image14 = [ee.Image('users/Emma/puentea4km/aGDH1980'), ee.Image('users/Emma/puentea4km/aGDH1981'),
    ee.Image('users/Emma/puentea4km/aGDH1982'), ee.Image('users/Emma/puentea4km/aGDH1983'),
    ee.Image('users/Emma/puentea4km/aGDH1984'), ee.Image('users/Emma/puentea4km/aGDH1985'),
    ee.Image('users/Emma/puentea4km/aGDH1986'), ee.Image('users/Emma/puentea4km/aGDH1987'),
    ee.Image('users/Emma/puentea4km/aGDH1988'), ee.Image('users/Emma/puentea4km/aGDH1989'),
    ee.Image('users/Emma/puentea4km/aGDH1990'), ee.Image('users/Emma/puentea4km/aGDH1991'),
    ee.Image('users/Emma/puentea4km/aGDH1992'), ee.Image('users/Emma/puentea4km/aGDH1993'),
    ee.Image('users/Emma/puentea4km/aGDH1994'), ee.Image('users/Emma/puentea4km/aGDH1995'),
    ee.Image('users/Emma/puentea4km/aGDH1996'), ee.Image('users/Emma/puentea4km/aGDH1997'),
    ee.Image('users/Emma/puentea4km/aGDH1998'), ee.Image('users/Emma/puentea4km/aGDH1999'),
    ee.Image('users/Emma/puentea4km/aGDH2000'), ee.Image('users/Emma/puentea4km/aGDH2001'),
    ee.Image('users/Emma/puentea4km/aGDH2002'), ee.Image('users/Emma/puentea4km/aGDH2003'),
    ee.Image('users/Emma/puentea4km/aGDH2004'), ee.Image('users/Emma/puentea4km/aGDH2005'),
    ee.Image('users/Emma/puentea4km/aGDH2006'), ee.Image('users/Emma/puentea4km/aGDH2007'),
    ee.Image('users/Emma/puentea4km/aGDH2008'), ee.Image('users/Emma/puentea4km/aGDH2009'),
    ee.Image('users/Emma/puentea4km/aGDH2010'), ee.Image('users/Emma/puentea4km/aGDH2011'),
    ee.Image('users/Emma/puentea4km/aGDH2012'), ee.Image('users/Emma/puentea4km/aGDH2013'),
    ee.Image('users/Emma/puentea4km/aGDH2014'), ee.Image('users/Emma/puentea4km/aGDH2015')]

Image21 = [ee.Image('users/Emma/LeafDaymet/1980'), ee.Image('users/Emma/LeafDaymet/1981'),
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

Image24 = [ee.Image('users/Emma/LeafDaymet4km/1980'), ee.Image('users/Emma/LeafDaymet4km/1981'),
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

acgdh_prev = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image14, Image11))
leaf = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image24, Image21))

year = range(1980, 2016)

for m in range(30, 36):
    yr = year[m]
    print(yr)

    date1 = str(yr) + ('-01-01')

    date2 = str(yr) + ('-09-30')

    # *******PART 1--- Selection the daymet image collection********************/
    collection = ee.ImageCollection('NASA/ORNL/DAYMET').filterDate(date1, date2)
    doy_filter = ee.Filter.calendarRange(startdate, enddate, 'day_of_year')
    collection = collection.filter(doy_filter)
    collection = collection.map(defcoll)

    scl_d = ee.Image(collection.first()).projection().nominalScale()

    crs = ee.Image(collection.first()).projection()
    # ****************************END OF PART 1**********************************/

    leaf_yr = ee.Image(ee.List(leaf).get(m)).reproject(crs, None, scl_d)

    # ***********PART 2--- Mapping the gdh function to the collection**********/
    gdh_col = collection.map(GDH)
    # ****************************END OF PART 2**********************************/

    # *********************************PART 3--- CALCULATING PREDICTORS********************************/
    acgdh_prev_yr = ee.Image(ee.List(acgdh_prev).get(m)).reproject(crs, None, scl_d)
    predictors = ee.ImageCollection(join.apply(gdh_col, gdh_col, filter1)).map(cumsumfunct)
    # #****************************END OF PART 3**********************************/

    # #**********PART 4 --- linear regression to the predictors and filter values higher than 1000***/
    ones = predictors.map(LinRegress).min()
    bloom = ones.where(ones.eq(thr_max), 0)

    yr1 = yr * 100
    task = ee.batch.Export.image(bloom, str(yr1), {'maxPixels': 9999999999, 'scale': scl,
                                                           'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()