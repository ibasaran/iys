from django.conf.urls import url
from django.urls import path

from . import views

app_name='recete'

urlpatterns = [
    url(r'recete/list/$', views.ReceteList.as_view(), name='recete-list'),
    url(r'recete/add/$', views.ReceteUygulamaCreate.as_view(), name='recete-add'),
    url(r'recete/(?P<pk>[0-9]+)/$', views.ReceteUygulamaUpdate.as_view(), name='recete-update'),
    url(r'recete/(?P<pk>[0-9]+)/delete/$', views.ReceteDelete.as_view(), name='recete-delete'),
    path('receteHazirla/', views.hazirlamaList , name='hazirlamaList'),
]