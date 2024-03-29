from django.conf.urls import url
from django.urls import path

from . import views

app_name='recete'

urlpatterns = [
    url(r'recete/(?P<type>\d+)/list/$', views.ReceteList.as_view(), name='recete-list'),
    url(r'recete/(?P<hpk>[-a-zA-Z0-9_]+)/add/$', views.ReceteUygulamaCreate.as_view(), name='recete-add'),
    url(r'recete/(?P<pk>[0-9]+)/(?P<isCreate>[0-9]+)/$', views.ReceteUygulamaUpdate.as_view(), name='recete-update'),
    url(r'recete/(?P<pk>[0-9]+)/delete/$', views.ReceteDelete.as_view(), name='recete-delete'),
    path('receteHazirla/', views.hazirlamaList , name='hazirlamaList'),
    path('receteDurdur/<int:id>', views.receteDurdur , name='receteDurdur'),
    url(
         r'^mayi-autocomplete/$',
        views.MayiAutocomplete.as_view(),
        name='mayi-autocomplete',
    ),
    url(
         r'^ilac-autocomplete/$',
        views.IlacAutocomplete.as_view(),
        name='ilac-autocomplete',
    ),
    url(
         r'^hasta-autocomplete/$',
        views.HastaAutocomplete.as_view(),
        name='hasta-autocomplete',
    ),
    path('recetePrint/<str:id>/<str:sid>', views.printRecete , name='recete-print'),
]