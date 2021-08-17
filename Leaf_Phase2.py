# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:39:20 2015

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
import math
import time

ee.Initialize()

def defcoll(im):
    date = ee.Date(im.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)
    ind = ee.Number(ee.Algorithms.If(I.gt(startdate-7), I.subtract(1), startdate-7))
    tminband1 = ee.Image(collection.select(5).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
                         .first())
    tmaxband1 = ee.Image(collection.select(4).filter(ee.Filter.calendarRange(ind.int(), ind.int(), 'day_of_year'))
                         .first())

    tminband = im.select(5).where(im.select(5).gt(tmaxband1), tmaxband1)
    tminband = ee.Image(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), tminband.reproject(crs, None, scl), tminband))

    tmaxband = im.select(4).where(im.select(4).lt(tminband1), tminband1)
    tmaxband = ee.Image(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), tmaxband.reproject(crs, None, scl), tmaxband))
    leng = ee.Image(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), im.select(0).reproject(crs, None, scl), im.select(0)))

    return leng.addBands(tmaxband).addBands(tminband).copyProperties(im, ['system:index', 'system:time_start'])

# #*************************************** GROWING DEGREE HOUR*******************************************/
def GDH(im):
    #convert temperature munimum from Celsius to Fahrenheit
    tminband = im.expression('(b(2) *1.8) + 32')
    temp_diff = im.expression('(b(1) * 1.8) + 32').subtract(tminband)

    #convert the daylength-convert from second to hours
    daylen = im.expression('b(0)/3600')
    ideal_dl = daylen.floor()

    bs_temp = ee.Image(31)
    t = tminband.subtract(bs_temp)
    t = t.where(t.lt(0),0)

    constant = ee.Image(math.pi).divide(daylen.add(ee.Image(4)))
    sunset = (temp_diff.multiply((constant.multiply(daylen)).sin())).add(tminband)

    constant2 = sunset.subtract(tminband)
    constant3 = (ee.Image(24).subtract(daylen)).log()

    # *************Calculate of modeling hourly temperature for each image*********************/
    for i in range(2,25):
         a = ideal_dl.add(ee.Image(1))
         b = ee.Image(i).subtract(a)
         log1 = b.where(b.gt(ee.Image(0)),b.log())


         eq1 = temp_diff.multiply(constant.multiply(ee.Image(i-1)).sin()).add(tminband)
         eq2 = sunset.subtract(constant2.divide(constant3).multiply(log1))
         temp = eq2.where(ee.Image(ee.Number(i)).lte(ideal_dl.add(ee.Image(1))),eq1)

         temp1 = temp.subtract(bs_temp)

         temp1 = temp1.where(temp1.lt(ee.Image(0)), 0)
         t = t.addBands(temp1)

    #growing degree hours  per day GDH
    gdh = t.reduce(ee.Reducer.sum())
    return gdh.copyProperties(im,['system:index','system:time_start'])

# #*************************************** PREDICTORS FUNCTION *******************************************/
def predLeaf(img):
    date = ee.Date(img.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)

    ind2 = ee.Number(ee.Algorithms.If(I.gte(ee.Number(startdate)), (I.subtract(ee.Number(2))).int(), 0)).int()
    im_day_int2 = gdh_col.filter(ee.Filter.calendarRange(ind2, I.int(), 'day_of_year')).sum()
    dde2 = ee.Image(ee.Algorithms.If(I.gte(ee.Number(startdate)), im_day_int2, day13))

    thr = day13.where(ee.Image(dde2).gte(ee.Image(637)), 1)

    ind7 = ee.Number(ee.Algorithms.If(I.gte(ee.Number(8)), (I.subtract(ee.Number(7))).int(), 1)).int()
    ind5 = ee.Number(ee.Algorithms.If(I.gte(ee.Number(8)), (I.subtract(ee.Number(5))).int(), 1)).int()

    im_day_int57 = gdh_col.filter(ee.Filter.calendarRange(ind7, ind5, 'day_of_year')).sum()
    dd57 = ee.Image(ee.Algorithms.If(I.gte(ee.Number(startdate)), im_day_int57, day13))

    mds0 = ee.Image(I.subtract(1)).add(day13)

    const = 24*60*60*1000
    sys_time = ee.Number(946684800000).add(ee.Number(const).multiply(I.subtract(ee.Number(1))))
    return dde2.addBands(dd57).addBands(thr).addBands(mds0).set({"system:time_start": sys_time})

