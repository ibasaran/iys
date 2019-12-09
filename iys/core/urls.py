from django.conf.urls import url
from django.urls import path


from .views import (
    login_page,
    
)

app_name='core'

urlpatterns = [
    url(r'^$', login_page,name="login"),
]
