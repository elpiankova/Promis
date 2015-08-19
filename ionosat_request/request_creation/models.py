from django.db import models
from ionosat_request.settings import BASE_DIR
from request_creation.validators import *
import os

class Request(models.Model):
    UPWARD_ORBIT = 'v'
    DOWNWARD_ORBIT = 'n'
    ANY_ORBIT = 'p'
    ORBIT_FLAG = (
        (UPWARD_ORBIT, 'восходящая'),
        (DOWNWARD_ORBIT, 'нисходящая'),
        (ANY_ORBIT, 'не имеет значения'),
    )
    number = models.SmallIntegerField(validators=[request_max_number_validator], unique=True)
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

    device_amount = models.SmallIntegerField(null=True, validators=[device_amount_max_val_validator,
                                                         device_amount_min_val_validator])
    request_file = models.FilePathField(path=os.path.join(BASE_DIR, 'request_files'),
                                        validators=[request_file_validator], null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    total_data_amount = models.BigIntegerField(default=0)
    total_power_amount = models.FloatField(default=0)


##  device_switch_list = models.ManyToManyField('DeviceSwitch')

    class Meta:
        db_table = 'requests'

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        self.clean_fields()
        super(Request, self).save(*args, **kwargs)

class Device(models.Model):
    # WP0000 = 'Wave probe WP(count3)'
    # EP0000 = 'Electric  probe'
    # RFA000 = 'Radio frequency analyser'
    # DN0000 = 'Neutral component plasma probe'
    # DE0000 = 'Electric component plasma probes'
    # FGM000 = 'Flux-Gate magnetometer constant field'
    # PES000 = 'Total electron content'
    # SSNI00 = 'System for gathering scientific information'
    # PROBES = (
    #     (WP0000, ''),
    #     (EP0000, 'Electric probe'),
    #     (RFA000, 'Radio frequency analyser'),
    #     (DN0000, 'Neutral component plasma probe'),
    #     (DE0000, 'Electric component plasma probes'),
    #     (FGM000, 'Flux-Gate magnetometer constant field'),
    #     (PES000, 'Total electron content'),
    #     (SSNI00, 'System for gathering scientific information'),
    # )
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'devices'

    def __str__(self):
        return self.name

class DeviceMode(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    power = models.FloatField(default=0)
    data_speed = models.IntegerField(default=0)
    device = models.ForeignKey('Device', related_name='modes')

    class Meta:
        db_table = 'device_modes'
        unique_together = ("device", "name")

    def __str__(self):
        return self.name

class DeviceSwitch(models.Model):
    argument_part_len = models.SmallIntegerField() #limit duration in validator 10
    time_delay = models.DurationField() #limit duration in validator
    time_duration = models.DurationField()
    argument_part = models.CharField(max_length=620, blank=True, null=True)
    device = models.ForeignKey('Device')
    mode = models.ForeignKey('DeviceMode') #limit to choice to
    request = models.ForeignKey('Request', related_name='switches') # limit to choice
    data_amount = models.BigIntegerField(default=0)
    power_amount = models.FloatField(default=0)

    class Meta:
        db_table = 'device_switches'
        unique_together = ("device", "request")

    def __str__(self):
        return str(self.time_duration)