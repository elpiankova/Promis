from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'geoprom.views.MainView'),
    ]