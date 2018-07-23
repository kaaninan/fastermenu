from django.conf.urls import url

from cart.views import *

app_name = 'cart'

urlpatterns = [

    url(r'^$', add_view, name="index"),

    url(r'^cart/$', add_view, name="cart"),

    # url(r'^change_password/?$', change_password_view, name="change_password"),

    # API

    url(r'^add/?$', add_view, name="add"),
    url(r'^remove/(?P<id>[\w+]+)/$', delete_session_view, name="remove"),
    # url(r'^update/(?P<id>[\w+]+)/$', add_view, name="update"),
    url(r'^updateCount/$', update_count_view, name="updateCount"),
    url(r'^show/$', show_view, name="show"),
    url(r'^count/$', count_view, name="count"),
    url(r'^delete/$', delete_view, name="delete"),

    # LINE

    url(r'^get_line/$', get_line, name="get_line"),
    url(r'^get_line_cash/$', get_line_cash, name="get_line_cash"),
    url(r'^set_complated/$', line_set_complated, name="set_complated"),
    url(r'^set_paid/$', line_set_paid, name="set_paid"),

    # url(r'^my_exams/(?P<id>[\w+]+)/show/$', my_exams_show_view, name="my_exams_show"),

    # url(r'^control_exam/$', control_exam_view, name="control_exam"),
    # url(r'^control_exam/(?P<id>[\w+]+)/$', control_exam_list_view, name="control_exam_list"),

    # url(r'^create_exam/$', exam_create_view, name="create_exam"),

    # url(r'^questions/?$', questions_view, name="questions"),
    # url(r'^questions/create/$', questions_create_view, name="questions_create"),
    # url(r'^questions/(?P<id>[\w+]+)/update/$', questions_update_view, name="questions_update"),
    # url(r'^questions/(?P<id>[\w+]+)/delete/$', questions_delete_view, name="questions_delete"),
    # url(r'^questions/(?P<id>[\w+]+)/show/$', questions_show_view, name="questions_show"),

    # url(r'^points/?$', points_view, name="points"),
    # url(r'^points/(?P<id>[\w+]+)/?$', points_list_view, name="points_list"),

    # url(r'^personal_settings/$', personal_settings_view, name="personal_settings"),

]
