from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from .models import Device


class DeviceResource(ModelResource):
    """
    API Facet
    """
    class Meta:
        queryset = Device.objects.all()
        resource_name = 'device'
        allowed_methods = ['post', 'get', 'patch', 'delete']
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

