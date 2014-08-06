# -*- coding: utf-8 -*- 
# расчитываем экцентрическую аномалию (Е) и координаты КА
from math import *
# Кеплеры и другие элементы
E0 = 0.5 # произвольное начальное значение экцентрической аномалии
T0 = 2456794.500000000 # эпохальное время
T = 2456794.471266817767 # текущее время
n = 6.458028291792567e-02*86400 # угловая частота вращения КА
e = 6.636160892353949e-04 # экцентриситет
eps = 0.0000001# ошибка
M = n*(T0 - T)
print(M)
a =
omega_big = 
omega_small = 
I = 

# начало той части, которую не могу вспомнить

#расчет средней аномалии (М)
#while M > 2*pi:
#    M = M - 2*pi
    
#print(M)    

# расчет Е
n1 = 1
while abs(E-E0) > eps:
    E = M + e*sin(E0)
    E0 = E
    n1 += 1
    
print(E,n1)

# конец той части, которую не могу вспомнить

# вспомагательные декартовые координаты
X0 = a*(cos(E) - e)
Y0 = a*sqrt(1-e**2)*sin(E)
Z0 = 0
# расчет декартовых координат КА
X = (cos(omega_big)*cos(omega_small)-sin(omega_big)*cos(I)*sin(omega_small))*X0 - \
    (cos(omega_big)*sin(omega_small)+sin(omega_big)*cos(I)*cos(omega_small))*Y0 + sin(omega_big)*sin(I)*Z0
Y = (sin(omega_big)*cos(omega_small)+cos(omega_big)*cos(I)*sin(omega_small))*X0 - \
    (sin(omega_small)*sin(omega_big)-cos(omega_big)*cos(I)*cos(omega_small))*Y0 - cos(omega_big)*sin(I)*Z0
Z = sin(I)*sin(omega_small)*X0 + sin(I)*cos(omega_small)*Y0 + cos(I)*Z0
print(X, Y, Z)
# переход из декартовых в сферические координаты, т.е. расчет координат КА в данный момент (долготы и широты)
fi = atan2(Y, X) # широта 
teta = 90 - atan2(Z, sqrt(X**2+Y**2)) # долгота
print(fi, teta)