# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import json

from barcode.models import *
from enterprise.models import *
from api.views import *



def health_view(request):
    return HttpResponse('OK')



def home_view(request):
    return redirect('enterprise:login')

    

# /redirect/XXXXXXXX Get ID, search Database and redirect related page
def redirect_view(request, id):
    barcode_valid = False
    barcode_active = False
    table_valid = False
    table_active = False
    enterprise = None
    table = None
    response_data = list()

    # Delete Old Session
    request.session['enterprise'] = None
    request.session['table'] = None

    # Get Barcode from database
    barcode = Barcode.objects.filter(barcode=id)

    # If Barcode exist
    if barcode:
        barcode = barcode[0]
        barcode_valid = True

        # If Barcode is active
        if barcode.active:
            barcode_active = True

            # Get Table from database
            table = Table.objects.filter(barcode=barcode)

            # If Table is exist
            if table:
                table = table[0]
                table_valid = True
                enterprise = table.enterprise

                # If Table is active
                if table.active:
                    table_active = True

                    request.session['enterprise'] = enterprise.id
                    request.session['table'] = table.id
                    
                else:
                    table_active = False
    else:
        barcode = None

    # Create Log with scanned time
    Log.objects.create(barcode=barcode, barcode_valid=barcode_valid, barcode_active=barcode_active, 
                       table_valid=table_valid, table_active=table_active,
                       enterprise=enterprise, table=table)

    # Delete shopping cart items
    cart_session_delete(request)

    return redirect('order:index')
