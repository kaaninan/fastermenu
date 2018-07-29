from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'barcode'

urlpatterns = [

    url(r'^single$', single_view, name='single'),
    url(r'^multiple$', multiple_view, name='multiple'),

]
