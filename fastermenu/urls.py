from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from redirect.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', test_view, name='index'),

    url(r'^redirect/(?P<id>[\w\.-]+)/$', redirect_view, name="redirect"),
    # url(r'^logout/$', logout_view, name="logout"),

    # url(r'^redirect/$', redirect_view, name="redirect"),

    url(r'^order/', include('order.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^enterprise/', include('enterprise.urls')),
    # url(r'^teacher/', include('teacher.urls')),
    # url(r'^student/', include('student.urls')),
    # url(r'^exam/', include('exams.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
