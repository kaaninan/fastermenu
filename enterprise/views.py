# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.core import serializers
from django.db.models import Q
import json, pickle, ast
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import ugettext as _

from enterprise.models import *
from menu.models import *
from cart.models import *

from enterprise.forms import *
from account.forms import *
from menu.forms import *


def language_view(request):
    return render(request, 'languages/index.html')

@login_required
def main_view(request):

	# Redirect System Admin to /admin
	try:
		if not request.user.profile:
			pass
	except Exception as e:
		return redirect('admin:index')


	# Hesap Tamamlama Adimlari
	is_check = {}
	# Check Logo
	if request.user.profile.enterprise.logo == '':
		is_check['logo'] = False
	else:
		is_check['logo'] = True
	# Check Category
	if Category.objects.filter(enterprise=request.user.profile.enterprise).count() == 0:
		is_check['category'] = False
	else:
		is_check['category'] = True	
	# Check Menu
	if Menu.objects.filter(enterprise=request.user.profile.enterprise).count() == 0:
		is_check['menu'] = False
	else:
		is_check['menu'] = True	
	# Check Menu
	if Table.objects.filter(enterprise=request.user.profile.enterprise).count() == 0:
		is_check['table'] = False
	else:
		is_check['table'] = True
	

	context = {'is_check':is_check}
	return render(request, "enterprise/index.html", context)





@login_required
def order_view(request):
	
	context = {'active_tab': 'order'}
	return render(request, "enterprise/order.html", context)




@login_required
def table_detail_view(request):

	tableID = request.GET.get('id')

	fetch = Order.objects.filter(line__table_id= tableID).select_related('line', 'menu', 'line__table').values(
		'id', 'menu__name', 'count', 'optionsReadable', 'price', 'line__totalPrice', 'line__table__name', 'line__table__id', 'line__id',
		'line__orderDate','line__complatedDate', 'line__isComplated', 'line__isPaid'
	).order_by('-line__orderDate')


	# Calculate Total Price from Line
	totalPrice = 0.0
	for item in fetch:
		totalPrice += float(item['line__totalPrice'])
	
	context = {'active_tab': 'order', 'data':fetch, 'totalPrice':totalPrice}
	return render(request, "enterprise/table_details.html", context)





@login_required
def cash_view(request):

	context = {'active_tab': 'cash'}
	return render(request, "enterprise/cash.html", context)




@login_required
def category_view(request):

	# Get Categories
	query = request.GET.get('search')
	if query:
		categories = Category.objects.filter(Q(name__icontains=query), enterprise=request.user.profile.enterprise).distinct()
	else:
		categories = Category.objects.filter(enterprise=request.user.profile.enterprise)


	# Get Category Menu Count
	for category in categories:
		menus = Menu.objects.filter(category=category)
		category.menuCount = menus.count

	context = {'active_tab': 'menu', 'categories': categories}
	return render(request, "enterprise/category.html", context)





@login_required
def menu_view(request, id):

	# Get Menus
	query = request.GET.get('search')
	if query:
		menus = Menu.objects.filter(Q(name__icontains=query), enterprise=request.user.profile.enterprise, category=id)
	else:
		menus = Menu.objects.filter(enterprise=request.user.profile.enterprise, category=id)

	# Get Category
	category = Category.objects.get(id=id, enterprise=request.user.profile.enterprise)

	# Add Menu Form
	form = MenuForm()

	context = {'active_tab': 'menu', 'menus': menus, 'category': category, 'form': form}
	return render(request, "enterprise/menu.html", context)





@login_required
def table_view(request):

	# Get Tables
	query = request.GET.get('search')
	if query:
		tables = Table.objects.filter(Q(name__icontains=query), enterprise=request.user.profile.enterprise).distinct()
	else:
		tables = Table.objects.filter(enterprise=request.user.profile.enterprise).extra(
			select={'myinteger': "CAST(substring(name FROM '^[0-9]+') AS INTEGER)"}
		).order_by('myinteger')

	context = {'active_tab': 'table', 'tables': tables}
	return render(request, "enterprise/table.html", context)





