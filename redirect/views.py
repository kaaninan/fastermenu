# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.utils import translation

from barcode.models import *
from enterprise.models import *
from api.views import *



def health_view(request):
    return HttpResponse('OK')



def home_view(request):
    return redirect('enterprise:login')


def change_language(request, lang):
    redirect = request.GET.get('redirect_to', '')
    user_language = lang
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    # redirect[3:] remove /en from path for redirect new selected language
    tourl = request.scheme + '://' + request.get_host() + redirect[3:]
    return HttpResponseRedirect(tourl)
    

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
    session_delete(request, 'enterprise')
    session_delete(request, 'table')
    session_delete(request, 'cart')
    # session_delete(request, 'line')

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


    # Redirect 404
    if not barcode or not barcode_valid or not barcode_active or not table_valid or not table_active:
        return redirect('order:notfound')

    # Create Log with scanned time
    Log.objects.create(barcode=barcode, barcode_valid=barcode_valid, barcode_active=barcode_active, 
                       table_valid=table_valid, table_active=table_active,
                       enterprise=enterprise, table=table)


    return redirect('order:index')
