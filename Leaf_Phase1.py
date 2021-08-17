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

# #*************************************** GROWING DEGREE HOUR*******************************************/
def GDH(im):
    # # convert temperature munimum from Celsius to Fahrenheit
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
         log1 = b.where(b.gt(ee.Image(0)), b.log())
         
        
         eq1 = temp_diff.multiply(constant.multiply(ee.Image(i-1)).sin()).add(tminband)
         eq2 = sunset.subtract(constant2.divide(constant3).multiply(log1))
         temp = eq2.where(ee.Image(ee.Number(i)).lte(ideal_dl.add(ee.Image(1))), eq1)
        
         temp1 = temp.subtract(bs_temp)
          
         temp1 = temp1.where(temp1.lt(ee.Image(0)), 0)
         t = t.addBands(temp1)

    #growing degree hours  per day GDH
    gdh = t.reduce(ee.Reducer.sum())
    return gdh.copyProperties(im, ['system:index','system:time_start'])

##*************************************** PREDICTORS FUNCTION *******************************************/
def predLeaf(img):
    date = ee.Date(img.get("system:time_start"))
    I = ee.Number(date.getRelative('day', 'year')).add(1)

    dde2_1 = ee.Algorithms.If(I.eq(ee.Number(1)), day1A, day2)

    ind2 = ee.Number(ee.Algorithms.If(I.gt(ee.Number(2)),(I.subtract(ee.Number(2))).int(), 1)).int()
    im_day_int2 = gdh_col.filter(ee.Filter.calendarRange(ind2, I.int(), 'day_of_year')).sum()
    dde2 = ee.Image(ee.Algorithms.If(I.gt(ee.Number(2)), im_day_int2, dde2_1))
    
    thr = day13.where(ee.Image(dde2).gte(ee.Image(637)), 1)
    
    dd57_1 = ee.Algorithms.If(I.lte(ee.Number(3)), day13, im)
    dd57_2 = ee.Algorithms.If(I.eq(ee.Number(5)), d1, dd57_1)
    dd57_3 = ee.Algorithms.If(I.eq(ee.Number(6)), day1A, dd57_2)
    dd57_4 = ee.Algorithms.If(I.eq(ee.Number(7)), day2, dd57_3)
    
    ind7 = ee.Number(ee.Algorithms.If(I.gte(ee.Number(8)), (I.subtract(ee.Number(7))).int(), 1)).int()
    ind5 = ee.Number(ee.Algorithms.If(I.gte(ee.Number(8)), (I.subtract(ee.Number(5))).int(), 1)).int()

    im_day_int57 = gdh_col.filter(ee.Filter.calendarRange(ind7, ind5, 'day_of_year')).sum()
    dd57 = ee.Image(ee.Algorithms.If(I.gte(ee.Number(8)), im_day_int57, dd57_4))
    
    mds0 = ee.Image(I.subtract(1)).add(day13)

    const = 24*60*60*1000
    sys_time = ee.Number(946684800000).add(ee.Number(const).multiply(I.subtract(ee.Number(1))))
    return dde2.addBands(dd57).addBands(thr).addBands(mds0).set({"system:time_start": sys_time})

join = ee.Join.saveAll(matchesKey='match', ordering='system:time_start')
filter1 = ee.Filter.greaterThanOrEquals(leftField='system:time_start', rightField='system:time_start')

##*************************************** CUMULATIVE FUNCTION *******************************************/
def cumsumfunct(img):
    sys_time = ee.Number(img.get('system:time_start'))
    list_collection = ee.ImageCollection.fromImages(img.get('match'))
    synop = list_collection.select(2).sum()
    return synop.addBands(img).set({'system:time_start': sys_time})


##*************************************** LINEAR COMBINATION *******************************************/
def LinRegress(im):
    regression = im.expression('b(1)*(0.201)+b(2)*(0.153)+b(0)*(13.878)+b(4)*(3.306)>(999.5)')
    regression2 = im.expression('b(2)*(0.248)+b(0)*(20.899)+b(4)*(4.266)>(999.5)')
    regression3 = im.expression('b(1)*(0.266)+b(0)*(21.433)+b(4)*(2.802)>(999.5)')
    doy_im = regression.where(regression.eq(1), im.select(4).add(ee.Image(1)))
    doy_im2 = regression2.where(regression2.eq(1), im.select(4).add(ee.Image(2)))
    doy_im3 = regression3.where(regression3.eq(1), im.select(4).add(ee.Image(1)))
    
    doy_im = doy_im.where(doy_im.eq(0), thr_max)
    doy_im2 = doy_im2.where(doy_im2.eq(0), thr_max)
    doy_im3 = doy_im3.where(doy_im3.eq(0), thr_max)
    return doy_im.addBands(doy_im2).addBands(doy_im3).copyProperties(im, ['system:time_start'])

startdate = 1
enddate = 125
thr_max = enddate + 5
folder = 'LeafDaymet1'
reg = [[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]]
years = range(1980, 2016)
scl = 1000

for yr in years:
    print yr

    date1 = str(yr) + '-01-01'

    date2 = str(yr) + '-08-31'

    # *******PART 1--- Selection the daymet image collection********************/
    collection = ee.ImageCollection('NASA/ORNL/DAYMET').filterDate(date1,date2)
    doy_filter = ee.Filter.calendarRange(startdate, enddate, 'day_of_year')
    sub_collection = collection.filter(doy_filter)
    sub_collection = sub_collection.map(defcoll)
    # ****************************END OF PART 1**********************************/

    # ***********PART 2--- Mapping the gdh function to the collection**********/
    gdh_col = sub_collection.map(GDH)
    # ****************************END OF PART 2**********************************/

    # *********************************PART 3--- CALCULATING PREDICTORS********************************/
    im = ee.Image(gdh_col.filter(ee.Filter.calendarRange(1, 1, 'day_of_year')).first())
    day1A = im.expression('b(0)*3')
    d1 = im.expression('b(0)*2')
    #
    ## DDE2 day 2 is equal to 2*GDH(1)+GDH(2):
    im1 = ee.Image(gdh_col.filter(ee.Filter.calendarRange(2, 2, 'day_of_year')).first())
    day2 = ee.Image(d1.add(im1))
    day13 = im.expression('b(0)*0')

    predictors1 = gdh_col.map(predLeaf)
    predictors = ee.ImageCollection(join.apply(predictors1, predictors1, filter1)).map(cumsumfunct)
    synopt = ee.Image(predictors.filter(ee.Filter.calendarRange(enddate, enddate, 'day_of_year')).first()).select(0)

    task = ee.batch.Export.image(synopt, 'synop' + str(yr), {'maxPixels': 9999999999, 'scale': scl, 'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
             print 'Running...'
             time.sleep(1)
    print 'Done.', task.status()
    # ****************************END OF PART 3**********************************/

    # **********PART 4 --- linear regression to the predictors and filter values higher than 1000***/
    ones = predictors.map(LinRegress).min()
    leaf = ones.where(ones.eq(thr_max), 0)

    yr1 = yr * 10
    task = ee.batch.Export.image(leaf, str(yr1), {'maxPixels': 9999999999, 'scale': scl, 'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
             print 'Running...'
             time.sleep(1)
    print 'Done.', task.status()

