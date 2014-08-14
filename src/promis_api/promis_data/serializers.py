from promis_data.models import Channel, Session, Measurement, MeasurementPoint
from rest_framework import serializers


class ChannelSerializers(serializers.ModelSerializer):
    ''' '''
    
    class Meta:
        model = Channel
        fields = ('title')
        
class SessionSerializers(serializers.ModelSerializer):
    ''' '''
    class Meta:
        model = Session
        

class MeasurementPointSerializers(serializers.ModelSerializer):
    ''' '''
    class Meta:
        model = MeasurementPoint


class MeasurementSerializers(serializers.ModelSerializer):
    ''' '''
    class Meta:
        model = Measurement
        fields = ('level_marker', 'measurement', 'channel', 'parameter',
                  'measurement_point', 'session')
        depth = 1
        read_only_fields = ('parameter', 'channel', 'session')


if __name__ == '__main__':
    import os, sys
    sys.path.append("/home/elena/workspace/promis/src/promis_api")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")
    
#     Measurement.objects.all().delete()
#     Session.objects.all().delete()
#     MeasurementPoint.objects.all().delete()

    m = Measurement.objects.all()[0]
    serializer = MeasurementSerializers(m)
    print serializer.data