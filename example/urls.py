from django.conf.urls import url

from teacher.views import *

app_name = 'teacher'

urlpatterns = [

    url(r'^$', home_view, name="index"),

    url(r'^change_password/?$', change_password_view, name="change_password"),

    url(r'^my_exams/?$', my_exams_view, name="my_exams"),
    url(r'^my_exams/(?P<id>[\w+]+)/update/$', my_exams_update_view, name="my_exams_update"),
    url(r'^my_exams/(?P<id>[\w+]+)/delete/$', my_exams_delete_view, name="my_exams_delete"),
    url(r'^my_exams/(?P<id>[\w+]+)/show/$', my_exams_show_view, name="my_exams_show"),

    url(r'^control_exam/$', control_exam_view, name="control_exam"),
    url(r'^control_exam/(?P<id>[\w+]+)/$', control_exam_list_view, name="control_exam_list"),

    url(r'^create_exam/$', exam_create_view, name="create_exam"),

    url(r'^questions/?$', questions_view, name="questions"),
    url(r'^questions/create/$', questions_create_view, name="questions_create"),
    url(r'^questions/(?P<id>[\w+]+)/update/$', questions_update_view, name="questions_update"),
    url(r'^questions/(?P<id>[\w+]+)/delete/$', questions_delete_view, name="questions_delete"),
    url(r'^questions/(?P<id>[\w+]+)/show/$', questions_show_view, name="questions_show"),

    url(r'^points/?$', points_view, name="points"),
    url(r'^points/(?P<id>[\w+]+)/?$', points_list_view, name="points_list"),

    url(r'^personal_settings/$', personal_settings_view, name="personal_settings"),

]
