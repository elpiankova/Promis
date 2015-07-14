from math import sin, cos, pi, sqrt, atan2, degrees
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#class of satellite#
class satellite(object):
    def __init__(self, ro, theta, fi):
        self.ro = ro
        self.theta = theta
        self.fi = fi
        self.x = ro * sin(theta) * cos(fi)
        self.y = ro * sin(theta) * sin(fi)
        self.z = ro * cos(theta)
        self.Vx = 0
        self.Vy = 7.66e3
        self.Vz = 0

    def update(self):
        self.ro = sqrt(self.x**2 + self.y**2 + self.z**2)
        self.theta = atan2(sqrt(self.x**2 + self.y**2), self.z)
        self.fi = atan2(self.y, self.x)

def from_spherical_to_decart(ro, theta, fi, m):
    x = ro * sin(theta) * cos(fi)
    y = ro * sin(theta) * sin(fi)
    z = ro * cos(theta)
    return [x, y, z, m]

#Generation of list of points with "small" mass to describe Earth like unDot mass body
#--------------------Find Density as a function of radius--------------------!!!!!!!!!!
def Earth_Gen():
    ro = 0
    theta = 0
    fi = 0
    i = -1

    dro = 6378.1e3 / 20
    dtheta = pi / 20
    dfi = 2 * pi / 20

    #density = 5.1166e+03

    list = []
    #print("ro theta fi m")
    #print("x y z m")
    while ro < dro * 20:
        ro += dro
        theta = 0
        density = (ro - dro/2 < 1258.1e3) * 18e3 + (1258.1e3 <= ro - dro/2 < 3678.1e3) * 9.5e3 + \
                  (3678.1e3 <= ro - dro/2 < 5478.1e3) * 5e3 + (5478.1e3 <= ro - dro/2 < 5978.1e3) * 3.2e3 + \
                  (5978.1e3 <= ro - dro/2) * 2.8e3
        density *= 0.9525
        while theta < pi:
            theta += dtheta
            fi = 0
            while fi < 2 * pi:
                i += 1
                fi += dfi
                m = density * ro**2 * sin(theta) * dro * dtheta * dfi
                list.append( from_spherical_to_decart(ro - dro/2, theta - dtheta/2, fi - dfi/2, m) )
    return list
#Opening Files to write#
PositionList = open("PositionList.txt", 'w')
PositionList.truncate()
Long_Lat = open("Long_Lat.txt", "w")
Long_Lat.truncate()
PositionList.write("x y z \n")
PositionList.write("0 0 0 \n")
Long_Lat.write("time ro Longitude Latitude \n")

#INIT parametrs#
Earth = Earth_Gen()
m = 200
G = 6.67384e-11
#Satellite position and speed#
s = satellite(6356.8e3 + 900e3, pi/4, 0)
#Time and dt in seconds#
dt = 30
time = 0
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(0, 0, 0, s=60)
#ax.set_xlim(-1.2e7, 1.2e7)
#ax.set_ylim(-1.2e7, 1.2e7)
#ax.set_zlim(-1.2e7, 1.2e7)

#print('time ', 'ro ', 'theta ', 'fi')
#print('time ', 'ro ', 'Longitude ', 'Latitude')

#Main loop#
#---------------------Euler Method------------------------#
while time <= 60 * 60 * 12:
    a_x, a_y, a_z = 0, 0, 0
    #recountig forces and acceleration#
    for i in range(0, 8000):
        e = Earth[i]
        dist = sqrt((e[0]-s.x)**2 + (e[1]-s.y)**2 + (e[2]-s.z)**2)
        force = -G * e[3] * m / dist / dist
        a_x += force * (s.x - e[0]) / s.ro / m
        a_y += force * (s.y - e[1]) / s.ro / m
        a_z += force * (s.z - e[2]) / s.ro / m
    #New Velocity and position#
    s.Vx += a_x * dt
    s.Vy += a_y * dt
    s.Vz += a_z * dt
    s.x += s.Vx*dt
    s.y += s.Vy*dt
    s.z += s.Vz*dt
    #updating parameters#
    time += dt
    s.update()
    #write to file and/or plot every ______ step#
    if int(time/dt) % 7 == 0:
        #ax.scatter(s.x, s.y, s.z, s=2)
        print(time)

        line = str(s.x) + " " + str(s.y) + " " + str(s.z) + "\n"
        PositionList.write(line)

        #print(time, s.ro, s.theta, s.fi)

        Longitude = s.fi + time * 2 * pi / 24 / 60 / 60
        while Longitude > pi:
            Longitude -= 2 * pi
        Latitude = s.theta - pi / 2
        line = str(time) + " " + str(s.ro) + " " + str(degrees(Longitude)) + " " + str(degrees(Latitude)) + "\n"
        Long_Lat.write(line)

        #print(time, s.ro, degrees(Longitude), degrees(Latitude))

#plt.show()

PositionList.close()
Long_Lat.close()





