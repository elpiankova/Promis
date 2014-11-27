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
time = 11838
while i <= time:
#hgjhjkhk
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
    T += 0.000694444/8 # дискредетация 1/8 минуты

end_array = []
Lon3 = []
Lon4 = Lon
# разбивка массива координат по долготе на подмассивы по "виткам"
while len(Lon4) > 0:
        
    begin = 0
    end = 0
    end1 = 0

    for i in range(len(Lon4)):
        if end == 0:
            if Lon4[i] < 180 and Lon4[i] > 0:
                end = i
            else: pass
        else: pass

    Lon1 = Lon4[end:]

    for i in range(len(Lon1)):
        if end1 == 0:
            if Lon1[i] < 0 or Lon1[i] == Lon1[-1] :
                end1 = i
            else: pass
            if Lon1[i] == Lon1[-1]:
                end += 1
            else: pass
        else: pass    
    end = end1 + end 
    
    end_array.append(end)
    Lon3.append(Lon4[begin:end])
    Lon4 = Lon4[end:]
    
end = end_array[0]

Lon1 = Lon[end:]
Lon2 = Lon[:end]

add_array = Lon3[1:]
# формирование одного массива координат по долготе с поправкой, для отрисовки на всей длины карты
i = 0
j = 0
popravka = 180

for i in range(len(add_array)):
    for j in range(len(add_array[i])):
        if add_array[i][j] <=0:
            add_array[i][j] = popravka + (180 - abs(add_array[i][j]))#внесение поправки
            Lon2.append(add_array[i][j])
        elif add_array[i][j] > 0 :
            add_array[i][j] = popravka + 180 + abs(add_array[i][j])#внесение поправки
            Lon2.append(add_array[i][j])
    popravka += 360 


Lon = Lon2

blok = []
coordinatelane = []
fh = open("/home/yakim/PROJECTS/orbit_plot/www/html/planelatlong.js", "w")
fh.write("var planelatlong = ")
fh.close()
print(Lon)
print(len(Lon))
print(len(Lat))

# формирование финального массива координат для отрисовки на карте
i = 0
for i in range(len(Lon)) and range(len(Lat)):
    blok.append(Lat[i])
    blok.append(Lon[i])
    coordinatelane.append(blok)
    blok = []
    
#print coordinatelane

coord_srt = str(coordinatelane)


fh = open("/home/yakim/PROJECTS/orbit_plot/www/html/planelatlong.js", "a")
fh.write(coord_srt)
fh.close()