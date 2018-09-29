from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns


from enterprise.views import *
from redirect.views import *

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^$', home_view, name='index'),

    url(r'^health/', health_view),

    url(r'^redirect/(?P<id>[\w\.-]+)/$', redirect_view, name="redirect"),
    url(r'^lang/(?P<lang>[\w\.-]+)/$', change_language, name="change_language"),

    url(r'^api/', include('api.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    
]

urlpatterns += i18n_patterns(
    url(r'^order/', include('order.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^enterprise/', include('enterprise.urls')),
    url(r'^barcode/', include('barcode.urls')),
)
