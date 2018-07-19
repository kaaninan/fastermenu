from django.conf.urls import url

from api.views import *

app_name = 'api'

urlpatterns = [

	url(r'^table_create/$', table_create, name="table_create"),
	url(r'^table_update/$', table_update, name="table_update"),
	url(r'^table_delete/$', table_delete, name="table_delete"),

	url(r'^category_create/$', category_create, name="category_create"),
	url(r'^category_update/$', category_update, name="category_update"),
	url(r'^category_delete/$', category_delete, name="category_delete"),

	url(r'^line_status/$', line_status, name="line_status"),

]
