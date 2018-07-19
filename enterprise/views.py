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
import json, pickle
import ast

from enterprise.models import *
from menu.models import *

from enterprise.forms import *
from account.forms import *


@login_required
def main_view(request):

	# sEnterprise = request.session.get('enterprise', 'enterprise')
	# sTable = request.session.get('table', 'table')
	# enterprise = get_object_or_404(Enterprise, name=sEnterprise)


	context = {}
	# context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise}
	return render(request, "enterprise/index.html", context)


@login_required
def order_view(request):
	
	context = {'active_tab': 'order'}
	return render(request, "enterprise/order.html", context)


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

	# Get Categories
	categories = Category.objects.filter(enterprise=request.user.profile.enterprise)

	# Get Category Menu Count
	for category in categories:
		menus = Menu.objects.filter(category=category)
		category.menuCount = menus.count

	context = {'active_tab': 'menu', 'menus': categories}
	return render(request, "enterprise/menu.html", context)


@login_required
def table_view(request):

	# Get Tables
	query = request.GET.get('search')
	if query:
		tables = Table.objects.filter(Q(name__icontains=query), enterprise=request.user.profile.enterprise).distinct()
	else:
		tables = Table.objects.filter(enterprise=request.user.profile.enterprise)

	context = {'active_tab': 'table', 'tables': tables}
	return render(request, "enterprise/table.html", context)



@login_required
def profile_view(request):

	print(request.user.username)

	form_enterprise = EnterpriseForm(request.POST or None, request.FILES or None, instance=request.user.profile.enterprise)
	form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
	
	if form.is_valid() and form_enterprise.is_valid():

		user = form.save(commit=False)
		user.username = form.cleaned_data.get('email')
		enterprise = form_enterprise.save()

		paw = form.cleaned_data.get('password1')
		if paw:
			user.set_password(paw)
			messages.success(request, "Successful. Your password has been changed.")
		else:
			messages.success(request, "Successful")

		user.save()
		user_login = authenticate(username=request.user.username, password=paw)
		login(request, user_login)

		return redirect('enterprise:profile')


	# sEnterprise = request.session.get('enterprise', 'enterprise')
	# sTable = request.session.get('table', 'table')
	# enterprise = get_object_or_404(Enterprise, name=sEnterprise)

	context = {'active_tab': 'profile', 'form': form, 'form_enterprise': form_enterprise}
	return render(request, "enterprise/profile.html", context)



def logout_view(request):
	if request.user:
		logout(request) 
	return redirect('enterprise:login')
