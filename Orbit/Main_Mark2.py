from math import sin, cos, pi, sqrt, atan2, radians, acos


#class of satellite#
class satellite(object):
    def __init__(self, i, N, e, w, M, nu, m):
        N = radians(N)
        i = radians(i)
        w = radians(w)
        nu = nu/24/60/60
        M = radians(M)
        m = m

        G = 6.67384e-11
        Me = 5.9726e24
        alpha = G * Me
        a = (alpha/nu**2.0/4/pi/pi)**(1.0/3.0)

        E0 = M
        E = e * sin(E0) + M
        while E - E0 >= radians(1e-10):
            E0 = E
            E = e * sin(E0) + M

        xv = a * (cos(E) - e)
        yv = a * (sqrt(1 - e**2) * sin(E))

        v = atan2(yv, xv)
        r = sqrt(xv ** 2 + yv ** 2)

        self.x = r * (cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i))
        self.y = r * (sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i))
        self.z = r * (sin(v+w) * sin(i))

        h = sqrt(alpha * a * (1 - e**2))
        p = a * (1 - e**2)

        A = h * e / r / p * sin(v)

        self.Vx = (1 + 0.0) * (self.x * A - h / r * (cos(N) * sin(v+w) + sin(N) * cos(v+w) * cos(i)))
        self.Vy = (1 + 0.0) * (self.y * A - h / r * (sin(N) * sin(v+w) - cos(N) * cos(v+w) * cos(i)))
        self.Vz = (1 + 0.0) * (self.z * A + h / r * sin(i) * cos(w+v))

        self.update()

        self.N = N
        self.i = i
        self.w = w
        self.nu = nu
        self.M = M
        self.m = m
        self.e = e
        self.a = a



    def update(self):
        self.ro = sqrt(self.x**2 + self.y**2 + self.z**2)
        self.theta = atan2(sqrt(self.x**2 + self.y**2), self.z)
        self.fi = atan2(self.y, self.x)


def from_spherical_to_decart(ro, theta, fi):
    x = ro * sin(theta) * cos(fi)
    y = ro * sin(theta) * sin(fi)
    z = ro * cos(theta)
    return [x, y, z]


#From TLE data using this def we could get Descartes velocity and position#
def Get_Descartes_data(s: satellite):
    N = radians(40.5433) #Right ascension of the ascending node
    i = radians(66.2708) #incl
    w = radians(93.5771) #Argument of perigee
    nu = 0.50315154/24/60/60 #Mean Motion (revolutions per day)
    e = 0.8019403 #Eccentricity (decimal point assumed)
    M = radians(359.9354) #Mean Anomaly (degrees)
    G = 6.67384e-11
    Me = 5.9726e24
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

    s.x = r * (cos(N) * cos(v+w) - sin(N) * sin(v+w) * cos(i))
    s.y = r * (sin(N) * cos(v+w) + cos(N) * sin(v+w) * cos(i))
    s.z = r * (sin(v+w) * sin(i))

    h = sqrt(alpha * a * (1 - e**2))
    p = a * (1 - e**2)

    A = h * e / r / p * sin(v)

    s.Vx = (1 + 0.0) * (s.x * A - h / r * (cos(N) * sin(v+w) + sin(N) * cos(v+w) * cos(i)))
    s.Vy = (1 + 0.0) * (s.y * A - h / r * (sin(N) * sin(v+w) - cos(N) * cos(v+w) * cos(i)))
    s.Vz = (1 + 0.0) * (s.z * A + h / r * sin(i) * cos(w+v))

    return s


