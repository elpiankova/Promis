from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
m = Basemap(projection='cyl',
            resolution=None, llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
# draw a land-sea mask for a map background.
# lakes=True means plot inland lakes with ocean color.
#m.drawlsmask(land_color='coral',ocean_color='aqua')

lons = 0
lats = 0
i = 0
#for i in [1,2,3,4,5]:
while i < 20:
    xx, yy = m(lons, lats)
    #m.scatter(x,y,10,marker='o',color='r')
    m.plot(xx,yy,linewidth=1.5,color='r')
    lons += 4
    lats += 4
    i += 1
        
    
m.drawparallels(np.arange(-90.,90.,90.))
m.drawmeridians(np.arange(-180.,180.,60.))
m.etopo()


plt.show()