from __future__ import unicode_literals

from django.db import models


class Satellite(models.Model):
    ''' Class representing an satellite 
    This is the class storing the satellite name and description
    Satellite name must be unique    
    '''
    title = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        db_table = 'satellites' # 'promis_satellites'
        
        
class Device(models.Model):
    ''' Class representing a scientific device of satellite 
        that performs measurements
        
    This is the class storing the device name, description and satellite 
    FOREIGN KEY `satellite_title` 
    '''
    #Django creates the next field automatically:
    #id = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    satellite   = models.ForeignKey('Satellite', db_column='satellite_title',
                                    on_delete=models.PROTECT)
                                    # Andrew, does it correspond to ON DELETE RESTRICT???
    
    def __unicode__(self):
        return u'%s of %s' % (self.title, self.satellite.title)
    class Meta:
        db_table = 'devices'
        #In future we want to have Multi-column primary key ("title","satellite_title")
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
    #Django creates the next field automatically:
    #id = models.AutoField(primary_key=True)
    objects = ChannelManager()
    title              = models.CharField(max_length=255)
    description        = models.TextField(blank=True)
    #sampling_frequency = models.FloatField(null=True, blank=True)
    #frequency_range    = models.CharField(max_length=100, blank=True)
    device = models.ForeignKey('Device', on_delete=models.PROTECT)
    
    #Many-to-many relations:
    parameters = models.ManyToManyField('Parameter', through = "ChannelsHaveParameters")
    sessions = models.ManyToManyField('Session', through = "ChannelsHaveSessions")
    
    def __unicode__(self):
        return u'%s of %s device (%s)' % (self.title, self.device.title, self.device.satellite.title)  
    class Meta:
        db_table = 'channels'
        #Django creates the next field automatically id as pk
        #But we want to have Multi-column primary key ("title","device") in future:
        unique_together = (("title", "device"),)
        ordering = ["title", "device"]


class ChannelOption(models.Model):
    ''' Class representing channel option
    FOREIGN KEY 'channel_id'
    '''    
    #Django creates the next field automatically:
    #id = models.AutoField(primary_key=True)
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    title   = models.CharField(max_length=255)
    value   = models.CharField(max_length=255, null=True, blank=True,
                               db_column='co_value')
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        if self.value==0:
            return self.title
        return u'%s: %s' % (self.title, self.value)
    class Meta:
        db_table = 'channels_options'


class ChannelsHaveParameters(models.Model):
    ''' Class representing MANY-TO-MANY relationship 
        for Channels and Parameters
    '''
    channel   = models.ForeignKey('Channel', on_delete=models.PROTECT,
                                  related_name='+')
    parameter = models.ForeignKey('Parameter', db_column='parameter_title',
                                  related_name='+', on_delete=models.PROTECT,)
    
    def __unicode__(self):
        return u'channel: %s, parameter: %s' % (self.channel.title, self.parameter.title)
    class Meta:
        db_table = 'channels_have_parameters'
        unique_together = (("channel", "parameter"),)
        verbose_name_plural = 'Channels have Parameters'


class ChannelsHaveSessions(models.Model):
    ''' Class representing MANY-TO-MANY relationship 
        for Channels and Sessions
    '''
    channel = models.ForeignKey('Channel', related_name='+', on_delete=models.PROTECT)
    session = models.ForeignKey('Session', related_name='+', on_delete=models.PROTECT)
    
    def __unicode__(self):
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
    short_name = models.CharField(max_length=45)
    description = models.TextField(null=True, blank=True)
    units = models.ForeignKey('Units', 
                              db_column='units_title', 
                              on_delete=models.PROTECT)
    
    parents = models.ManyToManyField(
        'self', 
        through = 'ParentChildRel',
        symmetrical = False, 
        related_name = 'children'
    )
    
    def __unicode__(self):
        return self.title
    class Meta:
        db_table = 'parameters'


class ParentChildRel(models.Model):
    ''' Class representing Parent-Child relationship for parameters
    
    This class shows ....
    '''
    parent = models.ForeignKey('Parameter', db_column='parent_title',
                               related_name = 'parent+', on_delete=models.PROTECT,
                               )
    child  = models.ForeignKey('Parameter', db_column='child_title',
                               related_name = 'child+', on_delete=models.PROTECT,
                               )
    def __unicode__(self):
        return u'parent: %s, child: %s' % (self.parent.title, self.child.title)
    class Meta:
        db_table = 'parameters_have_parameters'
        unique_together = (("parent", "child"),)


