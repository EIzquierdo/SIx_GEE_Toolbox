import ee
import math

# #************************************* ADDING system:time_start property ****************************************/


def timeStart(img):
    I = ee.String(img.id().split('_').get(1))
    I = ee.Number.parse(I)
    const = 24 * 60 * 60 * 1000
    sys_time = ee.Number(946684800000).add(ee.Number(const).multiply(I.subtract(ee.Number(1))))
    return img.set({"system:time_start": sys_time})


# #*************************************** ADDING day light length BAND *******************************************/
def daylength_func(sub_collection, bandmaxT):

    def calc_daylen(img):
        image = ee.Image(img.select(bandmaxT).reduce(ee.Reducer.sum()).add(ee.Image(2.2e-16)))
        LonLat = ee.Image.pixelLonLat()
        Latitude = LonLat.select('latitude').And(image)
        latitude = Latitude.where(Latitude.eq(1), LonLat.select('latitude'))

        CDAY = ee.List(
            [307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327,
             328,
             329, 330, 331,
             332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352,
             353,
             354, 355, 356,
             357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
             17,
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
             234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254,
             255,
             256, 257, 258,
             259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279,
             280,
             281, 282, 283,
             284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304,
             305,
             306])

        date = ee.Date(img.get("system:time_start"))
        I = ee.Number(date.getRelative('day', 'year'))

        #  //CALCULATE SOLAR VALUES
        cosine = (
            (ee.Image(0.0172).multiply(ee.Image(ee.Number(CDAY.get(ee.Number(I)))))).subtract(ee.Image(1.95))).cos()
        tangent = (latitude.multiply(ee.Image(math.pi)).divide(180)).tan()
        DLL1 = ee.Image(12.14).add(ee.Image(3.34).multiply(tangent).multiply(cosine))
        DLL2 = ee.Image(12.25).add(
            (ee.Image(1.6164).add(ee.Image(1.7643).multiply(tangent.pow(ee.Image(2))))).multiply(cosine))
        DLL = DLL1.where(latitude.gt(ee.Image(40)), DLL2)

        #  //SET DAYLENGTH TO 1 IF LESS 1 or to 23 if more than 23 (ACCOUNTS FOR HIGH LATITUDE LOCATIONS)
        DLL = DLL.where(DLL.lt(ee.Image(1)), 1)
        DLL = DLL.where(DLL.gt(ee.Image(23)), 23)
        DLL = DLL.select(['constant'], ['dayl']).float()
        return DLL.addBands(img).copyProperties(img, ['system:index', 'system:time_start'])

    return sub_collection.map(calc_daylen)


def thr_temperature(sub_collection, bandmaxT, bandminT, area):

    def defcoll(im):
        prev = ee.ImageCollection.fromImages(im.get('match')).sort('system:time_start').first()
        tminband1 = ee.Image(prev.select(bandminT))
        tmaxband1 = ee.Image(prev.select(bandmaxT))

        tminband = im.select(bandminT).where(im.select(bandminT).gt(tmaxband1), tmaxband1)
        tmaxband = im.select(bandmaxT).where(im.select(bandmaxT).lt(tminband1), tminband1)
        # # convert temperature minimum from Celsius (*100) to Fahrenheit
        if area == 'europe':
            tminband = tminband.expression('(b(0) *1.8/100) + 32')
            tmaxband = tmaxband.expression('(b(0) *1.8/100) + 32')
            leng = im.select(0)

        elif area == 'conus':
            tminband = tminband.expression('(b(0) *1.8) + 32')
            tmaxband = tmaxband.expression('(b(0) *1.8) + 32')
            leng = im.expression('b(0)/3600')

        return leng.addBands(tmaxband).addBands(tminband).copyProperties(im, ['system:index', 'system:time_start'])
    return sub_collection.map(defcoll)


