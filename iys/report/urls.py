from django.conf.urls import url
from django.urls import path


from .views import (
    openReportForm
)

app_name='report'

urlpatterns = [
     path('hastaReport/', openReportForm,name="hastaReport"),
]