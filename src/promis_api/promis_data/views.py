from promis_data.models import Session, MeasurementPoint, Measurement
from promis_data.models import Parameter, Channel
from promis_data.serializers import SessionSerializer, MeasurementPointSerializer
from promis_data.serializers import MeasurementSerializer
from rest_framework import views, status, generics
from rest_framework.response import Response


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

class MeasurementList(generics.ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    
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
        
    