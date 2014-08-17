from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from promis_data import views


urlpatterns = patterns('',
    url(r'sessions/$', views.SessionList.as_view()),
    url(r'measurement_points/$', views.MeasurementPointList.as_view()),
    url(r'measurements/$', views.MeasurementList.as_view())
)

urlpatterns = format_suffix_patterns(urlpatterns)