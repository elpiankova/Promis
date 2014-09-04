# -*- coding: utf-8 -*- 
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from E_demo_1 import Orbit_calculate
from math import *

class Data_orbit(Orbit_calculate):
    T0 = 2456896.500000000 #(Julian day number), эпохальное время
    n = 6.457576287408390e-02 # (degrees/sec), угловая частота вращения КА
    e = 1.637994365076186e-03 # экцентриситет
    eps = 0.0000001# ошибка
    a = 6.795394080891185e+03#(km)
    omega_big = 1.224602531823290e+02*pi/180#(rad)
    omega_small = 5.823934876750221e+01*pi/180#(rad)
    I = 6.198649551806115e+01*pi/180#(rad)
    T = 2456896.507593647577 #(Julian day number), текущее время
    def _init_(T0, n, e, eps, a, omega_big, omega_small, I, T):
        Orbit_calculate.all_orbit(T0, n, e, eps, a, omega_big, omega_small, I, T)
        

# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
map = Basemap(projection='cyl', lat_0=50, lon_0=50,
              resolution='l', area_thresh=1000.0)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='coral')
map.drawmapboundary()

map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

lons= [130.0347968958357,128.1267780629088, 126.26167270570916, 124.4218048935301, 
122.59877628945893,120.77552056098396, 118.93984057479392, 117.08108490479621, 115.18032887516296, 113.22728187013215, 
111.20366756129992, 109.0892795249134, 106.86879075371877, 104.51278663153055, 101.99753473034983, 99.29262468286643, 96.35514070869407,
93.14997805102541, 89.62098150694054, 85.71104828271012, 81.36376138610787]

lats = [13.915867912505632, 10.514139996976748, 7.103504783642812, 3.681251424040815, 0.26037395781015504, 
-3.1630468660391946, -6.5838748404351595, -9.993555757277317, -13.39734666102602, -16.782763858279964, 
-20.148839177535557, -23.493636519221088, -26.803243162171054, -30.079714776283037, -33.309884076958035, -36.482912795705985,
-39.59366053967854, -42.6191871112062, -45.547845712229005, -48.35696157493297, -51.01489127822661]

x, y = map(lons, lats)

map.plot(x, y, '-', markersize=1, linewidth=2, color='b', markerfacecolor='b')
 
plt.show()