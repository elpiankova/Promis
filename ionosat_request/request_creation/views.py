from django.shortcuts import render

from .models import Device, Request, DeviceSwitch
from rest_framework import viewsets
from .serializers import DeviceSerializer, RequestSerializer, DeviceSwitchSerializer
from django.http import HttpResponse
import json


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):

    """ function view_get_number used for autoincrement number of request
        function view_orbit_flag used for creation json
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
# Create your views here.
class RequestViewSet(viewsets.ModelViewSet):

    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class DeviceSwitchViewSet(viewsets.ModelViewSet):

    queryset = DeviceSwitch.objects.all()
    serializer_class = DeviceSwitchSerializer


def view_get_number(request):
    last_object = Request.objects.last()

    if last_object != None:
        return HttpResponse(last_object.number+1)
    else:
        return HttpResponse(1)

def view_orbit_flag(request):
    list_orbit_flag = []
    for i in Request.ORBIT_FLAG:
        list_orbit_flag.append({"code": i[0], "name": i[1]})

    return HttpResponse(json.dumps(list_orbit_flag))
# def view_last_request(request):
#     last_request =