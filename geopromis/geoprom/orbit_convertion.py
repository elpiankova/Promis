import numpy as np

class PlacePoint(object):
    """This is base class for measurements points. Agregation xyz and lat,long"""
    def __init__(self, rx_ifr,ry_ifr,rz_ifr):
        super(PlacePoint, self).__init__()
        self.rx_ifr = rx_ifr
        self.ry_ifr = ry_ifr
        self.rz_ifr = rz_ifr
        self.cart_to_spheric()
        
    def cart_to_spheric(self):
        """This function convert cartesian coor system to spherical"""
        R0 = pow((self.rx_ifr**2+self.ry_ifr**2+self.rz_ifr**2),0.5)
        sinfi = self.rz_ifr/R0
        cosfi = pow((self.rx_ifr**2+self.ry_ifr**2),0.5)/R0
        sinlambda = self.ry_ifr/pow(self.rx_ifr**2+self.ry_ifr**2,0.5)
        coslambda = self.rx_ifr/pow(self.rx_ifr**2+self.ry_ifr**2,0.5)
        tanfi = sinfi/cosfi
        tanlambda = sinlambda/coslambda
        self.latitude = 180*(np.arctan(tanfi))/np.pi
        self.longitude = 180*(np.arctan2(sinlambda, coslambda))/np.pi
        self.lonlat = (self.longitude, self.latitude)