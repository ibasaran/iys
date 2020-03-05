from django.conf.urls import url
from django.urls import path


from .views import (
    hastaList,
    hastaEdit,
    hastaAdd
)

app_name='hasta'

urlpatterns = [
     path('hastaList/', hastaList,name="hastaList"),
     path('hastaAdd/', hastaAdd,name="hastaAdd"),
     path('hastaEdit/<int:id>', hastaEdit,name="hastaEdit"),
]