def gdh_leaf_func(im):

    tminband = im.select(2)
    temp_diff = im.select(1).subtract(tminband)

    # convert the daylength-convert from second to hours
    daylen = im.select(0)
    ideal_dl = daylen.floor()

    bs_temp = ee.Image(31)
    t = tminband.subtract(bs_temp)

    constant = ee.Image(math.pi).divide(daylen.add(ee.Image(4)))
    sunset = (temp_diff.multiply((constant.multiply(daylen)).sin())).add(tminband)

    constant2 = sunset.subtract(tminband)
    constant3 = (ee.Image(24).subtract(daylen)).log()

    # *************Calculate of modeling hourly temperature for each image*********************/
    for i in range(2, 25):
        a = ideal_dl.add(ee.Image(1))
        b = ee.Image(i).subtract(a)
        log1 = b.where(b.gt(ee.Image(0)), b.log())

        eq1 = temp_diff.multiply(constant.multiply(ee.Image(i - 1)).sin()).add(tminband)
        eq2 = sunset.subtract(constant2.divide(constant3).multiply(log1))
        temp = eq2.where(ee.Image(ee.Number(i)).lte(ideal_dl.add(ee.Image(1))), eq1)

        temp1 = temp.subtract(bs_temp)

        t = t.addBands(temp1)

    t = t.where(t.lt(0), 0)

    # growing degree hours  per day GDH
    gdh = t.reduce(ee.Reducer.sum())
    return gdh.copyProperties(im, ['system:index', 'system:time_start'])

# #*************************************** PREDICTORS FUNCTION *******************************************/


def predLeaf(img):
    I = ee.List(img.get('match')).size()

    col = ee.ImageCollection.fromImages(img.get('match'))
    prev = ee.Image(col.first())
    # DDE2 day 1 is equal to 3*GDH(1) and DDE2 day 2 is equal to 2*GDH(1)+GDH(2):
    dde2_1 = ee.Algorithms.If(I.eq(ee.Number(1)), img.expression('b(0)*3'),
                              prev.expression('b(0)*2').add(img.expression('b(0)')))

    date = ee.Date(img.get("system:time_start"))
    I_sub = ee.Number(date.getRelative('day', 'year')).add(1)
    ind2 = ee.Number(ee.Algorithms.If(I_sub.gt(ee.Number(2)), (I_sub.subtract(ee.Number(2))).int(), 1)).int()
    im_day_int2 = col.filter(ee.Filter.calendarRange(ind2, I_sub.int(), 'day_of_year')).sum()
    dde2 = ee.Image(ee.Algorithms.If(I.gt(ee.Number(2)), im_day_int2, dde2_1))

    thr = img.expression('b(0)*0').where(ee.Image(dde2).gte(ee.Image(637)), 1)

    dd57_1 = ee.Algorithms.If(I.lte(ee.Number(3)), img.expression('b(0)*0'), prev)
    dd57_2 = ee.Algorithms.If(I.eq(ee.Number(5)), prev.expression('b(0)*2'), dd57_1)
    dd57_3 = ee.Algorithms.If(I.eq(ee.Number(6)), prev.expression('b(0)*3'), dd57_2)
    dd57_4 = ee.Algorithms.If(I.eq(ee.Number(7)),
                              prev.expression('b(0)*2')
                              .add(ee.Image(col.filter(ee.Filter.calendarRange(2, None, 'day_of_year')).first())
                                   .expression('b(0)')), dd57_3)

    ind7 = ee.Number(ee.Algorithms.If(I.gte(ee.Number(8)), (I_sub.subtract(ee.Number(7))).int(), 1)).int()
    ind5 = ee.Number(ee.Algorithms.If(I.gte(ee.Number(8)), (I_sub.subtract(ee.Number(5))).int(), 1)).int()

    im_day_int57 = col.filter(ee.Filter.calendarRange(ind7, ind5, 'day_of_year')).sum()
    dd57 = ee.Image(ee.Algorithms.If(I.gte(ee.Number(8)), im_day_int57, dd57_4))

    mds0 = ee.Image(I_sub.subtract(1)).add(img.expression('b(0)*0'))

    return dde2.addBands(dd57).addBands(thr).addBands(mds0).rename(['DDE2', 'DD57', 'Synop', 'MDS0']) \
        .set({"system:time_start": img.get("system:time_start")})


# #*************************************** CUMULATIVE FUNCTION *******************************************/
def cumsumfunct_leaf(img):
    sys_time = ee.Number(img.get('system:time_start'))
    list_collection = ee.ImageCollection.fromImages(img.get('match'))
    synop = list_collection.select(2).reduce(ee.Reducer.sum(), 2).rename('Synop')
    return img.addBands(synop, None, True).set({'system:time_start': sys_time})


