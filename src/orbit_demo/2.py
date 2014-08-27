from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
 
# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
map = Basemap(projection='cyl', lat_0=50, lon_0=50,
              resolution='l', area_thresh=1000.0)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='coral')
map.drawmapboundary()

map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

lats = [53.5519317,53.8758499, 54.2894659, 55.2333142, 
54.9846137,54.7064869, 51.5296651, 51.5536226, 51.7653115, 52.1625237, 
52.5809163, 52.9393892]

lons = [-9.9413447, -9.9621948, -8.9583439, -7.6770179, -8.3771698, 
-8.7406732, -8.9529546, -9.7907148, -10.1531573, -10.4099873, 
-9.8456417, -9.4344939]

x, y = map(lons, lats)
#for i in range(len(lons)):
#     for j in range(len(lons)):
#         if i == j: continue
#         map.plot([x[i],y[i]],[x[j],y[j]],'b')

map.plot(x, y, 'D-', markersize=10, linewidth=2, color='k', markerfacecolor='b')
 
plt.show()