class SessionManager(models.Manager):
    def get_by_natural_key(self, time_begin, time_end):
        return self.get(time_begin=time_begin, time_end=time_end)


class Session(models.Model):
    ''' Class representing session
        
    This is the class storing the begin and end time of session 
    MANY-TO-MANY REL: 'session_id'
    '''    
    #Django creates the next field automatically:
    #id = models.AutoField(primary_key=True)
    objects = SessionManager()
    
    time_begin = models.DateTimeField()
    time_end   = models.DateTimeField()
    
    @property
    def time_interval(self):
        return " ".join([str(self.time_begin), str(self.time_end)])
    
    def __unicode__(self):
        return u'%s - %s' % (str(self.time_begin), str(self.time_end))
    class Meta:
        db_table = 'sessions'
        unique_together = (('time_begin', 'time_end'),)
        ordering = ['time_begin', 'time_end']


class SessionOption(models.Model):
    ''' Class representing session option
    FOREIGN KEY 'session_id'
    '''    
    #Django creates the next field automatically:
    #id = models.AutoField(primary_key=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    title   = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True, 
                             db_column='so_value')
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        if self.value==0:
            return self.title
        return u'%s: %s' % (self.title, self.value)
    class Meta:
        db_table = 'sessions_options'


class MeasurementPointManager(models.Manager):
    def get_by_natural_key(self, time):
        from dateutil import parser as dateutil_parser
        time = dateutil_parser.parse(time)
        return self.get(time=time)


class MeasurementPoint(models.Model):
    ''' Class representing measurement point that is characterized by time point
        and (optional) space point 
        
    This is the class storing the time point and optional geographic coordinates: 
    x_geo, y_geo, z_geo
    FOREIGN KEY `sessions_id`
    '''
    #Django creates the next field automatically:
    #id = models.AutoField(primary_key=True)

    #We want BigAutoFiled here. Now it doesn't work. 
    # I, O.P, should try it in TRUNK version of Django    
    #id = models.BigAutoField(primary_key=True)
    objects = MeasurementPointManager()
    
    time  = models.DateTimeField(unique=True)
    x_geo = models.FloatField(null=True, blank=True)
    y_geo = models.FloatField(null=True, blank=True)
    z_geo = models.FloatField(null=True, blank=True)
#    session   = models.ForeignKey('Session', on_delete=models.PROTECT)
        
    def __unicode__(self):
        return unicode(self.time)
    class Meta:
        db_table = 'measurement_points'


class Measurement(models.Model):
    ''' Class representing measurement
        
    This is the class storing the measurement value, level of processing,
    relative error and relationships with parameter, channel and measurement point
    FOREIGN KEY `parameter_title`,
                `channel_id`,
                `measurement_point_id`
    '''
    #Django creates the next field automatically:
    #id = models.AutoField(primary_key=True)
    #We want BigAutoFiled here that was fixed 3 month ago in TRUNK version of Django
    # I, O.P, should try it in TRUNK version of Django    
    #id = models.BigAutoField(primary_key=True)
    level_marker   = models.IntegerField()
    measurement    = models.FloatField()
    relative_error = models.FloatField(null=True, blank=True)
    parameter      = models.ForeignKey('Parameter', db_column='parameter_title', 
                                       on_delete=models.PROTECT)
    channel        = models.ForeignKey('Channel', 
                                       on_delete=models.PROTECT)
    measurement_point = models.ForeignKey('MeasurementPoint', 
                                          on_delete=models.PROTECT)
    session        = models.ForeignKey('Session', on_delete=models.PROTECT)
    
    def __unicode__(self):
        return u'%s, time: %s' % (unicode(self.measurement), unicode(self.measurement_point))
    class Meta:
        db_table = 'measurements'
        

class Units(models.Model):
    ''' Class representing parameter units
        
    This is the class storing the unique title, short name, long name and 
    description of units
    '''
    title       = models.CharField(max_length=255, primary_key=True)
    short_name  = models.CharField(max_length=45)
    long_name   = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title
    class Meta:
        db_table = 'units'
        verbose_name_plural = 'units'