from math import sin, cos, pi

def from_spherical_to_decart(ro, theta, fi, m):
    x = ro * sin(theta) * cos(fi)
    y = ro * sin(theta) * sin(fi)
    z = ro * cos(theta)
    return [x, y, z, m]

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
print("x y z m")
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
        while fi < 2 *pi:
            i += 1
            fi += dfi
            m = density * ro**2 * sin(theta) * dro * dtheta * dfi
            list.append( from_spherical_to_decart(ro - dro/2, theta - dtheta/2, fi - dfi/2, m) )
            print(list[i][0], list[i][1], list[i][2], m)

            #list.append([ro - dro/2, theta - dtheta/2, fi - dfi/2, m])
            #print(ro - dro/2, theta - dtheta/2, fi - dfi/2, m)

#print(list)
print(i)






