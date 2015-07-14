from math import sin, cos, pi, sqrt, atan2, radians, asin

m = 1
k = (2*pi)**2

x = 1
V = 0

t = 0
dt = 0.01
h = 0.01

print("time x V E")
i = 0
V_list = []
a_list = []

#while i != 5:
#    a = - k / m * x
#    V += a * dt
#    x += V * dt
#
#    a_list.append(a)
#    V_list.append(V)
#
#    t += dt
#    i += 1

while i != 5:
    k1 = dt * (- k / m * x)
    l1 = dt * V
    k2 = dt * (- k / m * (x + l1/2))
    l2 = dt * (V + k1/2)
    k3 = dt * (- k / m * (x + l2/2))
    l3 = dt * (V + k2/2)
    k4 = dt * (- k / m * (x + l3))
    l4 = dt * (V + k3)

    V += 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    x += 1 / 6 * (l1 + 2 * l2 + 2 * l3 + l4)
    a = - k / m * x

    a_list.append(a)
    V_list.append(V)
#    print(t, x, V)
    i += 1
    t += dt

#print(t, a_list, V_list)

while t <= 5:

    V += (1901/720 * a_list[-1] - 1387/360 * a_list[-2] + 109/30 * a_list[-3] - 637/360 * a_list[-4] + 251/720 * a_list[-5]) * h
    x += (1901/720 * V_list[-1] - 1387/360 * V_list[-2] + 109/30 * V_list[-3] - 637/360 * V_list[-4] + 251/720 * V_list[-5]) * h

    a = - k / m * x

    a_list.append(a)
    a_list.pop(0)
    V_list.append(V)
    V_list.pop(0)

    t += dt

    E = k * x**2 / 2 + m * V**2 / 2
    #if int(t/dt) % 10 == 0:
    print(t, x, V, E)
