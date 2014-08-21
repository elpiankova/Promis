from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
m = Basemap(projection='cyl', lat_0=50, lon_0=10, resolution='l')

    
m.drawparallels(np.arange(-90.,90.,90.))
m.drawmeridians(np.arange(-180.,180.,60.))
#m.etopo()
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='coral')
m.drawmapboundary()
# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
date = datetime.utcnow()
CS=m.nightshade(date)

plt.show()