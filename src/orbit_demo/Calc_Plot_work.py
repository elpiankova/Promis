# -*- coding: utf-8 -*- 
from math import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# Расчет координат пролета спутника

#данные для вычислений
T0 = 2456896.500000000 #(Julian day number), эпохальное время
n = 6.457576287408390e-02 # (degrees/sec), угловая частота вращения КА
e = 1.637994365076186e-03 # экцентриситет
eps = 0.0000001# ошибка
a = 6.795394080891185e+03#(km)
omega_big = 1.224602531823290e+02*pi/180#(rad)
omega_small = 5.823934876750221e+01*pi/180#(rad)
I = 6.198649551806115e+01*pi/180#(rad)
T = 2456896.507593647577 #(Julian day number), текущее время


i = 0
Lon = []
Lat = []
time = 300
while i <= time:
    E = 0
    E0 = 0.5 # произвольное начальное значение экцентрической аномалии
    M = n*((T - T0)*24*3600)#(degrees)
        #расчет средней аномалии (М)
    while M*pi/180 > 2*pi:
        M = M - 360
    
    while M*pi/180 < 0:
        M = M + 360

        # расчет Е
    n1 = 1
    while abs(E-E0) > eps:
        E0 = E
        E = M + e*sin(E0)
        n1 += 1

         # вспомагательные декартовые координаты
    X0 = a*(cos(E*pi/180) - e)
    Y0 = a*sqrt(1-e**2)*sin(E*pi/180)
    Z0 = 0
#            print('X0 = ',X0,' Y0 = ',Y0, ' Z0 = ',Z0)
            # расчет декартовых координат КА
    X = (cos(omega_big)*cos(omega_small)-sin(omega_big)*cos(I)*sin(omega_small))*X0 - \
        (cos(omega_big)*sin(omega_small)+sin(omega_big)*cos(I)*cos(omega_small))*Y0 + \
        sin(omega_big)*sin(I)*Z0
    Y = (sin(omega_big)*cos(omega_small)+cos(omega_big)*cos(I)*sin(omega_small))*X0 - \
        (sin(omega_small)*sin(omega_big)-cos(omega_big)*cos(I)*cos(omega_small))*Y0 - \
        cos(omega_big)*sin(I)*Z0
    Z = sin(I)*sin(omega_small)*X0 + sin(I)*cos(omega_small)*Y0 + cos(I)*Z0
#    print(X, Y, Z) 
            # переход из декартовых в сферические координаты
    fi = (180/pi)*atan2(Y, X) - 0.25/2*i # долгота
    teta = (180/pi)*atan2(Z, sqrt(X**2 + Y**2)) # широта
#            print(fi, teta)
    if fi < -180:
        fi = 180 - (abs(fi) - 180)

    Lon.append(fi)
    Lat.append(teta)
    print(Lon[i], Lat[i])
    i += 1
    T += 0.000694444/2
  
print(Lon)
print(Lat)    
Lon1 = Lon[0:177]
Lat1 = Lat[0:177]
Lon2 = Lon[178:300]
Lat2 = Lat[178:300]

    
# Отрисовка карты Земли с трассой спутника

# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
map = Basemap(projection='cyl', lat_0=0, lon_0=0,
              resolution='l', area_thresh=2000.0)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='coral')
map.drawmapboundary()

map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

x, y = map(Lon1, Lat1)
x1, y1 = map(Lon2, Lat2)

map.plot(x, y, '-', markersize=1, linewidth=2, color='b', markerfacecolor='b')
map.plot(x1, y1, '-', markersize=1, linewidth=2, color='b', markerfacecolor='b')

plt.show()
