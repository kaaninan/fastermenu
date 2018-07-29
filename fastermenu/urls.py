from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from redirect.views import *

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^$', home_view, name='index'),

    url(r'^health/', health_view),

    url(r'^redirect/(?P<id>[\w\.-]+)/$', redirect_view, name="redirect"),

    url(r'^order/', include('order.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^enterprise/', include('enterprise.urls')),

    url(r'^api/', include('api.urls')),
    url(r'^barcode/', include('barcode.urls')),
    
]
