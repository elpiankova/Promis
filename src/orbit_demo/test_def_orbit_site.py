# -*- coding: utf-8 -*- 
from math import pi, cos, sin, sqrt, atan2

# This script calculate coordinate points for 
# generation array of coordinate for every satellite revolutions.
# Initial data for this are "Orbital elements". 

# Orbital elements
T0 = 2456896.500000000                     #(Julian day number), epochal time
n = 6.457576287408390e-02                  # (degrees/sec), the angular speed of the spacecraft
e = 1.637994365076186e-03                  # eccentricity
eps = 0.0000001                            # error
a = 6.795394080891185e+03                  #(km)semimajor axis
omega_big = 1.224602531823290e+02*pi/180   #(rad)
omega_small = 5.823934876750221e+01*pi/180 #(rad)
I = 6.198649551806115e+01*pi/180           #(rad) inclination
T = 2456896.507593647577                   #(Julian day number), present time

# Time data for calculating
time = 1000                               # (min) Calculation time
time_divider = 8                           # If time_divider = 1 => time discreteness = 1 min

# This class calculate arrays with coordinates
class CoordinatesArrayMaker:
    
    def __init__(self, T0, n, e, eps, a, omega_big, omega_small, I, T, time, time_divider):
        # Orbital elements
        self.T0 = T0
        self.n = n
        self.e = e
        self.eps = eps
        self.a = a
        self.omega_big = omega_big
        self.omega_small = omega_small
        self.I = I
        self.T = T
        # Time data 
        self.time = time                    # (min) Calculation time
        self.time_divider = time_divider    # If time_divider = 1 => time discreteness = 1 min
        # Initialization of arrays of coordinates
        self.Lon = []                       # Longitude array
        self.Lat = []                       # Latitude array
        
        self.coord_srt = 0

    # This function calculate initial arrays with coordinates    
    def coordinate_calculate(self):
        # Initial parameters
        i = 0
        # Coordinate calculation every point for "time"
        while i <= self.time:
            # Initial parameters for anomaly
            E = 0                   # Initialization of E parameter
            E0 = 0.5                # Random initial parameter of eccentric anomaly (E0)
            M = self.n*((self.T - self.T0)*24*3600)#(degrees) Mean anomaly
            # Calculation of Mean anomaly (М)
            while M*pi/180 > 2*pi:
                M = M - 360
        
            while M*pi/180 < 0:
                M = M + 360
    
            # Calculation of eccentric anomaly
            n1 = 1
            while abs(E-E0) > self.eps:
                E0 = E
                E = M + self.e*sin(E0)
                n1 += 1
    
            # Auxiliary Cartesian coordinates
            X0 = self.a*(cos(E*pi/180) - self.e)
            Y0 = self.a*sqrt(1-self.e**2)*sin(E*pi/180)
            Z0 = 0
            # Calculation of Cartesian coordinates for spacecraft
            X = (cos(self.omega_big)*cos(self.omega_small)-sin(self.omega_big)*cos(self.I)*sin(self.omega_small))*X0 - \
                (cos(self.omega_big)*sin(self.omega_small)+sin(self.omega_big)*cos(self.I)*cos(self.omega_small))*Y0 + \
                sin(self.omega_big)*sin(self.I)*Z0
            Y = (sin(self.omega_big)*cos(self.omega_small)+cos(self.omega_big)*cos(self.I)*sin(self.omega_small))*X0 - \
                (sin(self.omega_small)*sin(self.omega_big)-cos(self.omega_big)*cos(self.I)*cos(self.omega_small))*Y0 - \
                cos(self.omega_big)*sin(self.I)*Z0
            Z = sin(self.I)*sin(self.omega_small)*X0 + sin(self.I)*cos(self.omega_small)*Y0 + cos(self.I)*Z0
            # Transfer Cartesian coordinates to spherical coordinates
            fi = (180/pi)*atan2(Y, X) - 0.25*i/self.time_divider # Longitude
            teta = (180/pi)*atan2(Z, sqrt(X**2 + Y**2))     # Latitude
            # Additional procedure for coordinates
            if fi < -180:
                fi = 180 - (abs(fi) - 180)
            # Formation arrays with coordinates
            self.Lon.append(fi)
            self.Lat.append(teta)
            # Time increment for calculation
            i += 1
            self.T += 0.000694444/self.time_divider # time = 1/n min
    
        return self.Lat, self.Lon

    #This function return array of coordinate divided to revolutions
    def orbital_revolutions(self):
        # Initialization of additional arrays       
        Lon2 = []
        Lat2 = []
        # Arrays of coordinates
        self.coordinate_calculate()
        # Dividing arrays to revolutions
        while len(self.Lon) > 0:
                
            begin = 0
            end = 0
            end1 = 0
        
            for i in range(len(self.Lon)):
                if end == 0:
                    if self.Lon[i] > 0 and self.Lon[i] < 180:
                        end = i
                    else: pass
                else: pass

            Lon1 = self.Lon[end:]

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
                end1 = len(self.Lon)
                 
            end = end1 + end 
            
            Lon2.append(self.Lon[begin:end])
            Lat2.append(self.Lat[begin:end])
        
            self.Lon = self.Lon[end:]
            self.Lat = self.Lat[end:]
        # Final arrays with coordinates for each orbital revolution    
        self.Lon = Lon2
        self.Lat = Lat2
        
        return self.Lat, self.Lon

    #This function make array with pair of Lon and Lat for each orbital revolution
    def final_arrays_maker(self):
        # Arrays of coordinates
        self.orbital_revolutions()
        # Additional arrays of coordinates
        block_j = []
        block_i = []
        coordinatelane = []

        # Create pair of coordinate 
        for i in range(len(self.Lon)) and range(len(self.Lat)):   
            for j in range(len(self.Lon[i])) and range(len(self.Lat[i])):
                block_j.append(self.Lat[i][j])
                block_j.append(self.Lon[i][j])
                block_i.append(block_j)
                block_j = []
            coordinatelane.append(block_i)
            block_i = []
            
        self.coord_srt = coordinatelane

        return self.coord_srt
    
    def revolutions_dict(self):
        self.final_arrays_maker()
        
        D = {}
        j = 1
        
        for i in range(len(self.coord_srt)):
            D[j] = self.coord_srt[i]
            j += 1
        
        return D
    

arrays = CoordinatesArrayMaker(T0, n, e, eps, a, omega_big, omega_small, I, T, time, time_divider)
#print arrays.coordinate_calculate()
#print arrays.orbital_revolutions()
#print arrays.final_arrays_maker()
print arrays.revolutions_dict()