#Getting theoretical orbit using Kepler problem#
def Kepler_solver(s:satellite):

    PositionList_Kepler_solver = open("PositionList_Kepler_solver.txt", 'w')
    PositionList_Kepler_solver.truncate()
    PositionList_Kepler_solver.write("x y z \n")
    PositionList_Kepler_solver.write("0 0 0 \n")

    dv = radians(1)
    v = 0
    while v <= 2*pi:
        v += dv
        #Get orbit in orbital plane#
        ro = s.a * (1 - s.e**2) / (1 + s.e * cos(v))

        #Rotating gained points#
        x = ro * (cos(s.N) * cos(v+s.w) - sin(s.N) * sin(v+s.w) * cos(s.i))
        y = ro * (sin(s.N) * cos(v+s.w) + cos(s.N) * sin(v+s.w) * cos(s.i))
        z = ro * (sin(v+s.w) * sin(s.i))

        line = str(x) + " " + str(y) + " " + str(z) + "\n"
        PositionList_Kepler_solver.write(line)

    PositionList_Kepler_solver.close()


#Solving Newton's eq. using Euler method#
def Earth_is_point_Euler(s: satellite, time):
    M = 5.97219E24
    G = 6.67384E-11
    t = 0
    dt = 20

    Mu = - G * M

    #s.x = -3669.868950e3
    #s.y = -6055.269990e3
    #s.z = 0.005870e3
    #s.Vx = -1.352148e3
    #s.Vy = 0.838718e3
    #s.Vz = 7.424009e3

    PositionList_Earth_is_point_Euler = open("PositionList_Earth_is_point_Euler_dt=" + str(dt) + ".txt", 'w')
    PositionList_Earth_is_point_Euler.truncate()
    PositionList_Earth_is_point_Euler.write("t x y z E L\n")
    #PositionList_Earth_is_point_Euler.write("0 0 0 0 0 0\n")

    #delta = open("delta_Euler_dt=" + str(dt) + ".txt", 'w')
    #delta.write("v_euler roK roI D_euler\n")
    #delta.truncate()

    while t <= time:
        a = -G * M / s.ro / s.ro
        a_x = a * s.x / s.ro
        a_y = a * s.y / s.ro
        a_z = a * s.z / s.ro

        s.Vx += a_x * dt
        s.Vy += a_y * dt
        s.Vz += a_z * dt

        s.x += s.Vx*dt
        s.y += s.Vy*dt
        s.z += s.Vz*dt

        t += dt
        s.update()

        if int(t/dt) % 10 == 0:
            #ax.scatter(s.x, s.y, s.z, s=2)
            print(t)
            #line = str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(s.Vx) + " " + str(s.Vy) + " " + str(s.Vz) + "\n"
            E = s.m * (s.Vx**2 + s.Vy**2 + s.Vz**2) / 2 - G * M * s.m / s.ro
            L = sqrt((s.y * s.Vz - s.z * s.Vy)**2 + (s.z * s.Vx - s.x * s.Vz)**2 + (s.x * s.Vy - s.y * s.Vx)**2) * s.m
            line = str(t) + " " + str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(E) + " " + str(L) + "\n"
            PositionList_Earth_is_point_Euler.write(line)

            #ex = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.x - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vx/(-Mu)
            #ey = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.y - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vy/(-Mu)
            #ez = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.z - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vz/(-Mu)
#
            #cosv = (ex*s.x+ey*s.y+ez*s.z)/(ex**2 + ey**2 + ez**2)**0.5/s.ro
            #ro = s.a * (1 - s.e**2) / (1 + s.e * cosv)
            #line = str(acos(cosv)) + " " + str(ro) + " " + str(s.ro) + " " + str(s.ro - ro) + " " + "\n"
            #delta.write(line)

    PositionList_Earth_is_point_Euler.close()
    #delta.close()


