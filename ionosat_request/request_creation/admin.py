from django.contrib import admin
from .models import Device, DeviceMode, Request

admin.site.register(Device)
admin.site.register(DeviceMode)
admin.site.register(Request)
# Register your models here.
