#!/usr/bin/python
#Project Storm: Plot trajectories of convective systems
#import libraries

import numpy as np
from mpl_toolkits.basemap import Basemap
import  matplotlib.pyplot as pl

# Plot a map for Mexico

m = Basemap(projection='cyl', llcrnrlat=12, urcrnrlat=35,llcrnrlon=-120, urcrnrlon=-80, resolution='c', area_thresh=1000.)
m.bluemarble()
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawstates(linewidth=0.5)

#Draw parallels and meridians

m.drawparallels(np.arange(10.,35.,5.))
m.drawmeridians(np.arange(-120.,-80.,10.))
m.drawmapboundary(fill_color='aqua')

#Open file whit numpy

data = np.loadtxt('data.csv', dtype=np.str,delimiter=',', skiprows=1)
latitude = data[:,0]
longitude = data[:,1]

#Convert latitude and longitude to coordinates X and Y

x, y = m(longitude, latitude)

#Plot the points on the map

pl.plot(x,y,'ro-')
pl.show()