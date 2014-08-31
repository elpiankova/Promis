from promis_data.models import Session, MeasurementPoint, Measurement
from promis_data.models import Parameter, Channel, Satellite
from promis_data.serializers import SessionSerializer, MeasurementPointSerializer
from promis_data.serializers import MeasurementSerializer, ChannelSerializer
from django.views.generic.base import TemplateView
from rest_framework import views, status, generics
from rest_framework.response import Response
import dateutil.parser
import pytz

class ViewerMain(TemplateView):
    template_name = "promis_data/main.html"

    def get_context_data(self, **kwargs):
        return {
            'data_sources': self.data_sources(),
        }

    def data_sources(self):
        satellites = Satellite.objects.all()
        return [sat.title for sat in satellites]

class ChannelList(generics.ListAPIView):
    serializer_class = ChannelSerializer
    
    def get_queryset(self):
        '''
        This views returns a list of all Channels 
        Optionally restricts the returned Channels by satellites 
        given in 'satellite' query parameter in the URL
        '''
        satellite_title = self.request.QUERY_PARAMS.get('satellite', None)
        if satellite_title is not None:
            try:
                satellite = Satellite.objects.get(title=satellite_title)
            except Satellite.DoesNotExist:
                return
            queryset = Channel.objects.filter(
                          device__satellite=satellite
                       ).exclude(title__contains='E4'
                       ).exclude(title__contains='E5'
                       ).exclude(title__contains='E6'
                       ).exclude(title__startswith='T')
        else:
            queryset = Channel.objects.all()
        return queryset


class SessionList(views.APIView):
    '''
    List all sessions, or create one or few new sessions
    '''
    queryset = Session.objects.all()
#     serializer_class = SessionSerializers
    
    def get(self, request, format=None):
        serializer = SessionSerializer(self.queryset, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):       
        if isinstance(request.DATA, list):
            serializer = SessionSerializer(data=request.DATA, many=True)
        else:
            serializer = SessionSerializer(data=request.DATA)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                 


class MeasurementPointList(views.APIView):
    '''
    List all measurement points, or create one or few new measurement points
    '''
    queryset = MeasurementPoint.objects.all()
#     serializer_class = SessionSerializers
    
    def get(self, request, format=None):
        serializer = MeasurementPointSerializer(self.queryset, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):       
        if isinstance(request.DATA, list):
            serializer = MeasurementPointSerializer(data=request.DATA, many=True)
        else:
            serializer = MeasurementPointSerializer(data=request.DATA)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class MeasurementList(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    
    def get_queryset(self):
        '''
        This views returns a list of all measurements 
        Optionally restricts the returned measurements by channel  
        and time interval given in query parameter in the URL
        '''
        satellite_title = self.request.QUERY_PARAMS.get('satellite', None)
        channel_title = self.request.QUERY_PARAMS.get('channel', None)
        time_interval = self.request.QUERY_PARAMS.get('time_interval', None)
        if (satellite_title is not None 
              and channel_title is not None 
              and time_interval is not None):
#             satellite = Satellite.objects.get(title=satellite_title)
#             channel = Channel.objects.get(title=channel_title,
#                                           device__satellite=satellite)
            (time_begin, time_end) = map(dateutil.parser.parse,time_interval.split('_'))
            queryset = Measurement.objects.filter(
                                                  channel__device__satellite__title=satellite_title,
                                                  channel__title=channel_title,
                                                  measurement_point__time__gte=time_begin,
                                                  measurement_point__time__lte=time_end
                                                  ).order_by('measurement_point__time')
        else:
            queryset = Measurement.objects.all()
        return queryset
    
    
#     def pre_save(self, obj):
#         obj.parameter = Parameter.objects.get(title=self.request.DATA.get('parameter'))
#         obj.channel = Channel.objects.get(title = self.request.DATA['channel']['title'],
#                                           device__title = self.request.DATA['channel']['device']
#                                          ) 
#         obj.measurement_point = MeasurementPoint.objects.get(time=self.request.DATA['measurement_point']['time'])
#         obj.session = Session.objects.get(time_begin=self.request.DATA['session']['time_begin'],
#                                           time_end=self.request.DATA['session'][''])

# from django.http import HttpResponse
# import json 
# 
# def quicklook(request):
#     if request.method == 'POST':
#         json_request = json.loads(request.POST['json'])
#         if json_request.get('type') == 'quicklook':
#             pass
#         else:
#             return HttpResponse('No such type of json requests')
#         
        
    