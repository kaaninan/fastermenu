# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localtime

from enterprise.models import *
from menu.models import *
from cart.models import *
from api.views import *
import json, datetime


def main_view(request):

	sEnterprise = request.session.get('enterprise', '')
	sTable = request.session.get('table', '')

	enterprise = get_object_or_404(Enterprise, id=sEnterprise)
	table = get_object_or_404(Table, id=sTable)

	# Get Menu
	categories = Category.objects.filter(enterprise=enterprise)

	state = {}

	state['added'] = False
	if 'added' in request.session:
		status = request.session['added']
		if status == 'success':
			state['added'] = True
			del request.session['added']


	state['deleteLine'] = False
	if 'deleteLine' in request.session:
		status = request.session['deleteLine']
		if status == 'success':
			state['deleteLine'] = True
			del request.session['deleteLine']


	for category in categories:
		menus = Menu.objects.filter(category=category)
		for menu in menus:
			subcategory = MenuSubCategory.objects.filter(menu=menu)
			menu.subcategory = subcategory
		category.menu = menus



	context = {'enterprise': enterprise, 'table': table, 'categories': categories, 'state': state}
	return render(request, "order/index.html", context)



def details_view(request, id):

	sEnterprise = request.session.get('enterprise', '')
	sTable = request.session.get('table', '')

	enterprise = get_object_or_404(Enterprise, id=sEnterprise)
	table = get_object_or_404(Table, id=sTable)

	# Get Menu Content
	menu = get_object_or_404(Menu, id=id)

	subMenus = MenuSubCategory.objects.filter(menu=menu)

	for subMenu in subMenus:
		options = MenuSubCategoryOption.objects.filter(subMenu=subMenu)
		subMenu.options = options


	context = {'enterprise': enterprise, 'table': table, 'menu': menu, 'subMenus': subMenus, 'backButton': True}
	return render(request, "order/details.html", context)



def cart_view(request):

	sEnterprise = request.session.get('enterprise', '')
	sTable = request.session.get('table', '')

	enterprise = get_object_or_404(Enterprise, id=sEnterprise)
	table = get_object_or_404(Table, id=sTable)

	# Edit Session
	getEdit = request.GET.get('edit', '')
	getLine = request.GET.get('line', '')

	if(getEdit == 'true'):
		dict = {'id': getLine, 'edit': True}
		qdict = QueryDict('', mutable=True)
		qdict.update(dict)
		request.POST = qdict
		line_delete(request)
		request.session['cart'] = request.session['backup']
		del request.session['backup']

	cartSession = request.session.get('cart', '')

	cart = []

	cartTotal = 0.0

	# print(cartSession)

	# Ayni urunden birden fazla eklendiyse
	# Tekrar eden urunleri bul, Menu objesinin icine count alani ekle ve orayi arttir
	for item in cartSession:
		dbMenu = Menu.objects.get(id=item['id'])
		print(dbMenu.price)
		print(item['totalPrice'])
		item['name'] = dbMenu.name
		item['description'] = dbMenu.description

		# Get Option Names
		if item['options'] != '-1':
			item['options_option'] = []
			item['options_dropadd'] = []
			for op in item['options']:
				op_object = MenuSubCategoryOption.objects.get(id=op)
				op_type = op_object.subMenu.type
				if op_type == 'option':
					item['options_option'].append(op_object)
				elif op_type == 'dropadd':
					item['options_dropadd'].append(op_object)

		cartTotal = cartTotal + item['totalPrice']


	context = {'enterprise': enterprise, 'table': table, 'cart': cartSession, 'total':cartTotal, 'backButton': True}
	return render(request, "order/cart.html", context)



def complated_view(request):

	sEnterprise = request.session.get('enterprise', '')
	sTable = request.session.get('table', '')

	enterprise = get_object_or_404(Enterprise, id=sEnterprise)
	table = get_object_or_404(Table, id=sTable)


	# Sayfa yenilenince siparis tekrar veriliyor
	# Siparisin uzerinden 30sn gecerse bu sayfayi gosterme

	# Daha once siparis verdiyse bu sayfayi gosterme
	# BUG: YENI SIPARIS VERINCE DIREK ESKI SIPARISE YONLENDIRIYOR
	if "line" in request.session:
		# Siparis tarihini session'dan al
		orderDate_s = request.session['line']['orderDate']
		# str to datetime
		orderDate = datetime.datetime.strptime(orderDate_s, '%Y-%m-%d %H:%M:%S')
		# Simdi
		now = datetime.datetime.now()
		# Farki hesapla
		diff = now - orderDate
		diff_seconds = int(diff.total_seconds())
		# -- BU HESAPLAMA SU AN KULLANILMAYACAK --

		# redirect
		return redirect('order:track', id=request.session['line']['id'])
	else:
		pass


	# Add Line and Get Line ID
	line_id = line_add(request)
	line_id = json.loads(line_id.content.decode('ascii'))
	line_id = line_id['line']

	# Get Line
	line = get_object_or_404(Line, id=line_id)

	line_serialize = {}
	line_serialize['id'] = line.id

	local_d = localtime(line.orderDate)

	date_normal = local_d.strftime('%Y-%m-%d %H:%M:%S')
	# line_serialize['orderDate'] = json.dumps(date_normal, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
	line_serialize['orderDate'] = date_normal
	request.session['line'] = line_serialize

	# # Delete Shopping List from Session
	request.session['backup'] = request.session['cart']
	cart_session_delete(request)


	context = {'enterprise': enterprise, 'table': table, 'enterprise': enterprise, 'line': line}
	return render(request, "order/complated.html", context)



def track_view(request, id):

	sEnterprise = request.session.get('enterprise', '')
	sTable = request.session.get('table', '')

	enterprise = get_object_or_404(Enterprise, id=sEnterprise)
	table = get_object_or_404(Table, id=sTable)

	# Siparisi bul
	line = get_object_or_404(Line, id=id)

	# Siparis icerigini bul
	orders = Order.objects.filter(line=line)


	context = {'enterprise': enterprise, 'table': table, 'line': line, 'orders': orders}
	return render(request, "order/track.html", context)








