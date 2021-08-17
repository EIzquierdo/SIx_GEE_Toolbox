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

folder = 'LeafDaymet'
reg = [[[-126.3, 49.25], [-126.3, 14.30], [-56.17, 14.30], [-56.17, 49.25]]]
scl = 4638.23937

data = 'Daymet'
Image11 = [ee.Image('users/Emma/Leaf' + str(data) + '1/1980'), ee.Image('users/Emma/Leaf' + str(data) + '1/1981'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1982'), ee.Image('users/Emma/Leaf' + str(data) + '1/1983'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1984'), ee.Image('users/Emma/Leaf' + str(data) + '1/1985'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1986'), ee.Image('users/Emma/Leaf' + str(data) + '1/1987'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1988'), ee.Image('users/Emma/Leaf' + str(data) + '1/1989'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1990'), ee.Image('users/Emma/Leaf' + str(data) + '1/1991'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1992'), ee.Image('users/Emma/Leaf' + str(data) + '1/1993'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1994'), ee.Image('users/Emma/Leaf' + str(data) + '1/1995'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1996'), ee.Image('users/Emma/Leaf' + str(data) + '1/1997'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/1998'), ee.Image('users/Emma/Leaf' + str(data) + '1/1999'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2000'), ee.Image('users/Emma/Leaf' + str(data) + '1/2001'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2002'), ee.Image('users/Emma/Leaf' + str(data) + '1/2003'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2004'), ee.Image('users/Emma/Leaf' + str(data) + '1/2005'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2006'), ee.Image('users/Emma/Leaf' + str(data) + '1/2007'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2008'), ee.Image('users/Emma/Leaf' + str(data) + '1/2009'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2010'), ee.Image('users/Emma/Leaf' + str(data) + '1/2011'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2012'), ee.Image('users/Emma/Leaf' + str(data) + '1/2013'),
        ee.Image('users/Emma/Leaf' + str(data) + '1/2014'), ee.Image('users/Emma/Leaf' + str(data) + '1/2015')]


Image14 = [ee.Image('users/Emma/Leaf' + str(data) + '4km1/1980'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1981'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1982'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1983'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1984'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1985'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1986'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1987'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1988'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1989'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1990'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1991'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1992'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1993'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1994'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1995'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1996'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1997'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/1998'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/1999'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2000'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2001'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2002'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2003'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2004'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2005'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2006'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2007'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2008'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2009'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2010'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2011'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2012'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2013'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km1/2014'), ee.Image('users/Emma/Leaf' + str(data) + '4km1/2015')]


    # Leaf de 1Km!!!

Image21 = [ee.Image('users/Emma/Leaf' + str(data) + '2/1980'), ee.Image('users/Emma/Leaf' + str(data) + '2/1981'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1982'), ee.Image('users/Emma/Leaf' + str(data) + '2/1983'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1984'), ee.Image('users/Emma/Leaf' + str(data) + '2/1985'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1986'), ee.Image('users/Emma/Leaf' + str(data) + '2/1987'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1988'), ee.Image('users/Emma/Leaf' + str(data) + '2/1989'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1990'), ee.Image('users/Emma/Leaf' + str(data) + '2/1991'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1992'), ee.Image('users/Emma/Leaf' + str(data) + '2/1993'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1994'), ee.Image('users/Emma/Leaf' + str(data) + '2/1995'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1996'), ee.Image('users/Emma/Leaf' + str(data) + '2/1997'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/1998'), ee.Image('users/Emma/Leaf' + str(data) + '2/1999'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2000'), ee.Image('users/Emma/Leaf' + str(data) + '2/2001'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2002'), ee.Image('users/Emma/Leaf' + str(data) + '2/2003'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2004'), ee.Image('users/Emma/Leaf' + str(data) + '2/2005'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2006'), ee.Image('users/Emma/Leaf' + str(data) + '2/2007'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2008'), ee.Image('users/Emma/Leaf' + str(data) + '2/2009'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2010'), ee.Image('users/Emma/Leaf' + str(data) + '2/2011'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2012'), ee.Image('users/Emma/Leaf' + str(data) + '2/2013'),
        ee.Image('users/Emma/Leaf' + str(data) + '2/2014'), ee.Image('users/Emma/Leaf' + str(data) + '2/2015')]


Image24 = [ee.Image('users/Emma/Leaf' + str(data) + '4km2/1980'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1981'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1982'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1983'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1984'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1985'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1986'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1987'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1988'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1989'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1990'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1991'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1992'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1993'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1994'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1995'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1996'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1997'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/1998'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/1999'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2000'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2001'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2002'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2003'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2004'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2005'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2006'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2007'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2008'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2009'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2010'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2011'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2012'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2013'),
        ee.Image('users/Emma/Leaf' + str(data) + '4km2/2014'), ee.Image('users/Emma/Leaf' + str(data) + '4km2/2015')]

leaf = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image14, Image11))
leaf2 = ee.List(ee.Algorithms.If(ee.Number(scl).eq(4638.23937), Image24, Image21))

year = range(1980, 2016)

for m in range(35, 36):
    yr = year[m]
    leaf_yr = ee.Image(ee.List(leaf).get(m))
    leaf_yr2 = ee.Image(ee.List(leaf2).get(m))
    Final_Leaf = leaf_yr.where(leaf_yr.eq(0), leaf_yr2)
    Final_Leaf = Final_Leaf.addBands(((Final_Leaf.select(0).add(Final_Leaf.select(1)).add(Final_Leaf.select(2))).divide(ee.Image(3))).round())
    task = ee.batch.Export.image(Final_Leaf, str(yr),
                                 {'maxPixels': 9999999999, 'driveFolder': folder, 'scale': scl, 'region': reg})
    task.start()
    while task.status()['state'] == 'RUNNING':
        print 'Running...'
        time.sleep(1)
    print 'Done.', task.status()