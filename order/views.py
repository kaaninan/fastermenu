# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from enterprise.models import *
from menu.models import *
from cart.models import *
from cart.views import *
import json

def main_view(request):

    sEnterprise = request.session.get('enterprise', 'enterprise')
    sTable = request.session.get('table', 'table')

    enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    # Get Menu
    categories = Category.objects.filter(enterprise=enterprise)

    addedState = False
    if 'added' in request.session:
        status = request.session['added']
        if status == 'success':
            addedState = True
            del request.session['added']


    for category in categories:
        menus = Menu.objects.filter(category=category)
        for menu in menus:
            subcategory = MenuSubCategory.objects.filter(menu=menu)
            menu.subcategory = subcategory
        category.menu = menus



    context = {'enterprise': enterprise, 'table': sTable, 'categories': categories, 'addedState': addedState}
    return render(request, "order/index.html", context)



def details_view(request, id):

    sEnterprise = request.session.get('enterprise', 'enterprise')
    sTable = request.session.get('table', 'table')

    enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    # Get Menu Content
    menu = get_object_or_404(Menu, id=id)

    subMenus = MenuSubCategory.objects.filter(menu=menu)

    print(subMenus)

    for subMenu in subMenus:
        options = MenuSubCategoryOption.objects.filter(subMenu=subMenu)
        print(options)
        subMenu.options = options

    # Get Options of Menu



    context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise, 'menu': menu, 'subMenus': subMenus, 'backButton': True}
    return render(request, "order/details.html", context)



def cart_view(request):

    sEnterprise = request.session.get('enterprise', 'enterprise')
    sTable = request.session.get('table', 'table')
    enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    cartSession = request.session.get('cart', '')

    cart = []

    cartTotal = 0.0

    # print(cartSession)

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
                    item['options_option'].append(op_object)
                elif op_type == 'dropadd':
                    item['options_dropadd'].append(op_object)

        cartTotal = cartTotal + item['totalPrice']


    context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise, 'cart': cartSession, 'total':cartTotal, 'backButton': True}
    return render(request, "order/cart.html", context)



def complated_view(request):

    sEnterprise = request.session.get('enterprise', 'enterprise')
    sTable = request.session.get('table', 'table')
    enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    # Add Line and Get Line ID
    line_id = add_line_view(request)
    line_id = json.loads(line_id.content.decode('ascii'))
    line_id = line_id['line']

    # Delete Shopping List from Session
    delete_session_view(request)


    context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise, 'line_id': line_id}
    return render(request, "order/complated.html", context)



def track_view(request, id):

    sEnterprise = request.session.get('enterprise', 'enterprise')
    sTable = request.session.get('table', 'table')
    enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    # Siparisi bul
    line = get_object_or_404(Line, id=id)

    # Siparis icerigini bul
    orders = Order.objects.filter(line=line)


    context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise, 'line': line, 'orders': orders}
    return render(request, "order/track.html", context)








