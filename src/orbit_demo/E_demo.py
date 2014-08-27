# -*- coding: utf-8 -*- 
# расчитываем экцентрическую аномалию (Е) и координаты КА
from math import *
# Кеплеры и другие элементы
E0 = 0.5 # произвольное начальное значение экцентрической аномалии
T0 = 2456794.500000000 #(Julian day number), эпохальное время
T = 2456794.471266817767 #(Julian day number), текущее время
n = 0.06458028291792567 # (degrees/sec), угловая частота вращения КА
e = 0.0006636160892353949 # экцентриситет
eps = 0.0000001# ошибка
a = 6795.076999205232#(km)
M = n*((T0 - T)*24*3600)#(degrees)
omega_big = 239.4100727837198*pi/180#(rad)
omega_small = 87.64322621108833*pi/180(rad)
I = 61.02565356512720*pi/180(rad)
E = 0

#расчет средней аномалии (М)
while M*pi/180 > 2*pi:
    M = M - 360
    

#while M < 0:
#    M = M + 2*pi

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
print(X, Y, Z) # -1.332128873099773E+03  3.747324942804415E+03 -5.514869586944249E+03
# переход из декартовых в сферические координаты
fi = (180/pi)*atan2(Y, X) # широта 
teta = (180/pi)*atan2(Z, sqrt(X**2 + Y**2)) # долгота
print(fi, teta)