join = ee.Join.saveAll(matchesKey='match', ordering='system:time_start')
filter1 = ee.Filter.greaterThanOrEquals(leftField='system:time_start', rightField='system:time_start')

# #*************************************** CUMULATIVE FUNCTION *******************************************/
def cumsumfunct(img):
    sys_time = ee.Number(img.get('system:time_start'))
    list_collection = ee.ImageCollection.fromImages(img.get('match'))
    synop = list_collection.select(2).sum()
    synop =synop.add(synopt_prev_yr)
    return synop.addBands(img).set({'system:time_start': sys_time})


# #*************************************** LINEAR COMBINATION *******************************************/
def LinRegress(im):
    regression = im.expression('b(1)*(0.201)+b(2)*(0.153)+b(0)*(13.878)+b(4)*(3.306)>(999.5)')
    regression2 = im.expression('b(2)*(0.248)+b(0)*(20.899)+b(4)*(4.266)>(999.5)')
    regression3 = im.expression('b(1)*(0.266)+b(0)*(21.433)+b(4)*(2.802)>(999.5)')
    doy_im = regression.where(regression.eq(1), im.select(4).add(ee.Image(1)))
    doy_im2 = regression2.where(regression2.eq(1), im.select(4).add(ee.Image(2)))
    doy_im3 = regression3.where(regression3.eq(1), im.select(4).add(ee.Image(1)))
    # Here doy_im cannot be zero:
    doy_im = doy_im.where(doy_im.eq(0), thr_max)
    doy_im2 = doy_im2.where(doy_im2.eq(0), thr_max)
    doy_im3 = doy_im3.where(doy_im3.eq(0), thr_max)
    return doy_im.addBands(doy_im2).addBands(doy_im3).copyProperties(im, ['system:time_start'])

# Define constants
startdate = 126
enddate = 250
thr_max = enddate+5
folder = 'LeafDaymet2'
reg = [[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]]
year = range(1980, 2016)
scl = 4638.23937


Image1 = [ee.Image('users/Emma/puentea/synop1980'), ee.Image('users/Emma/puentea/synop1981'),
ee.Image('users/Emma/puentea/synop1982'), ee.Image('users/Emma/puentea/synop1983'),
ee.Image('users/Emma/puentea/synop1984'), ee.Image('users/Emma/puentea/synop1985'),
ee.Image('users/Emma/puentea/synop1986'), ee.Image('users/Emma/puentea/synop1987'),
ee.Image('users/Emma/puentea/synop1988'), ee.Image('users/Emma/puentea/synop1989'),
ee.Image('users/Emma/puentea/synop1990'), ee.Image('users/Emma/puentea/synop1991'),
ee.Image('users/Emma/puentea/synop1992'), ee.Image('users/Emma/puentea/synop1993'),
ee.Image('users/Emma/puentea/synop1994'), ee.Image('users/Emma/puentea/synop1995'),
ee.Image('users/Emma/puentea/synop1996'), ee.Image('users/Emma/puentea/synop1997'),
ee.Image('users/Emma/puentea/synop1998'), ee.Image('users/Emma/puentea/synop1999'),
ee.Image('users/Emma/puentea/synop2000'), ee.Image('users/Emma/puentea/synop2001'),
ee.Image('users/Emma/puentea/synop2002'), ee.Image('users/Emma/puentea/synop2003'),
ee.Image('users/Emma/puentea/synop2004'), ee.Image('users/Emma/puentea/synop2005'),
ee.Image('users/Emma/puentea/synop2006'), ee.Image('users/Emma/puentea/synop2007'),
ee.Image('users/Emma/puentea/synop2008'), ee.Image('users/Emma/puentea/synop2009'),
ee.Image('users/Emma/puentea/synop2010'), ee.Image('users/Emma/puentea/synop2011'),
ee.Image('users/Emma/puentea/synop2012'), ee.Image('users/Emma/puentea/synop2013'),
ee.Image('users/Emma/puentea/synop2014'), ee.Image('users/Emma/puentea/synop2015')]


