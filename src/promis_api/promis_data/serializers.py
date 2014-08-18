from promis_data.models import Channel, Session, Measurement, MeasurementPoint, Parameter, Device
from rest_framework import serializers


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('title', 'satellite')


class ChannelSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()
    
    class Meta:
        model = Channel
        fields = ('title', 'device')

      
class SessionSerializer(serializers.Serializer):
    time_begin = serializers.DateTimeField()
    time_end = serializers.DateTimeField()
    time_interval = serializers.Field(source='time_interval')
    
    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.time_begin = attrs.get('time_begin', instance.time_begin)
            instance.time_end = attrs.get('time_end', instance.time_end)
            return instance
        return Session(**attrs)
    def get_identity(self, data):
        try:
            return data.get('time_begin', None)
        except AttributeError:
            return None
        

class MeasurementPointSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MeasurementPoint
        fields =('time', 'x_geo', 'y_geo', 'z_geo')


class MeasurementSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    parameter = serializers.PrimaryKeyRelatedField()
    measurement_point = MeasurementPointSerializer()
    session = SessionSerializer(read_only=True)
    
    class Meta:
        model = Measurement
        fields = ('level_marker', 'measurement', 'relative_error', 
                  'channel', 'parameter', 'measurement_point', 'session')
        
    def restore_object(self, attrs, instance=None):
        '''
        Given a dictionary of deserialized field values,
        either update an existing model, or create a new instance.
        '''
        print "HHHHHH"
        if instance is not None:
            instance.level_marker = attrs.get('level_marker', instance.level_marker)
            instance.measurement = attrs.get('measurement', instance.measurement)
            return instance
        print attrs.get('channel')
        print type(attrs['channel'])
        channel = Channel.objects.get(title=attrs['channel']['title'],
                                      device__title=attrs['channel']['device'],
                                      device__satellite__title=attrs.pop('channel')['satellite'])
        parameter = Parameter.objects.get(title=attrs.pop('parameter'))
        mp = MeasurementPoint.objects.get(time=attrs['measurement_point']['time'],
                                          x_geo=attrs['measurement_point'].get('x_geo'),
                                          y_geo=attrs['measurement_point'].get('y_geo'),
                                          z_geo=attrs.pop('measurement_point').get('z_geo'))
        session = Session.objects.get(time_begin=attrs['session']['time_bigin'],
                                      time_end=attrs.pop('session')['time_end'])
        return Measurement(channel=channel, parameter=parameter, measurement_point=mp,
                           session=session, **attrs)



          
#         obj.parameter = Parameter.objects.get(title=self.request.DATA.get('parameter'))
#         obj.channel = Channel.objects.get(title = self.request.DATA['channel']['title'],
#                                           device__title = self.request.DATA['channel']['device']
#                                          ) 
#         obj.measurement_point = MeasurementPoint.objects.get(time=self.request.DATA['measurement_point']['time'])
#         obj.session = Session.objects.get(time_begin=self.request.DATA['session']['time_begin'],
#                                           time_end=self.request.DATA['session'][''])




if __name__ == '__main__':
    import os, sys
    sys.path.append("/home/elena/workspace/promis/src/promis_api")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")
    import datetime, pytz
    data={'level_marker': 0, 'measurement': 1575.21216, 
          'channel': {'title': u'Bx quasiconstant', 'device': {'title': u'DC fluxgate magnetometer FZM', 'satellite': u'Variant'}}, 
          'parameter': u'X-component of magnetic field vector', 
          'measurement_point': {'time': datetime.datetime(2005, 2, 1, 8, 22, 59, tzinfo=pytz.utc), 'x_geo': None, 'y_geo': None, 'z_geo': None}, 
          'session': {'time_begin': datetime.datetime(2005, 2, 1, 8, 22, 59, tzinfo=pytz.utc), 'time_end': datetime.datetime(2005, 2, 1, 8, 43, 29, tzinfo=pytz.utc)}}

#     serializer = MeasurementSerializer(Measurement.objects.first())
#     print serializer.data
    serializer = MeasurementSerializer(data=data)
    print serializer.is_valid()
    print serializer.errors
    print serializer.data
    
    
#     Session.objects.all().delete()
#     MeasurementPoint.objects.all().delete()
#     data = [
#             {'time_begin': datetime.datetime(2005, 2, 1, 9, 22, 59, tzinfo=pytz.utc),
#              'time_end': datetime.datetime(2005, 2, 1, 9, 43, 29, tzinfo=pytz.utc)}
#             ]
# 
#     qs = Session.objects.all()
#     for s in qs: print s
# 
# #     serializer = SessionSerializers(qs, many=True)
#     serializer = SessionSerializers(data=data, many=True)
# # 
#     print serializer.is_valid()
#     print serializer.errors
# # #     
#     serializer.save()
# #     print Session.objects.all()
# #     print 
#     print serializer.data
#     qs = Session.objects.all()
#     for s in qs: print s