from django.conf.urls import url

from api.views import *

app_name = 'api'

urlpatterns = [
	
	# CART
	url(r'^cart_add/?$', cart_add, name="cart_add"),
	url(r'^cart_delete/$', cart_delete, name="cart_delete"),
    url(r'^cart_show/$', cart_show, name="cart_show"),
    url(r'^cart_count/$', cart_count, name="cart_count"),
    url(r'^cart_update_count/$', cart_update_count, name="cart_update_count"),
    
    # ORDER
    url(r'^order_get/$', order_get, name="order_get"),

    # LINE
    url(r'^line_add/$', line_add, name="line_add"),
    url(r'^line_delete/$', line_delete, name="line_delete"),
    url(r'^line_get/$', line_get, name="line_get"),
    url(r'^line_get_for_printer/$', line_get_for_printer, name="line_get_for_printer"),
    url(r'^line_set_complated/$', line_set_complated, name="line_set_complated"),
    url(r'^line_set_complated_table/$', line_set_complated_table, name="line_set_complated_table"),
    url(r'^line_set_paid/$', line_set_paid, name="line_set_paid"),
    url(r'^line_set_canceled/$', line_set_canceled, name="line_set_canceled"),
    url(r'^line_set_printed/$', line_set_printed, name="line_set_printed"),


    # TABLE
	url(r'^table_create/$', table_create, name="table_create"),
	url(r'^table_update/$', table_update, name="table_update"),
	url(r'^table_delete/$', table_delete, name="table_delete"),


	# CATEGORY
	url(r'^category_create/$', category_create, name="category_create"),
	url(r'^category_update/$', category_update, name="category_update"),
	url(r'^category_delete/$', category_delete, name="category_delete"),
	url(r'^category_order/$', category_order, name="category_order"),


	# MENU
	url(r'^menu_create/$', menu_create, name="menu_create"),
	url(r'^menu_update/$', menu_update, name="menu_update"),
	url(r'^menu_delete/$', menu_delete, name="menu_delete"),
	url(r'^menu_get/$', menu_get, name="menu_get"),

	url(r'^line_status/$', line_status, name="line_status"),


	# BIOT
	url(r'^biot_order/$', biot_order, name="biot_order"),
	url(r'^biot_hepsiburada/$', biot_hepsiburada, name="biot_hepsiburada"),

	# CALL WAITER
	url(r'^waiter_call_create/$', waiter_call_create, name="waiter_call_create"),
	url(r'^waiter_call_complate/$', waiter_call_complate, name="waiter_call_complate"),
	url(r'^waiter_call_list/$', waiter_call_list, name="waiter_call_list"),
	

]
