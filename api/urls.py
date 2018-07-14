from django.conf.urls import url

from api.views import *

app_name = 'api'

urlpatterns = [

    url(r'^table_create/$', table_create, name="table_create"),
    url(r'^table_update/$', table_update, name="table_update"),
    url(r'^table_delete/$', table_delete, name="table_delete"),

]
