#from django.contrib import admin
from django.contrib.gis import admin
from geoprom.models import Session, Satellite

#admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(Session, admin.GeoModelAdmin)
admin.site.register(Satellite, admin.GeoModelAdmin)
#admin.site.register(FrameWindow, admin.GeoModelAdmin)
# Register your models here.
