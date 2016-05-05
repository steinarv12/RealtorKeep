from django.conf.urls import url
from realtorApp import views


urlpatterns = [
    url(r'front', views.index, name='index'),
    url(r'update', views.update, name='update'),
    url(r'test', views.test, name='test'),
]
