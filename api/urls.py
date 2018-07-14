from django.conf.urls import url

from api.views import *

app_name = 'api'

urlpatterns = [

    url(r'^table_create/$', table_create, name="table_create"),

]
