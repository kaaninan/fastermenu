from django.conf.urls import url

from order.views import *

app_name = 'order'

urlpatterns = [

    url(r'^$', main_view, name="index"),

    url(r'^cart/$', cart_view, name="cart"),
    url(r'^detail/(?P<id>[\w+]+)/?$', details_view, name="detail"),
    url(r'^complated/$', complated_view, name="complated"),
    url(r'^track/(?P<id>[\w+]+)/$', track_view, name="track"),

]
