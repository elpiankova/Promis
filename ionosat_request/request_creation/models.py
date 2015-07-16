from django.db import models
from ionosat_request.settings import BASE_DIR
from request_creation.validators import *


class Request(models.Model):
    UPWARD_ORBIT = 'y'
    DOWNWARD_ORBIT = 'n'
    ANY_ORBIT = 'p'
    ORBIT_FLAG = (
        (UPWARD_ORBIT, 'upward'),
        (DOWNWARD_ORBIT, 'downward'),
        (ANY_ORBIT, 'any'),
    )
    number = models.SmallIntegerField(validators=[request_max_number_validator])
    date_start = models.DateField()
    date_end = models.DateField()
    orbit_flag = models.CharField(max_length=1, choices=ORBIT_FLAG, default=ANY_ORBIT)
    latitude_start = models.DecimalField(max_digits=3, decimal_places=1,
                                         validators=[request_max_latitude_start_validator,
                                                     request_min_latitude_start_validator])
    longitude_left = models.DecimalField(max_digits=4, decimal_places=1,
                                         validators=[request_max_longitude_validator,
                                                     request_min_longitude_validator])
    longitude_right = models.DecimalField(max_digits=4, decimal_places=1,
                                          validators=[request_max_longitude_validator,
                                                      request_min_longitude_validator])

    device_amount = models.SmallIntegerField(validators=[device_amount_max_val_validator,
                                                         device_amount_min_val_validator])
    request_file = models.FilePathField(path=BASE_DIR+'/request_files', validators=[request_file_validator])
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
##  device_switch_list = models.ManyToManyField('DeviceSwitch')

    class Meta:
        db_table = 'requests'

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        self.clean_fields()
        super(Request, self).save(*args, **kwargs)

class Device(models.Model):
    WP0000 = 'Wave probe WP(count3)'
    EP0000 = 'Electric  probe'
    RFA000 = 'Radio frequency analyser'
    DN0000 = 'Neutral component plasma probe'
    DE0000 = 'Electric component plasma probes'
    FGM000 = 'Flux-Gate magnetometer constant field'
    PES000 = 'Total electron content'
    SSNI00 = 'System for gathering scientific information'
    PROBES = (
        (WP0000, 'Wave probe WP(count3)'),
        (EP0000, 'Electric  probe'),
        (RFA000, 'Radio frequency analyser'),
        (DN0000, 'Neutral component plasma probe'),
        (DE0000, 'Electric component plasma probes'),
        (FGM000, 'Flux-Gate magnetometer constant field'),
        (PES000, 'Total electron content'),
        (SSNI00, 'System for gathering scientific information'),
    )
    name = models.CharField(max_length=255, choices=PROBES)
    code = models.CharField(max_length=6)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'devices'

    def __str__(self):
        return self.name

class DeviceMode(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    device = models.ForeignKey('Device', related_name='modes')

    class Meta:
        db_table = 'device_modes'

    def __str__(self):
        return self.name

class DeviceSwitch(models.Model):
    argument_part_len = models.SmallIntegerField() #limit duration in validator 10
    time_delay = models.DurationField() #limit duration in validator
    time_duration = models.DurationField()
    argument_part = models.CharField(max_length=620)
    device = models.ForeignKey('Device')
    mode = models.ForeignKey('DeviceMode') # limit to choice to
    request = models.ForeignKey('Request', related_name='switches') # limit to choice

    class Meta:
        db_table = 'device_switches'

    def __str__(self):
        return self.time_duration
# Create your models here.

