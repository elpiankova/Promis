# -*- coding: utf-8 -*- 
# расчитываем экцентрическую аномалию (Е) и координаты КА
from math import *
# Кеплеры и другие элементы
# Константы для расчета
T0 = 2456896.500000000 #(Julian day number), эпохальное время
n = 6.457576287408390e-02 # (degrees/sec), угловая частота вращения КА
e = 1.637994365076186e-03 # экцентриситет
eps = 0.0000001# ошибка
a = 6.795394080891185e+03#(km)
omega_big = 1.224602531823290e+02*pi/180#(rad)
omega_small = 5.823934876750221e+01*pi/180#(rad)
I = 6.198649551806115e+01*pi/180#(rad)
# Велечины в расчетном цикле
T = 2456896.507593647577 #(Julian day number), текущее время

i = 0
while i <= 20:
    
    E = 0
    E0 = 0.5 # произвольное начальное значение экцентрической аномалии
    M = n*((T0 - T)*24*3600)#(degrees)
    #расчет средней аномалии (М)
    while M*pi/180 > 2*pi:
        M = M - 360
    

    while M*pi/180 < 0:
        M = M + 360

    print(M)  

# расчет Е
    n1 = 1
    while abs(E-E0) > eps:
        E0 = E
        E = M + e*sin(E0)
        n1 += 1
    
    
    print(E,n1)

    # вспомагательные декартовые координаты
    X0 = a*(cos(E*pi/180) - e)
    Y0 = a*sqrt(1-e**2)*sin(E*pi/180)
    Z0 = 0
    print('X0 = ',X0,' Y0 = ',Y0, ' Z0 = ',Z0)
# расчет декартовых координат КА
    X = (cos(omega_big)*cos(omega_small)-sin(omega_big)*cos(I)*sin(omega_small))*X0 - \
        (cos(omega_big)*sin(omega_small)+sin(omega_big)*cos(I)*cos(omega_small))*Y0 + sin(omega_big)*sin(I)*Z0
    Y = (sin(omega_big)*cos(omega_small)+cos(omega_big)*cos(I)*sin(omega_small))*X0 - \
        (sin(omega_small)*sin(omega_big)-cos(omega_big)*cos(I)*cos(omega_small))*Y0 - cos(omega_big)*sin(I)*Z0
    Z = sin(I)*sin(omega_small)*X0 + sin(I)*cos(omega_small)*Y0 + cos(I)*Z0
    print(X, Y, Z) 
# переход из декартовых в сферические координаты
    fi = (180/pi)*atan2(Y, X) # долгота
    teta = (180/pi)*atan2(Z, sqrt(X**2 + Y**2)) # широта
    print(fi, teta)
    
    i += 1
    T += 0.000694444
