from django.contrib.gis.db import models


class Satellite(models.Model):
    ''' Class representing an satellite
    This is the class storing the satellite title and description
    Satellite title must be unique
    '''
    title = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)
    date_start = models.DateField()
    date_end = models.DateField()
    owner = models.ForeignKey('auth.User', related_name='satellites')
    highlighted = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'satellites'
    
class Device(models.Model):
    ''' Class representing a scientific device of satellite
        that performs measurements

    This is the class storing the device title, description and satellite
    FOREIGN KEY `satellite_title`
    '''
    # Django creates the next field automatically:
    # id = models.IntegerField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    satellite = models.ForeignKey('Satellite', db_column='satellite_title', on_delete=models.PROTECT)

    def __str__(self):
        return u'%s of %s' % (self.title, self.satellite.title)

    class Meta:
        db_table = 'devices'
        # In future we want to have Multi-column primary key ("title","satellite_title")
        unique_together = (("title", "satellite"),)
        ordering = ["title"]

class ChannelManager(models.Manager):
    def get_by_natural_key(self, title, device_name):
        device = Device.objects.get(title=device_name)
        return self.get(title=title, device=device)

class Channel(models.Model):
    ''' Class representing measuring channels of devices

    This is the class storing the channel title, description and device
    FOREIGN KEY `device_id`
    MANY-TO-MANY REL: 'parameter_title'
                      'session_id'
    '''
    # Django creates the next field automatically:
    # id = models.IntegerField(max_length=10, primary_key=True)
    objects = ChannelManager()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sampling_frequency = models.FloatField(null=True, blank=True)
    device = models.ForeignKey('Device', on_delete=models.PROTECT)

    # Many-to-many relations:
    # parameters = models.ManyToManyField('Parameter', through = "ChannelsHaveParameters")
    sessions = models.ManyToManyField('Session', through="ChannelsHaveSessions")

    def __str__(self):
        return u'%s of %s device (%s)' % (self.title, self.device.title, self.device.satellite.title)

    class Meta:
        db_table = 'channels'
        # Django creates the next field automatically id as pk
        # But we want to have Multi-column primary key ("title","device") in future:
        unique_together = (("title", "device"),)
        ordering = ["title", "device"]


class ChannelOption(models.Model):
    ''' Class representing channel option
    FOREIGN KEY 'channel_id'
    '''
    # Django creates the next field automatically:
    # id = models.AutoField(primary_key=True)
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    value = models.CharField(max_length=45, null=True, blank=True, db_column='co_value')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.value == 0:
            return self.title
        return u'%s: %s' % (self.title, self.value)

    class Meta:
        db_table = 'channels_options'


class SessionManager(models.GeoManager):
    def get_by_natural_key(self, time_begin, time_end):
        return self.get(time_begin=time_begin, time_end=time_end)


class Session(models.Model):
    ''' Class representing session
    This is the class storing the begin and end time of session
    MANY-TO-MANY REL: 'session_id'
    '''
    # Django creates the next field automatically:
    # id = models.AutoField(primary_key=True)
    objects = SessionManager()
    code = models.CharField(max_length=6)
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()
    geo_line = models.MultiLineStringField()
    parameters = models.ManyToManyField('Parameter', through="SessionsHaveParameters")

    @property
    def time_interval(self):
        return " ".join([str(self.time_begin), str(self.time_end)])

    def __str__(self):
        return u'%s - %s' % (str(self.time_begin), str(self.time_end))

    class Meta:
        db_table = 'sessions'
        unique_together = (('time_begin', 'time_end', 'geo_line'),)
        ordering = ['time_begin', 'time_end', 'geo_line']


class SessionOption(models.Model):
    '''
    Class representing session option
    FOREIGN KEY 'session_id'
    '''
    # Django creates the next field automatically:
    # id = models.AutoField(primary_key=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True,
                             db_column='so_value')

    def __str__(self):
        if self.value == 0:
            return self.title
        return u'%s: %s' % (self.title, self.value)

    class Meta:
        db_table = 'sessions_options'


class ChannelsHaveSessions(models.Model):
    ''' Class representing MANY-TO-MANY relationship
        for Channels and Sessions
    '''
    channel = models.ForeignKey('Channel', related_name='+', on_delete=models.PROTECT)
    session = models.ForeignKey('Session', related_name='+', on_delete=models.PROTECT)

    def __str__(self):
        return u'channel: %s, session: %d' % (self.channel.title, self.session.id)

    class Meta:
        db_table = 'channels_have_sessions'
        unique_together = (("channel", "session"),)


class Parameter(models.Model):
    ''' Class representing measured parameter

    This is the class storing the parameter title and units
    MANY-TO-MANY REL: 'channels_id'
                      'parent_title' or/and 'child_title'
    '''
    title = models.CharField(max_length=255, primary_key=True)
    short_name = models.CharField(max_length=25)
    level = models.IntegerField()
    description = models.TextField(max_length=255, null=True, blank=True)
    units = models.ForeignKey('Units',
                              db_column='units_title',
                              on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'parameters'


class SessionsHaveParameters(models.Model):
    ''' Class representing MANY-TO-MANY relationship
        for Sessions and Parameters
    '''
    session = models.ForeignKey('Session', related_name='+', on_delete=models.PROTECT)
    parameter = models.ForeignKey('Parameter', related_name='+', on_delete=models.PROTECT)

    def __str__(self):
        return u'session: %s, parameter: %s' % (self.session.id, self.parameter.title)

    class Meta:
        db_table = 'sessions_have_parameters'
        unique_together = (("session", "parameter"),)



class Units(models.Model):
    ''' Class representing parameter units

    This is the class storing the unique title, short name, long name and
    description of units
    '''
    title = models.CharField(max_length=255, primary_key=True)
    short_name = models.CharField(max_length=45)
    long_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'units'
        verbose_name_plural = 'units'


class ParentChildRel(models.Model):
    ''' Class representing Parent-Child relationship for parameters

    This class shows ....
    '''
    parent = models.ForeignKey('Parameter', db_column='parent_title',
                               related_name='parent+', on_delete=models.PROTECT,)

    child = models.ForeignKey('Parameter', db_column='child_title',
                               related_name='child+', on_delete=models.PROTECT,)

    def __str__(self):
        return u'parent: %s, child: %s' % (self.parent.title, self.child.title)

    class Meta:
        db_table = 'parameters_have_parameters'
        unique_together = (("parent", "child"),)

'''
class FrameWindow(models.Model):
    
    name = models.CharField(max_length=20)
    poly = models.PolygonField()
    objects = models.GeoManager()

    def __str__(self):
        return self.name
'''