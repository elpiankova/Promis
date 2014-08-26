from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from promis_data import views
from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', views.ViewerMain.as_view(), name='viewer_main'),
    url(r'^channels/$', views.ChannelList.as_view()),
    url(r'sessions/$', views.SessionList.as_view()),
    url(r'measurement_points/$', views.MeasurementPointList.as_view()),
    url(r'measurements/$', views.MeasurementList.as_view())
)

urlpatterns = format_suffix_patterns(urlpatterns)