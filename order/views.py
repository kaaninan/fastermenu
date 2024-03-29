# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localtime
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import ugettext as _

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

	# For notifications (method could be changed)

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


	# Get Last Orders in Session
	lastOrders = list()
	if "line" in request.session:
		for item in request.session['line'][::-1]: # Reverse list

			# Check enterprise
			if int(sEnterprise) == int(item['enterprise']):

				# Get Line from Database
				# TODO Session'da sadece ID tutulabilir
				line = Line.objects.get(enterprise=sEnterprise, id=item['id'])

				# Son siparis tarihini session'dan al
				orderDate = line.orderDate
				# str to datetime
				# orderDate = datetime.datetime.strptime(orderDate_s, '%Y-%m-%d %H:%M:%S')
				# Get now
				now = timezone.now()

				# Get Orders
				order = list(Order.objects.filter(line=item['id']).values())
				line.order = []
				line.orderString = ''
				# for idx, val in enumerate(ints):
				for idx, orderItem in enumerate(order):
					try:
						menu = Menu.objects.get(id=orderItem['menu_id'])
						# Prepare string for order index, last orders
						line.orderString += menu.name
						if idx != (len(order) - 1):
							line.orderString += ", "
						line.order.append(menu.name)
					except Exception as e:
						pass

				# If ordered last 1 month
				diff = now - orderDate
				if (diff.days < 30):
					lastOrders.append(line)
		
		# Limit 6 orders
		lastOrders = lastOrders[-6:]


	context = {'enterprise': enterprise, 'table': table, 'categories': categories, 'state': state, 'orders': lastOrders}
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

	# If clicks Sepeti Duzenle on complated view, then this works
	if(getEdit == 'true'):

		# If refresh, Line could be deleted
		listLine = Line.objects.filter(id=getLine)
		if listLine.count() == 0:
			return redirect('order:index')

		# if edit == TRUE, success message wont show on order index page
		# edit == FALSE is Sepet Silme action, message will show on order index page
		dict = {'id': getLine, 'edit': True}
		qdict = QueryDict('', mutable=True)
		qdict.update(dict)
		request.POST = qdict
		line_delete(request)

		# When runs complated view, request.session['cart'] will be deleted. So to go back old order, use ['backup'] session
		# and delete backup
		request.session['cart'] = request.session['backup']
		del request.session['backup']

	cartSession = request.session.get('cart', '')

	print(cartSession)

	cartTotal = 0.0


	# Ayni urunden birden fazla eklendiyse
	# Tekrar eden urunleri bul, Menu objesinin icine count alani ekle ve orayi arttir
	for item in cartSession:
		dbMenu = Menu.objects.get(id=item['id'])
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
					item['options_option'].append(op_object.name)
				elif op_type == 'dropadd':
					item['options_dropadd'].append(op_object.name)

		cartTotal = cartTotal + item['totalPrice']


	context = {'enterprise': enterprise, 'table': table, 'cart': cartSession, 'total':cartTotal, 'backButton': True}
	return render(request, "order/cart.html", context)



def complated_view(request):

	# Get totalPrice and tip price
	tip_custom = request.POST.get('custom-tip', '')
	tip_val = request.POST.get('tip-val', '')
	payment = request.POST.get('payment', '')

	tip = 0 #as %

	if tip_val == '' and tip_custom != '':
		tip = int(tip_custom)
	elif tip_custom == '' and tip_val != '':
		tip = int(tip_val[:2])
	else:
		tip = 0


	sEnterprise = request.session.get('enterprise', '')
	sTable = request.session.get('table', '')

	enterprise = get_object_or_404(Enterprise, id=sEnterprise)
	table = get_object_or_404(Table, id=sTable)

	sOrder = request.session.get('cart', '')

	# If there is a valid cart, Line will be updated
	# line = None 

	if(sOrder == ''):
		# Refresh or Nothing
		# Check Last Line
		# Was it given in 30 seconds?
		if "line" in request.session:
			# Son siparis tarihini session'dan al
			orderDate_s = request.session['line'][-1]['orderDate']
			# str to datetime
			orderDate = datetime.datetime.strptime(orderDate_s, '%Y-%m-%d %H:%M:%S')
			# Simdi
			now = datetime.datetime.now()
			# Farki hesapla
			diff = now - orderDate
			diff_seconds = int(diff.total_seconds())
			
			# If just ordered, show page in 30 seconds
			if diff_seconds <= 30:
				line = get_object_or_404(Line, id=request.session['line'][-1]['id'])

			# Else redirect track
			else:
				# redirect track
				return redirect('order:track', id=request.session['line'][-1]['id'])

		else:
			# There is no line & order here
			return redirect('order:index')

	
	# If coming from cart page and have orders
	else:
		# Add Line and Get Line ID
		line_id = line_add(request, tip=tip, payment=payment)
		line_id = json.loads(line_id.content.decode('ascii'))
		line_id = line_id['line']

		# Get Line
		line = get_object_or_404(Line, id=line_id)

		# Add Line to Session

		# Get old list and append if exist, otherwise create new list
		line_list = list()
		if 'line' in request.session:
			line_list = request.session['line']
		
		line_serialize = {}
		local_d = localtime(line.orderDate)
		date_string = local_d.strftime('%Y-%m-%d %H:%M:%S')
		line_serialize['id'] = line.id
		line_serialize['orderDate'] = date_string
		line_serialize['table'] = table.name
		line_serialize['enterprise'] = sEnterprise

		line_list.append(line_serialize)
		request.session['line'] = line_list


		# Delete Shopping List from Session
		request.session['backup'] = request.session['cart']
		session_delete(request, 'cart')


	context = {'enterprise': enterprise, 'table': table, 'enterprise': enterprise, 'line': line}
	return render(request, "order/complated.html", context)



def track_view(request, id):

	sEnterprise = request.session.get('enterprise', '')
	sTable = request.session.get('table', '')

	enterprise = get_object_or_404(Enterprise, id=sEnterprise)
	table = get_object_or_404(Table, id=sTable)

	# Siparisi bul
	line = get_object_or_404(Line, id=id)

	# Yorumu Kaydet
	post = request.POST
	if post:
		# Create Comment
		comment = Comment()
		comment.commentDate = datetime.datetime.now()
		comment.comment = request.POST['comment']
		comment.line = line
		comment.enterprise = enterprise
		comment.save()

		# Edit Line Object
		line.isCommented = True
		line.save()

		# Send Message
		messages.success(request, _("Yorumunuz kaydedildi!"))

	# Siparis icerigini bul
	orders = Order.objects.filter(line=line)

	# Yorum varsa getir
	if line.isCommented:
		comment = Comment.objects.get(enterprise=enterprise, line=line)
		line.comment = comment
		print(comment.commentDate)



	context = {'enterprise': enterprise, 'table': table, 'line': line, 'orders': orders}
	return render(request, "order/track.html", context)




def notfound_view(request):
	return render(request, "404.html", {})

