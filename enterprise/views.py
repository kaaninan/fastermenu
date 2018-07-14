# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib import messages

from enterprise.models import *
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

	# sEnterprise = request.session.get('enterprise', 'enterprise')
	# sTable = request.session.get('table', 'table')
	# enterprise = get_object_or_404(Enterprise, name=sEnterprise)

	context = {'active_tab': 'order'}
	# context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise}
	return render(request, "enterprise/order.html", context)




@login_required
def table_view(request):

	# sEnterprise = request.session.get('enterprise', 'enterprise')
	# sTable = request.session.get('table', 'table')
	# enterprise = get_object_or_404(Enterprise, name=sEnterprise)

	context = {'active_tab': 'table'}
	# context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise}
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







