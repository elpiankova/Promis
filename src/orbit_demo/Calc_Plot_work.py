# -*- coding: utf-8 -*- 
from math import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from decimal import Decimal, getcontext
getcontext().prec = 19

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

#(Julian day number), текущее время
def julian_day_number():
    d= datetime.utcnow()
    r = d.timetuple()
    
    D = []
    for it in r:
        D.append(it)
        
    year = D[0]
    month = D[1]
    day = D[2]
    hour = D[3]
    minute = D[4]
    sec = D[5]
    
    julian_day = day - 32075 + 1461*(year + 4800 + (month - 14)/12)/4 + \
                 367*(month - 2 - (month - 14)/12*12)/12 - 3*((year + 4900 + \
                 (month - 14)/12)/100)/4
                 
    if hour >= 12 and hour < 24:
        hour = hour - 12
    else:
        hour = hour + 12
    
    
    fractional_part = float(hour*3600+minute*60+sec)/(86400)
    julian_day = Decimal(julian_day) + Decimal(fractional_part)
    
    return julian_day

T = julian_day_number() #(Julian day number), текущее время
#print T

i = 0
Lon = []
Lat = []
time = 2000
while i <= time:
#hgjhjkhk
    E = 0
    E0 = 0.5 # произвольное начальное значение экцентрической аномалии
    M = n*float((T - Decimal(T0))*24*3600)#(degrees)
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
# расчет декартовых координат КА
    X = (cos(omega_big)*cos(omega_small)-sin(omega_big)*cos(I)*sin(omega_small))*X0 - \
        (cos(omega_big)*sin(omega_small)+sin(omega_big)*cos(I)*cos(omega_small))*Y0 + \
        sin(omega_big)*sin(I)*Z0
    Y = (sin(omega_big)*cos(omega_small)+cos(omega_big)*cos(I)*sin(omega_small))*X0 - \
        (sin(omega_small)*sin(omega_big)-cos(omega_big)*cos(I)*cos(omega_small))*Y0 - \
        cos(omega_big)*sin(I)*Z0
    Z = sin(I)*sin(omega_small)*X0 + sin(I)*cos(omega_small)*Y0 + cos(I)*Z0
# переход из декартовых в сферические координаты
    fi = (180/pi)*atan2(Y, X) - 0.25*i/8 # долгота
    teta = (180/pi)*atan2(Z, sqrt(X**2 + Y**2)) # широта

    if fi < -180:
        fi = 180 - (abs(fi) - 180)

    Lon.append(fi)
    Lat.append(teta)

    i += 1
    T += Decimal(0.000694444/8) # дискредетация 1/8 минуты

Lon2 = []
Lat2 = []
print len(Lon)
while len(Lon) > 0:
       
    begin = 0
    end = 0
    end1 = 0

    for i in range(len(Lon)):
        if end == 0:
            if Lon[i] > 0 and Lon[i] < 180:
                end = i
            else: pass
        else: pass

    Lon1 = Lon[end:]

    if end != 0:
        for i in range(len(Lon1)):
            
                if end1 == 0:
                    if Lon1[i] < 0 or Lon1[i] == Lon1[-1] :
                        end1 = i
                    else: pass
                    if Lon1[i] == Lon1[-1]:
                        end += 1
                    else: pass
                else: pass
    else:
        end1 = len(Lon)
                 
    end = end1 + end 
    
    Lon2.append(Lon[begin:end])
    Lat2.append(Lat[begin:end])

    Lon = Lon[end:]
    Lat = Lat[end:]
    
    
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

for i in range(len(Lon2)) and range(len(Lat2)):    
    x, y = map(Lon2[i], Lat2[i])
    map.plot(x, y, '-', markersize=1, linewidth=2, color='b', markerfacecolor='b')

print Lon2
print Lat2
print len(Lon2)
print len(Lat2)


plt.show()