#Solving Newton's eq. using Adam's method with gaining first points through RK4#
def Earth_is_point_Adams(s: satellite, time):
    M = 5.97219E24
    G = 6.67384E-11
    t = 0
    dt = 10
    j = 0
    Mu = - G * M

    PositionList_Earth_is_point_Adams = open("PositionList_Earth_is_point_Adams_dt=" + str(dt) + ".txt", 'w')
    PositionList_Earth_is_point_Adams.truncate()
    PositionList_Earth_is_point_Adams.write("t x y z E L\n")
    #PositionList_Earth_is_point_Adams.write("0 0 0 0 0 0\n")

    #delta = open("delta_Adams_dt=" + str(dt) + ".txt", 'w')
    #delta.write("v_adams roK roI D_Adams\n")
    #delta.truncate()

    ax_list, ay_list, az_list = [], [], []
    Vx_list, Vy_list, Vz_list = [], [], []
    s.update()

    k1, k2, k3, k4 = [0]*3, [0]*3, [0]*3, [0]*3
    l1, l2, l3, l4 = [0]*3, [0]*3, [0]*3, [0]*3
    V = [s.Vx, s.Vy, s.Vz]
    x = [s.x, s.y, s.z]

    while j < 5:
        ro = sqrt(x[0]**2 + x[1]**2 + x[2]**2)
        for i in range(3):
            k1[i] = dt * (Mu * x[i] / ro**3)
            l1[i] = dt * (V[i])

        ro = sqrt((x[0] + 1/2.0 * l1[0])**2 + (x[1] + 1/2.0 * l1[1])**2 + (x[2] + 1/2.0 * l1[2])**2)
        for i in range(3):
            k2[i] = dt * (Mu * (x[i] + 1/2.0 * l1[i]) / ro**3)
            l2[i] = dt * (V[i] + 1/2.0 * k1[i])

        ro = sqrt((x[0] + 1/2.0 * l2[0])**2 + (x[1] + 1/2.0 * l2[1])**2 + (x[2] + 1/2.0 * l2[2])**2)
        for i in range(3):
            k3[i] = dt * (Mu * (x[i] + 1/2.0 * l2[i]) / ro**3)
            l3[i] = dt * (V[i] + 1/2.0 * k2[i])

        ro = sqrt((x[0] + l3[0])**2 + (x[1] + l3[1])**2 + (x[2] + l3[2])**2)
        for i in range(3):
            k4[i] = dt * (Mu * (x[i] + l3[i]) / ro**3)
            l4[i] = dt * (V[i] + k3[i])

        for i in range(3):
            V[i] += 1 / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
            x[i] += 1 / 6.0 * (l1[i] + 2 * l2[i] + 2 * l3[i] + l4[i])

        t += dt
        s.x = x[0]
        s.y = x[1]
        s.z = x[2]
        s.Vx = V[0]
        s.Vy = V[1]
        s.Vz = V[2]
        s.update()

        a = -G * M / s.ro**2
        a_x = a * s.x / s.ro
        a_y = a * s.y / s.ro
        a_z = a * s.z / s.ro

        ax_list.append(a_x)
        ay_list.append(a_y)
        az_list.append(a_z)

        Vx_list.append(s.Vx)
        Vy_list.append(s.Vy)
        Vz_list.append(s.Vz)

        t += dt
        s.update()
        j += 1

        if int(time/dt) % 20 == 0:
            #ax.scatter(s.x, s.y, s.z, s=2)
            print(t)
            #line = str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(s.Vx) + " " + str(s.Vy) + " " + str(s.Vz) + "\n"
            E = s.m * (s.Vx**2 + s.Vy**2 + s.Vz**2) / 2 - G * M * s.m / s.ro
            L = sqrt((s.y * s.Vz - s.z * s.Vy)**2 + (s.z * s.Vx - s.x * s.Vz)**2 + (s.x * s.Vy - s.y * s.Vx)**2) * s.m
            line = str(t) + " " + str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(E) + " " + str(L) + "\n"
            PositionList_Earth_is_point_Adams.write(line)

    while t < time:

        s.Vx += (1901/720 * ax_list[-1] - 1387/360 * ax_list[-2] + 109/30 * ax_list[-3] - 637/360 * ax_list[-4] + 251/720 * ax_list[-5]) * dt
        s.x  += (1901/720 * Vx_list[-1] - 1387/360 * Vx_list[-2] + 109/30 * Vx_list[-3] - 637/360 * Vx_list[-4] + 251/720 * Vx_list[-5]) * dt

        s.Vy += (1901/720 * ay_list[-1] - 1387/360 * ay_list[-2] + 109/30 * ay_list[-3] - 637/360 * ay_list[-4] + 251/720 * ay_list[-5]) * dt
        s.y  += (1901/720 * Vy_list[-1] - 1387/360 * Vy_list[-2] + 109/30 * Vy_list[-3] - 637/360 * Vy_list[-4] + 251/720 * Vy_list[-5]) * dt

        s.Vz += (1901/720 * az_list[-1] - 1387/360 * az_list[-2] + 109/30 * az_list[-3] - 637/360 * az_list[-4] + 251/720 * az_list[-5]) * dt
        s.z  += (1901/720 * Vz_list[-1] - 1387/360 * Vz_list[-2] + 109/30 * Vz_list[-3] - 637/360 * Vz_list[-4] + 251/720 * Vz_list[-5]) * dt

        t += dt
        s.update()

        a = -G * M / s.ro**2
        a_x = a * s.x / s.ro
        a_y = a * s.y / s.ro
        a_z = a * s.z / s.ro

        ax_list.append(a_x)
        ax_list.pop(0)
        Vx_list.append(s.Vx)
        Vx_list.pop(0)

        ay_list.append(a_y)
        ay_list.pop(0)
        Vy_list.append(s.Vy)
        Vy_list.pop(0)

        az_list.append(a_z)
        az_list.pop(0)
        Vz_list.append(s.Vz)
        Vz_list.pop(0)

        if int(t/dt) % 20 == 0:
            #ax.scatter(s.x, s.y, s.z, s=2)
            print(t)
            #line = str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(s.Vx) + " " + str(s.Vy) + " " + str(s.Vz) + "\n"
            E = s.m * (s.Vx**2 + s.Vy**2 + s.Vz**2) / 2 - G * M * s.m / s.ro
            L = sqrt((s.y * s.Vz - s.z * s.Vy)**2 + (s.z * s.Vx - s.x * s.Vz)**2 + (s.x * s.Vy - s.y * s.Vx)**2) * s.m
            line = str(t) + " " + str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(E) + " " + str(L) + "\n"
            PositionList_Earth_is_point_Adams.write(line)

            #ex = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.x - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vx/(-Mu)
            #ey = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.y - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vy/(-Mu)
            #ez = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.z - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vz/(-Mu)
