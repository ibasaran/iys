from django.conf.urls import url
from django.urls import path



from .views import (
    login_page,
    dashboard,
    logout
)

app_name='core'

urlpatterns = [
    url(r'^$', login_page,name="login"),
    path('dashboard/', dashboard,name="dashboard"),
    path('logout/', logout,name="logout"),
    
]
