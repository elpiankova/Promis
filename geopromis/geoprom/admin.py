from django.contrib.gis import admin
from geoprom.models import Session, Satellite

admin.site.register(Session, admin.GeoModelAdmin)
admin.site.register(Satellite, admin.GeoModelAdmin)