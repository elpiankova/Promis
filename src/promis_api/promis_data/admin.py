from django.contrib import admin
from promis_data.models import Satellite, Device, Channel, Parameter, Units, ChannelsHaveParameters, ChannelOption

#class DeviceAdmin(admin.ModelAdmin):
#    fieldsets =[
#        (None, {'fields': ['title']}),
#        (None, {'fields': ['description'], 'classes': ['collapse']}),
#    ]

class DeviceInline(admin.TabularInline):
    model = Device
    
    
class SatelliteAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    inlines = [DeviceInline]
    list_display = ('title',)
    search_fields = ['title']

admin.site.register(Satellite, SatelliteAdmin)

class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 1
    
class DeviceAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'satellite']
    inlines = [ChannelInline]
    list_display = ('title', 'satellite')
    search_fields = ['title']

admin.site.register(Device, DeviceAdmin)

class ChannelParameterInline(admin.TabularInline):
    model = Channel.parameters.through
    extra = 1
    
#class ChannelSessionInline(admin.TabularInline):
#    model = Channel.sessions.through
#    extra = 1
    
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'device', )
    search_fields = ['title', 'device']
    ordering = ('title',)
    inlines = [
        ChannelParameterInline,
#        ChannelSessionInline,
    ]
admin.site.register(Channel, ChannelAdmin)

class ChannelOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'channel')
    
admin.site.register(ChannelOption, ChannelOptionAdmin)
admin.site.register(Parameter)
admin.site.register(Units)

class ChannelsHaveParemAdmin(admin.ModelAdmin):
    list_display = ('channel', 'parameter')
admin.site.register(ChannelsHaveParameters, ChannelsHaveParemAdmin)
