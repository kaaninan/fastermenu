from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url

from enterprise.views import *
from account.views import *

app_name = 'enterprise'

urlpatterns = [

    url(r'^$', main_view, name="index"),

    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', signup_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),


    url(r'^password_reset/$', forget_password_view, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'post_reset_redirect': 'enterprise:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^order/$', order_view, name='order'),
    url(r'^cash/$', cash_view, name='cash'),
    url(r'^category/$', category_view, name='category'),
    url(r'^category/(?P<id>[\w+]+)/$', menu_view, name='menu'),
    url(r'^table/$', table_view, name='table'),
    url(r'^analyze/$', analyze_view, name='analyze'),
    url(r'^comment/$', comment_view, name='comment'),
    url(r'^comment/(?P<id>[\w+]+)/$', comment_detail_view, name='comment_detail'),
    url(r'^biot/$', biot_view, name='biot'),
    url(r'^profile/$', profile_view, name='profile'),

]
