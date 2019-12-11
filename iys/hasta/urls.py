from django.conf.urls import url
from django.urls import path


from .views import (
    hastaList,
    hastaEdit
)

app_name='hasta'

urlpatterns = [
     path('hastaList/', hastaList,name="hastaList"),
     path('hastaEdit/', hastaEdit,name="hastaEdit"),
]
