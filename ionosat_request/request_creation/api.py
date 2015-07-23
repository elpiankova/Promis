from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from .models import Device, DeviceMode
from tastypie import fields
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer

class DeviceResource(ModelResource):
    """
    API Facet
    """

    class Meta:
        queryset = Device.objects.all()
        resource_name = 'device'
        allowed_methods = ['get']
        excludes = ['id', 'description', 'resource_uri']
        #include_resource_uri = False
        serializer = Serializer()
        #authentication = Authentication()
        #authorization = Authorization()
        #always_return_data = True

class DeviceModeResource(ModelResource):

    device = fields.ForeignKey(DeviceResource, 'device')

    class Meta:
        queryset = DeviceMode.objects.all()
        resource_name = 'devicemode'
        allowed_methods = ['get']
        excludes = ['id', 'description', 'resource_uri']
        include_resource_uri = False

class CustomJSONSerializer(Serializer):
    def to_json(self, data, options=None):
        options = options or {}

        data = self.to_simple(data, options)

        # Add in the current time.
        data['requested_time'] = time.time()

        return json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)

    def from_json(self, content):
        data = json.loads(content)

        if 'requested_time' in data:
            # Log the request here...
            pass

        return data