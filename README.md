# Extended Spring Indices: Toolbox to process in Google Earth Engine.

This toolbox contains the scripts needed to calculate the spring onset (Leaf and Bloom indices) using Google Earth Engine python API.

# Overview

Changes in climate are a current reality, they are evident in observacional weather and ecological records. Understand the different causes and impacts of the climate change are fundamental to fight against it. Therefore, consitent indicators are needed as phenological observations or phenological indicators. The latter have been derived using phenological models. The Extended Spring Indices models (SI-x), which was developed by [Schwartz in 2013](https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/joc.3625), is a suite of simple models thermal models without chilling requirements. The SI-x models are used to generate a [Start of Spring indicator](http://www.globalchange.gov/explore/indicators) which is included in the US Global Change Research Program.The Start of Spring indicator is important because of providing a direct connection between vegetation phenology effects and global warming.

The availability of the SIx models were focused on specific locations (based onplant stations) or coarse spatial resolution (gridded produts). Recetly products, as the products provided by [Crimmins et al](https://pubs.er.usgs.gov/publication/ofr20171003), increased the spatial resolution until 4 km. However, higher spatial resolution phenological products could be used to obtain more realistic views of local phenology and to support regional ecological studies. Here, the SI-x models have been scale up to cloud computing to provide new long term phenological products at 1 km grids.

# Background

The SI-x models require daily maximum and minimum temperature as well as the day length (i.e. the hours with sunlight). From them, the Growing Degree Hours (GDH) is calculated and used to define accumulation of short- and long-term variables. These variable are used to predict **Leaf** and **Bloom** indices. The SI-x models are primary calculated for three indicator plant species (Lilac (Syringa chinensis “Red Rothomagensis”)) and Honeysuckle (Lonicera tatarica “Arnold Red” and Lonicera korolkowii “Zabeli”)). The final indices are the average of the three plants. The SI-x models per plant is a regeression based model that its coefficients were calculated by [Schwartz in 2013](https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/joc.3625):
* For **Leaf** index: 

$$DDE\cdot20.201+DD57\cdot0.153+SYNOP\cdot13.878+MDS0\cdot3.306>=1000 \text{ (Lilac)}$$

$$DD57\cdot0.248+SYNOP\cdot20.899+MDS0\cdot4.266>=1000  \text{ (Arnold Red Honeysuckle)}$$

$$DDE2\cdot0.266+SYNOP\cdot21.433+MDS0\cdot2.802>=1000 \text{ (Zabeli Honeysuckle)}$$

$DDE2$ is the accumulated GDH from day $t$ until day $t+2$, $DD57$ is the accumulated GDH from day $t+5$ until day $t+7$ with $t$ being a temporal index from January $1^{st}$, $ASYNOP$ is accumulative of the synop variable which is $1$ when $DDE2>637$ and otherwise is $0$ and $MDS0$ is a counter that starts on January $1^{st}$.

* For **Bloom** index:

$$ACGDH\cdot0.116-MDS0\cdot23.934>=1000$$

$$ACGDH\cdot0.127+MDS0\cdot24.825>=1000$$

$$ACGDH\cdot0.096+MDS0\cdot11.368>=1000$$

where $ACGDH$ is the accumulation of GDH from LF index and, $MDS0$ is still a counter but it starts on the LF index date.

## Study areas

At the present, there are two study areas of the new SI-x products available:
* North and Central America (located between 14°02'31.3"N and 55°37'04.1"N latitude and 56°05'50.7"W 126°22'06.1"W longitude). [Daymet version 4](https://daymet.ornl.gov/) from 1980 to 2021, were used to generated the dataset of this study area. The needed data (i.e. daily maximunim and minimum temperature and the daylength) are available GEE database.
* Europe (located between 35°55'48.7"N and 73°32'47.1"N latitude and  10°36'29.5"W and 44°50'29.5"E longitude). The daily maximum and minimum temperature used is the [Downscaled version of European Observations (E-OBS)](https://rmets.onlinelibrary.wiley.com/doi/10.1002/joc.4436) version 3 from 1950 to 2020. Downscaled E-OBS is avabalible for downloading [here](/url{ftp://palantir.boku.ac.at/Public/ClimateData}). The daylength is calculated once the data are ingested. In this case, the data is not avaibailable in GEE database and it is needed to ingest the data in the API.

Leaf over America             |  Leaf over Europe
:-------------------------:|:-------------------------:
<img width="350" height="200" src="./gif/America.gif">  |   <img width="350" height="200" src="./gif/Europe.gif">

# Instalation:

To install the libraries:

    pip install -r requirements.txt
