from django.db import models
from ionosat_request.settings import BASE_DIR

class Request(models.Model):
    UPWARD_ORBIT = 'y'
    DOWNWARD_ORBIT = 'n'
    ANY_ORBIT = 'p'
    ORBIT_FLAG = (
        (UPWARD_ORBIT, 'upward'),
        (DOWNWARD_ORBIT, 'downward'),
        (ANY_ORBIT, 'any'),
    )
    orbit_flag = models.CharField(max_length=1, choices=ORBIT_FLAG, default=ANY_ORBIT)
    number = models.CharField(max_length=4)
    date_start = models.DateField()
    date_end = models.DateField()
    latitude_start = models.DecimalField(max_digits=3, decimal_places=1)
    longitude_left = models.DecimalField(max_digits=4, decimal_places=1)
    longitude_right = models.DecimalField(max_digits=4, decimal_places=1)
    device_amount = models.SmallIntegerField()
    device_switch_list = models.ManyToManyField('DeviceSwitch')
    request_file = models.FilePathField(path=BASE_DIR+'/request_files')
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'requests'

    def __str__(self):
        return self.number

class Device(models.Model):
    device_name = models.CharField(max_length=255)
    device_code = models.CharField(max_length=6)
    device_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'devices'

    def __str__(self):
        return self.device_name

class DeviceMode(models.Model):
    mode_name = models.CharField(max_length=255)
    mode_code = models.CharField(max_length=6)
    device = models.ForeignKey('Device')

    class Meta:
        db_table = 'device_modes'

    def __str__(self):
        return self.mode_name

class DeviceSwitch(models.Model):
    argument_part_len = models.SmallIntegerField() #limit duration in validator 10
    time_delay = models.DurationField() #limit duration in validator
    time_duration = models.DurationField()
    argument_part = models.CharField(max_length=620)
    device = models.ForeignKey('Device')
    mode = models.ForeignKey('DeviceMode') # limit to choice to

    class Meta:
        db_table = 'device_switches'

    def __str__(self):
        return self.time_duration
# Create your models here.
