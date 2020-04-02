from django.conf.urls import url
from django.urls import path


from .views import (
    openReportForm,
    openReport,
    durumReportForm,
    durumReport
)

app_name='report'

urlpatterns = [
     path('hastaReportForm/', openReportForm,name="hastaReportForm"),
     path('hastaReport/', openReport, name="hastaReport"),
     path('durumReportForm/', durumReportForm, name="durumReportForm"),
     path('durumReport/', durumReport, name="durumReport"),
]