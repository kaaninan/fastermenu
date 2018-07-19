from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from enterprise.views import *
from account.views import *

app_name = 'enterprise'

urlpatterns = [

    url(r'^$', main_view, name="index"),

    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^register/$', signup_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),


    # url(r'^registration/', include('django.contrib.auth.urls')),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^order/$', order_view, name='order'),
    url(r'^cash/$', cash_view, name='cash'),
    url(r'^category/$', category_view, name='category'),
    url(r'^category/(?P<id>[\w+]+)/$', menu_view, name='menu'),
    url(r'^table/$', table_view, name='table'),
    url(r'^profile/$', profile_view, name='profile'),

]