def LinRegressLeaf(predictors, thr_max):

    def LinRegress(im):
        regression = im.expression('b(0)*(0.201)+b(1)*(0.153)+b(2)*(13.878)+b(3)*(3.306)>(999.5)')
        regression2 = im.expression('b(1)*(0.248)+b(2)*(20.899)+b(3)*(4.266)>(999.5)')
        regression3 = im.expression('b(0)*(0.266)+b(2)*(21.433)+b(3)*(2.802)>(999.5)')

        doy_im = regression.where(regression.eq(1), im.select(3).add(ee.Image(1)))
        doy_im2 = regression2.where(regression2.eq(1), im.select(3).add(ee.Image(2)))
        doy_im3 = regression3.where(regression3.eq(1), im.select(3).add(ee.Image(1)))

        doy_im = doy_im.where(doy_im.eq(0), thr_max)
        doy_im2 = doy_im2.where(doy_im2.eq(0), thr_max)
        doy_im3 = doy_im3.where(doy_im3.eq(0), thr_max)
        return doy_im.addBands(doy_im2).addBands(doy_im3).rename(['lilac', 'red', 'zabeli']) \
            .copyProperties(im, ['system:time_start'])

    return predictors.map(LinRegress)


def gdh_bloom_func(sub_collection, leaf_yr):
    def GDH(im):
        tminband = im.select(2)
        temp_diff = im.select(1).subtract(tminband)

        # convert the daylength-convert from second to hours
        daylen = im.expression('b(0)')
        ideal_dl = daylen.floor()

        bs_temp = ee.Image(31)
        t = tminband.subtract(bs_temp)

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

            t = t.addBands(temp1)

        t = t.where(t.lt(0), 0)

        # growing degree hours  per day GDH
        gdh = t.reduce(ee.Reducer.sum())
        sys_time = im.get("system:time_start")
        I = ee.Number(ee.Date(sys_time).getRelative('day', 'year')).add(1)
        gdh1 = gdh.where(ee.Image(I).lt(leaf_yr.select(0)), 0)
        gdh2 = gdh.where(ee.Image(I).lt(leaf_yr.select(1)), 0)
        gdh3 = gdh.where(ee.Image(I).lt(leaf_yr.select(2)), 0)
        return gdh1.addBands(gdh2).addBands(gdh3).set({'system:time_start': sys_time})
    return sub_collection.map(GDH)


# #*************************************** CUMULATIVE FUNCTION *******************************************/
def predBloom(gdh_col, leaf_yr):

    def cumsumfunct(img):
        sys_time = img.get('system:time_start')
        I = ee.Number(ee.Date(sys_time).getRelative('day', 'year')).add(1)
        list_collection = ee.ImageCollection.fromImages(img.get('match'))
        acgdh = list_collection.sum()

        doy = ee.Image(I).subtract(leaf_yr)
        doy = doy.where(doy.lte(ee.Image(0)), 0).floor()
        return acgdh.rename(['agdh_lilac', 'agdh_red', 'agdh_zabeli'])\
            .addBands(doy.rename(['mds0_lilac', 'mds0_red', 'mds0_zabeli'])).set({"system:time_start": sys_time})

    return gdh_col.map(cumsumfunct)


# #*************************************** LINEAR COMBINATION *******************************************/
def LinRegressBloom(predictors, thr_max):

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

        return doy_im.addBands(doy_im2).addBands(doy_im3).rename(['lilac', 'red', 'zabeli']) \
            .copyProperties(im, ['system:time_start'])
    return predictors.map(LinRegress)


def lastFreeze(collection, area):

    def lastFreezeIndex(Temperature):
        date = ee.Date(Temperature.get("system:time_start"))
        I = ee.Image(ee.Number(date.getRelative('day', 'year')).add(1))
        if area == 'europe':
            Temperature = ee.Image(Temperature.expression('b(0)/100 *1.8 + 32')\
            .copyProperties(Temperature,['system:time_start']))

        elif area == 'conus':
            Temperature = ee.Image(Temperature.expression('(b(0) *1.8) + 32')\
            .copyProperties(Temperature,['system:time_start']))
        Tfreeze = Temperature.where(Temperature.lte(28), I)
        Tfreeze = Tfreeze.where(Temperature.gt(28), 0)
        return Tfreeze

    return collection.map(lastFreezeIndex)