Image14 = [ee.Image('users/Emma/puentea4km/synop1980'), ee.Image('users/Emma/puentea4km/synop1981'),
ee.Image('users/Emma/puentea4km/synop1982'), ee.Image('users/Emma/puentea4km/synop1983'),
ee.Image('users/Emma/puentea4km/synop1984'), ee.Image('users/Emma/puentea4km/synop1985'),
ee.Image('users/Emma/puentea4km/synop1986'), ee.Image('users/Emma/puentea4km/synop1987'),
ee.Image('users/Emma/puentea4km/synop1988'), ee.Image('users/Emma/puentea4km/synop1989'),
ee.Image('users/Emma/puentea4km/synop1990'), ee.Image('users/Emma/puentea4km/synop1991'),
ee.Image('users/Emma/puentea4km/synop1992'), ee.Image('users/Emma/puentea4km/synop1993'),
ee.Image('users/Emma/puentea4km/synop1994'), ee.Image('users/Emma/puentea4km/synop1995'),
ee.Image('users/Emma/puentea4km/synop1996'), ee.Image('users/Emma/puentea4km/synop1997'),
ee.Image('users/Emma/puentea4km/synop1998'), ee.Image('users/Emma/puentea4km/synop1999'),
ee.Image('users/Emma/puentea4km/synop2000'), ee.Image('users/Emma/puentea4km/synop2001'),
ee.Image('users/Emma/puentea4km/synop2002'), ee.Image('users/Emma/puentea4km/synop2003'),
ee.Image('users/Emma/puentea4km/synop2004'), ee.Image('users/Emma/puentea4km/synop2005'),
ee.Image('users/Emma/puentea4km/synop2006'), ee.Image('users/Emma/puentea4km/synop2007'),
ee.Image('users/Emma/puentea4km/synop2008'), ee.Image('users/Emma/puentea4km/synop2009'),
ee.Image('users/Emma/puentea4km/synop2010'), ee.Image('users/Emma/puentea4km/synop2011'),
ee.Image('users/Emma/puentea4km/synop2012'), ee.Image('users/Emma/puentea4km/synop2013'),
ee.Image('users/Emma/puentea4km/synop2014'), ee.Image('users/Emma/puentea4km/synop2015')]

synopt_prev = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image14, Image1))

for m in range(30, 36):
    yr = year[m]
    print yr

    date1 = str(yr)+('-01-01')

    date2 = str(yr)+('-09-30')

    # *******PART 1--- Selection the daymet image collection********************/
    collection = ee.ImageCollection('NASA/ORNL/DAYMET').filterDate(date1, date2)

    scl_d = ee.Image(collection.first()).projection().nominalScale()
    crs = ee.Image(collection.first()).projection()
    doy_filter = ee.Filter.calendarRange(startdate-7, enddate, 'day_of_year')
    collection = collection.filter(doy_filter)
    collection = collection.map(defcoll)
    # ****************************END OF PART 1**********************************/

    # ***********PART 2--- Mapping the gdh function to the collection**********/
    gdh_col = collection.map(GDH)
    # ****************************END OF PART 2**********************************/

    # *********************************PART 3--- CALCULATING PREDICTORS********************************/
    im = ee.Image(gdh_col.first())
    day13 = im.expression('b(0)*0')

    predictors1 = gdh_col.map(predLeaf)
    predictors1 = predictors1.filter(ee.Filter.calendarRange(startdate, enddate, 'day_of_year'))

    synopt_prev_yr = ee.Image(ee.List(synopt_prev).get(m)).reproject(crs, None, scl_d)
    predictors = ee.ImageCollection(join.apply(predictors1, predictors1, filter1)).map(cumsumfunct)
    # ****************************END OF PART 3**********************************/

    # **********PART 4 --- linear regression to the predictors and filter values higher than 1000***/
    ones = predictors.map(LinRegress).min()
    leaf = ones.where(ones.eq(thr_max), 0)

    yr1 = yr * 100
    task = ee.batch.Export.image(leaf, str(yr1), {'maxPixels': 9999999999, 'scale': scl, 'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
             print 'Running...'
             time.sleep(1)
    print 'Done.', task.status()