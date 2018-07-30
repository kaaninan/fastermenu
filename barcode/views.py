# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from enterprise.models import *
from .models import *


@login_required
def single_view(request):

	barcode = request.GET.get('barcode', '')

	# Get Table Name
	objBarcode = Barcode.objects.get(barcode=barcode)
	table = Table.objects.get(enterprise=request.user.profile.enterprise, barcode=objBarcode)

	barcodes = [{'name':table.name, 'barcode':barcode}]

	context = {'barcodes': barcodes}
	return render(request, "barcode/qr.html", context)



@login_required
def multiple_view(request):

	# Get Table Name
	table = Table.objects.filter(enterprise=request.user.profile.enterprise, active=True)

	context = {'barcodes': table}
	return render(request, "barcode/qr.html", context)