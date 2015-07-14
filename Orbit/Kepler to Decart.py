## N = longitude of the ascending node
## i = inclination to the ecliptic (plane of the Earth's orbit)
## w = argument of perihelion
## a = semi-major axis, or mean distance from Sun
## e = eccentricity (0=circle, 0-1=ellipse, 1=parabola)
## M = mean anomaly (0 at perihelion; increases uniformly with time)
## w1 = N + w   = longitude of perihelion
## L  = M + w1  = mean longitude
## q  = a*(1-e) = perihelion distance
## Q  = a*(1+e) = aphelion distance
## P  = a ^ 1.5 = orbital period (years if a is in AU, astronomical units)
## T  = Epoch_of_M - (M(deg)/360_deg) / P  = time of perihelion
## v  = true anomaly (angle between position and perihelion)
## E  = eccentric anomaly

from math import atan2, sqrt, sin, cos, asin, radians, degrees, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

## Orbital elements of the ISS:
N = radians(247.4627)
i = radians(51.6416)
w = radians(130.5360)
nu = 15.72125391/24/60/60
e = 0.0006703
M = radians(325.0288)
ecl = radians(23.4393)
G = 6.67384e-11
Me = 5.9726e24
#for ISS
M_s = 450000
alpha = G * Me

a = (alpha/nu**2.0/4/pi/pi)**(1.0/3.0)


E0 = 1e10
E = M + e * sin(M) * (1.0 + e * cos(M))

while E0-E > radians(1e-5):
    E0 = E
    E = E0 - (E0 - e * sin(E0) - M) / (1 - e * cos(E0))

xv = a * (cos(E) - e)
yv = a * (sqrt(1 - e**2) * sin(E))

v = atan2(yv, xv)
r = sqrt(xv ** 2 + yv ** 2)
print(r)


xe = r * (cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i))
ye = r * (sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i))
ze = r * (sin(v+w) * sin(i))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(0, 0, 0, s=600)
ax.scatter(xe, ye, ze, s=20)
#plt.show()

V = sqrt( 2 * (-alpha / 2 / a + alpha / r) )
print(V)
E = M_s * V**2 / 2 - alpha * M_s / r
ksi = asin(sqrt( (e**2 - 1) * (M_s * Me)/(M_s + Me) * alpha**2 * M_s ** 2 / 2 / E ) / M_s / V / r)
ksi = degrees(ksi)
print(ksi)

Vxe = V * (cos(N) * cos(v+w+pi-ksi) - sin(N) * sin(v+w+pi-ksi) * cos(i))
Vye = V * (sin(N) * cos(v+w+pi-ksi) + cos(N) * sin(v+w+pi-ksi) * cos(i))
Vze = V * (sin(v+w+pi-ksi) * sin(i))

print(Vxe, Vye, Vze, sqrt(Vxe**2 + Vye**2 + Vze**2), V)