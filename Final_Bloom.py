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
import time

ee.Initialize()

folder = 'BloomDaymet'
reg = [[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]]
scl = 4638.23937

leaf1 = [ee.Image('users/Emma/LeafDaymet/1980'), ee.Image('users/Emma/LeafDaymet/1981'),
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

leaf4 = [ee.Image('users/Emma/LeafDaymet4km/1980'), ee.Image('users/Emma/LeafDaymet4km/1981'),
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

Image11 = [ee.Image('users/Emma/BloomDaymet1/1980'), ee.Image('users/Emma/BloomDaymet1/1981'),
           ee.Image('users/Emma/BloomDaymet1/1982'), ee.Image('users/Emma/BloomDaymet1/1983'),
           ee.Image('users/Emma/BloomDaymet1/1984'), ee.Image('users/Emma/BloomDaymet1/1985'),
           ee.Image('users/Emma/BloomDaymet1/1986'), ee.Image('users/Emma/BloomDaymet1/1987'),
           ee.Image('users/Emma/BloomDaymet1/1988'), ee.Image('users/Emma/BloomDaymet1/1989'),
           ee.Image('users/Emma/BloomDaymet1/1990'), ee.Image('users/Emma/BloomDaymet1/1991'),
           ee.Image('users/Emma/BloomDaymet1/1992'), ee.Image('users/Emma/BloomDaymet1/1993'),
           ee.Image('users/Emma/BloomDaymet1/1994'), ee.Image('users/Emma/BloomDaymet1/1995'),
           ee.Image('users/Emma/BloomDaymet1/1996'), ee.Image('users/Emma/BloomDaymet1/1997'),
           ee.Image('users/Emma/BloomDaymet1/1998'), ee.Image('users/Emma/BloomDaymet1/1999'),
           ee.Image('users/Emma/BloomDaymet1/2000'), ee.Image('users/Emma/BloomDaymet1/2001'),
           ee.Image('users/Emma/BloomDaymet1/2002'), ee.Image('users/Emma/BloomDaymet1/2003'),
           ee.Image('users/Emma/BloomDaymet1/2004'), ee.Image('users/Emma/BloomDaymet1/2005'),
           ee.Image('users/Emma/BloomDaymet1/2006'), ee.Image('users/Emma/BloomDaymet1/2007'),
           ee.Image('users/Emma/BloomDaymet1/2008'), ee.Image('users/Emma/BloomDaymet1/2009'),
           ee.Image('users/Emma/BloomDaymet1/2010'), ee.Image('users/Emma/BloomDaymet1/2011'),
           ee.Image('users/Emma/BloomDaymet1/2012'), ee.Image('users/Emma/BloomDaymet1/2013'),
           ee.Image('users/Emma/BloomDaymet1/2014'), ee.Image('users/Emma/BloomDaymet1/2015')]

Image14 = [ee.Image('users/Emma/BloomDaymet4km1/1980'), ee.Image('users/Emma/BloomDaymet4km1/1981'),
           ee.Image('users/Emma/BloomDaymet4km1/1982'), ee.Image('users/Emma/BloomDaymet4km1/1983'),
           ee.Image('users/Emma/BloomDaymet4km1/1984'), ee.Image('users/Emma/BloomDaymet4km1/1985'),
           ee.Image('users/Emma/BloomDaymet4km1/1986'), ee.Image('users/Emma/BloomDaymet4km1/1987'),
           ee.Image('users/Emma/BloomDaymet4km1/1988'), ee.Image('users/Emma/BloomDaymet4km1/1989'),
           ee.Image('users/Emma/BloomDaymet4km1/1990'), ee.Image('users/Emma/BloomDaymet4km1/1991'),
           ee.Image('users/Emma/BloomDaymet4km1/1992'), ee.Image('users/Emma/BloomDaymet4km1/1993'),
           ee.Image('users/Emma/BloomDaymet4km1/1994'), ee.Image('users/Emma/BloomDaymet4km1/1995'),
           ee.Image('users/Emma/BloomDaymet4km1/1996'), ee.Image('users/Emma/BloomDaymet4km1/1997'),
           ee.Image('users/Emma/BloomDaymet4km1/1998'), ee.Image('users/Emma/BloomDaymet4km1/1999'),
           ee.Image('users/Emma/BloomDaymet4km1/2000'), ee.Image('users/Emma/BloomDaymet4km1/2001'),
           ee.Image('users/Emma/BloomDaymet4km1/2002'), ee.Image('users/Emma/BloomDaymet4km1/2003'),
           ee.Image('users/Emma/BloomDaymet4km1/2004'), ee.Image('users/Emma/BloomDaymet4km1/2005'),
           ee.Image('users/Emma/BloomDaymet4km1/2006'), ee.Image('users/Emma/BloomDaymet4km1/2007'),
           ee.Image('users/Emma/BloomDaymet4km1/2008'), ee.Image('users/Emma/BloomDaymet4km1/2009'),
           ee.Image('users/Emma/BloomDaymet4km1/2010'), ee.Image('users/Emma/BloomDaymet4km1/2011'),
           ee.Image('users/Emma/BloomDaymet4km1/2012'), ee.Image('users/Emma/BloomDaymet4km1/2013'),
           ee.Image('users/Emma/BloomDaymet4km1/2014'), ee.Image('users/Emma/BloomDaymet4km1/2015')]

Image21 = [ee.Image('users/Emma/BloomDaymet2/1980'), ee.Image('users/Emma/BloomDaymet2/1981'),
           ee.Image('users/Emma/BloomDaymet2/1982'), ee.Image('users/Emma/BloomDaymet2/1983'),
           ee.Image('users/Emma/BloomDaymet2/1984'), ee.Image('users/Emma/BloomDaymet2/1985'),
           ee.Image('users/Emma/BloomDaymet2/1986'), ee.Image('users/Emma/BloomDaymet2/1987'),
           ee.Image('users/Emma/BloomDaymet2/1988'), ee.Image('users/Emma/BloomDaymet2/1989'),
           ee.Image('users/Emma/BloomDaymet2/1990'), ee.Image('users/Emma/BloomDaymet2/1991'),
           ee.Image('users/Emma/BloomDaymet2/1992'), ee.Image('users/Emma/BloomDaymet2/1993'),
           ee.Image('users/Emma/BloomDaymet2/1994'), ee.Image('users/Emma/BloomDaymet2/1995'),
           ee.Image('users/Emma/BloomDaymet2/1996'), ee.Image('users/Emma/BloomDaymet2/1997'),
           ee.Image('users/Emma/BloomDaymet2/1998'), ee.Image('users/Emma/BloomDaymet2/1999'),
           ee.Image('users/Emma/BloomDaymet2/2000'), ee.Image('users/Emma/BloomDaymet2/2001'),
           ee.Image('users/Emma/BloomDaymet2/2002'), ee.Image('users/Emma/BloomDaymet2/2003'),
           ee.Image('users/Emma/BloomDaymet2/2004'), ee.Image('users/Emma/BloomDaymet2/2005'),
           ee.Image('users/Emma/BloomDaymet2/2006'), ee.Image('users/Emma/BloomDaymet2/2007'),
           ee.Image('users/Emma/BloomDaymet2/2008'), ee.Image('users/Emma/BloomDaymet2/2009'),
           ee.Image('users/Emma/BloomDaymet2/2010'), ee.Image('users/Emma/BloomDaymet2/2011'),
           ee.Image('users/Emma/BloomDaymet2/2012'), ee.Image('users/Emma/BloomDaymet2/2013'),
           ee.Image('users/Emma/BloomDaymet2/2014'), ee.Image('users/Emma/BloomDaymet2/2015')]

Image24 = [ee.Image('users/Emma/BloomDaymet4km2/1980'), ee.Image('users/Emma/BloomDaymet4km2/1981'),
           ee.Image('users/Emma/BloomDaymet4km2/1982'), ee.Image('users/Emma/BloomDaymet4km2/1983'),
           ee.Image('users/Emma/BloomDaymet4km2/1984'), ee.Image('users/Emma/BloomDaymet4km2/1985'),
           ee.Image('users/Emma/BloomDaymet4km2/1986'), ee.Image('users/Emma/BloomDaymet4km2/1987'),
           ee.Image('users/Emma/BloomDaymet4km2/1988'), ee.Image('users/Emma/BloomDaymet4km2/1989'),
           ee.Image('users/Emma/BloomDaymet4km2/1990'), ee.Image('users/Emma/BloomDaymet4km2/1991'),
           ee.Image('users/Emma/BloomDaymet4km2/1992'), ee.Image('users/Emma/BloomDaymet4km2/1993'),
           ee.Image('users/Emma/BloomDaymet4km2/1994'), ee.Image('users/Emma/BloomDaymet4km2/1995'),
           ee.Image('users/Emma/BloomDaymet4km2/1996'), ee.Image('users/Emma/BloomDaymet4km2/1997'),
           ee.Image('users/Emma/BloomDaymet4km2/1998'), ee.Image('users/Emma/BloomDaymet4km2/1999'),
           ee.Image('users/Emma/BloomDaymet4km2/2000'), ee.Image('users/Emma/BloomDaymet4km2/2001'),
           ee.Image('users/Emma/BloomDaymet4km2/2002'), ee.Image('users/Emma/BloomDaymet4km2/2003'),
           ee.Image('users/Emma/BloomDaymet4km2/2004'), ee.Image('users/Emma/BloomDaymet4km2/2005'),
           ee.Image('users/Emma/BloomDaymet4km2/2006'), ee.Image('users/Emma/BloomDaymet4km2/2007'),
           ee.Image('users/Emma/BloomDaymet4km2/2008'), ee.Image('users/Emma/BloomDaymet4km2/2009'),
           ee.Image('users/Emma/BloomDaymet4km2/2010'), ee.Image('users/Emma/BloomDaymet4km2/2011'),
           ee.Image('users/Emma/BloomDaymet4km2/2012'), ee.Image('users/Emma/BloomDaymet4km2/2013'),
           ee.Image('users/Emma/BloomDaymet4km2/2014'), ee.Image('users/Emma/BloomDaymet4km2/2015')]

leaf = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), leaf4, leaf1))
bloom = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image14, Image11))
bloom2 = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image24, Image21))

year = range(1980, 2016)

for m in range(30, 36):
    yr = year[m]
    leaf_yr = ee.Image(ee.List(leaf).get(m)).select(0, 1, 2)
    bloom_yr = ee.Image(ee.List(bloom).get(m))
    bloom_yr2 = ee.Image(ee.List(bloom2).get(m))
    Final_Bloom = bloom_yr.where(bloom_yr.eq(0), bloom_yr2).add(leaf_yr)
    Final_Bloom = Final_Bloom.addBands(((Final_Bloom.select(0).add(Final_Bloom.select(1)).add(Final_Bloom.select(2))).divide(ee.Image(3))).round())
    task = ee.batch.Export.image(Final_Bloom, str(yr),
                                 {'maxPixels': 9999999999, 'scale': scl, 'driveFolder': folder, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()