@login_required
def analyze_view(request):


	some_day_last_week = timezone.now().date() - timedelta(days=7)
	monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
	monday_of_this_week = monday_of_last_week + timedelta(days=7)
	

	data_daily = Line.objects.filter(enterprise=request.user.profile.enterprise, orderDate__gte=timezone.now().date())
	data_weekly = Line.objects.filter(enterprise=request.user.profile.enterprise, orderDate__gte=monday_of_this_week)
	data_montly = Line.objects.filter(enterprise=request.user.profile.enterprise, orderDate__month__gte=timezone.now().month)


	total_daily = 0
	total_weekly  = 0
	total_montly = 0

	for item in data_daily:
		total_daily += item.totalPrice

	for item in data_weekly:
		total_weekly += item.totalPrice

	for item in data_montly:
		total_montly += item.totalPrice


	# Get Sales
	sales = {}
	sales['daily'] = data_daily.count
	sales['weekly'] = data_weekly.count
	sales['montly'] = data_montly.count

	# Get Endorsement
	endorsement = {}
	endorsement['daily'] = total_daily
	endorsement['weekly'] = total_weekly
	endorsement['montly'] = total_montly

	context = {'active_tab': 'analyze', 'sales': sales, 'endorsement': endorsement}
	return render(request, "enterprise/analyze.html", context)


@login_required
def comment_view(request):

	comment = Comment.objects.filter(enterprise=request.user.profile.enterprise).select_related('line', 'line__table').values(
		'id', 'comment', 'commentDate', 'line__table__name', 'line__id',
		'line__orderDate', 'line__isComplated', 'line__isPaid'
	).order_by('-line__orderDate')


	context = {'active_tab': 'comment', 'comment':comment}
	return render(request, "enterprise/comment.html", context)


@login_required
def comment_detail_view(request, id):

	# Get orders
	data = Line.objects.filter(id=id, enterprise=request.user.profile.enterprise).prefetch_related('order_set', 'comment_set').select_related('table').values(
    	'orderDate', 'complatedDate', 'paidDate', 'isComplated', 'isPaid', 'totalPrice', 'table__name',
    	'order__menu__name', 'order__count', 'order__totalPrice', 'order__optionsReadable', 'comment__comment', 'comment__commentDate'
	)

	process_time = data[0]['complatedDate'] - data[0]['orderDate']

	context = {'active_tab': 'comment', 'data':data, 'process_time': process_time}
	return render(request, "enterprise/order_detail.html", context)


@login_required
def biot_view(request):

	exist = Biot.objects.filter(enterprise=request.user.profile.enterprise)
	
	if exist:
		form = BiotForm(request.POST or None, enterprise=request.user.profile.enterprise, instance=exist[0])
	else:
		form = BiotForm(request.POST or None, enterprise=request.user.profile.enterprise)

	if form.is_valid():
		selected_menu = form.cleaned_data.get('menu')

		# Sadece bir tane kayit olacak
		selected = Biot.objects.filter(enterprise=request.user.profile.enterprise)
		
		if selected.count() == 0:
			# New
			obj = Biot()
			obj.menu = selected_menu
			obj.enterprise = request.user.profile.enterprise
			obj.save()
			messages.success(request, _("Successful!"))
		else:
			edit_obj = selected[0]
			edit_obj.menu = selected_menu
			edit_obj.save()
			messages.success(request, _("Successful!"))



	context = {'active_tab': 'biot', 'form': form}
	return render(request, "enterprise/biot.html", context)


@login_required
def profile_view(request):

	form_enterprise = EnterpriseForm(request.POST or None, request.FILES or None, instance=request.user.profile.enterprise)
	form = ProfileUpdateForm(request.POST or None, instance=request.user)
	
	if form.is_valid() and form_enterprise.is_valid():

		user = form.save(commit=False)
		user.username = form.cleaned_data.get('email')
		enterprise = form_enterprise.save()

		paw = form.cleaned_data.get('password1')
		if paw:
			user.set_password(paw)
			messages.success(request, _("Successful!"))
			user.save()
			user_login = authenticate(username=request.user.username, password=paw)
			login(request, user_login)

		else:
			messages.success(request, _("Successful!"))

		return redirect('enterprise:profile')


	context = {'active_tab': 'profile', 'form': form, 'form_enterprise': form_enterprise}
	return render(request, "enterprise/profile.html", context)



def logout_view(request):
	if request.user:
		logout(request) 
	return redirect('enterprise:login')