#
            #cosv = (ex*s.x+ey*s.y+ez*s.z)/(ex**2 + ey**2 + ez**2)**0.5/s.ro
            #ro = s.a * (1 - s.e**2) / (1 + s.e * cosv)
            #line = str(acos(cosv)) + " " + str(ro) + " " + str(s.ro) + " " + str(s.ro - ro) + " " + "\n"
            #delta.write(line)



    PositionList_Earth_is_point_Adams.close()
    #delta.close()


#Solving Newton's eq. using RK4 method#
def RK4(s: satellite, time):
    M = 5.97219E24
    G = 6.67384E-11

    Mu = - G * M

    t = 0
    dt = 20
    i = 0
    PositionList_RK4 = open("RK4_dt=" + str(dt) + ".txt", 'w')
    PositionList_RK4.truncate()
    PositionList_RK4.write("t x y z E L\n")
    #PositionList_RK4.write("0 0 0 0 0 0\n")

    #delta = open("delta_RK4_dt=" + str(dt) + ".txt", 'w')
    #delta.write("v_RK4 roK roI D_RK4\n")
    #delta.truncate()

    #s.x = 261.861150e3
    #s.y = 7061.175000e3
    #s.z = 0.002510e3
    #s.Vx = 1.588904e3
    #s.Vy = -0.062803e3
    #s.Vz = 7.439352e3

    k1, k2, k3, k4 = [0]*3, [0]*3, [0]*3, [0]*3
    l1, l2, l3, l4 = [0]*3, [0]*3, [0]*3, [0]*3
    V = [s.Vx, s.Vy, s.Vz]
    x = [s.x, s.y, s.z]
    while t <= time:
        ro = sqrt(x[0]**2 + x[1]**2 + x[2]**2)
        for i in range(3):
            k1[i] = dt * (Mu * x[i] / ro**3)
            l1[i] = dt * (V[i])

        ro = sqrt((x[0] + 1/2.0 * l1[0])**2 + (x[1] + 1/2.0 * l1[1])**2 + (x[2] + 1/2.0 * l1[2])**2)
        for i in range(3):
            k2[i] = dt * (Mu * (x[i] + 1/2.0 * l1[i]) / ro**3)
            l2[i] = dt * (V[i] + 1/2.0 * k1[i])

        ro = sqrt((x[0] + 1/2.0 * l2[0])**2 + (x[1] + 1/2.0 * l2[1])**2 + (x[2] + 1/2.0 * l2[2])**2)
        for i in range(3):
            k3[i] = dt * (Mu * (x[i] + 1/2.0 * l2[i]) / ro**3)
            l3[i] = dt * (V[i] + 1/2.0 * k2[i])

        ro = sqrt((x[0] + l3[0])**2 + (x[1] + l3[1])**2 + (x[2] + l3[2])**2)
        for i in range(3):
            k4[i] = dt * (Mu * (x[i] + l3[i]) / ro**3)
            l4[i] = dt * (V[i] + k3[i])

        for i in range(3):
            V[i] += 1 / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
            x[i] += 1 / 6.0 * (l1[i] + 2 * l2[i] + 2 * l3[i] + l4[i])

        t += dt
        s.x = x[0]
        s.y = x[1]
        s.z = x[2]
        s.Vx = V[0]
        s.Vy = V[1]
        s.Vz = V[2]
        s.update()

        if int(t/dt) % 10 == 0:
            #ax.scatter(s.x, s.y, s.z, s=2)
            print(t)
            #line = str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(s.Vx) + " " + str(s.Vy) + " " + str(s.Vz) + "\n"
            E = s.m * (s.Vx**2 + s.Vy**2 + s.Vz**2) / 2 - G * M * s.m / s.ro
            L = sqrt((s.y * s.Vz - s.z * s.Vy)**2 + (s.z * s.Vx - s.x * s.Vz)**2 + (s.x * s.Vy - s.y * s.Vx)**2) * s.m
            line = str(t) + " " + str(s.x) + " " + str(s.y) + " " + str(s.z) + " " + str(E) + " " + str(L) + "\n"
            PositionList_RK4.write(line)

            #ex = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.x - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vx/(-Mu)
            #ey = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.y - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vy/(-Mu)
            #ez = (s.Vx**2 + s.Vy**2 + s.Vz**2 + Mu/s.ro)/(-Mu) * s.z - (s.x*s.Vx + s.y*s.Vy + s.z*s.Vz)*s.Vz/(-Mu)
#
            #cosv = (ex*s.x+ey*s.y+ez*s.z)/(ex**2 + ey**2 + ez**2)**0.5/s.ro
            #ro = s.a * (1 - s.e**2) / (1 + s.e * cosv)
            #line = str(acos(cosv)) + " " + str(ro) + " " + str(s.ro) + " " + str(s.ro - ro) + " " + "\n"
            #delta.write(line)

    PositionList_RK4.close()
    #delta.close()


s = satellite(66.2708, 40.5433, 0.8019403, 93.5771, 359.9354, 0.50315154, 3800)
#s = Get_Descartes_data(s)
s.update()

#Kepler_solver(s)
#Earth_is_point_Euler(s, 60 * 60 * 48 * 20)
#Earth_is_point_Adams(s, 60 * 60 * 48 * 20)
RK4(s, 60 * 60 * 48 * 20)




