"""geopromis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.contrib.gis import admin
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from geoprom import views
from geoprom.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router = routers.MongoSimpleRouter()
#router.register(r'datas', views.DataViewSet)
router.register(r'users', UserViewSet)
router.include_format_suffixes = False

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^satellites/$', views.SatelliteList.as_view()),
    url(r'^satellites/(?P<pk>[a-zA-Z]+)$', views.SatelliteDetail.as_view()),
    url(r'^sessions/(?P<pk>[0-9]+)$', views.SatelliteSession.as_view()), 
    url(r'^datas/$', views.DataViewSet.as_view({'get': 'list','post': 'create'})),     
]

urlpatterns = format_suffix_patterns(urlpatterns)
