# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from enterprise.models import *
from menu.models import *
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
            subcategory = SubMenuCategory.objects.filter(menu=menu)
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

    subMenus = SubMenuCategory.objects.filter(menu=menu)
    print(subMenus)

    for subMenu in subMenus:
        options = SubMenuCategoryOption.objects.filter(menu=menu, subMenu=subMenu)
        subMenu.options = options

    # Get Options of Menu



    context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise, 'menu': menu, 'subMenus': subMenus}
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
        cartTotal = cartTotal + item['totalPrice']


    context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise, 'cart': cartSession, 'total':cartTotal}
    return render(request, "order/cart.html", context)




def complated_view(request, id):

    sEnterprise = request.session.get('enterprise', 'enterprise')
    sTable = request.session.get('table', 'table')
    enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    cartSession = request.session['cart']

    cart = []

    cartTotal = 0

    # Tekrar eden urunleri bul, Menu objesinin icine count alani ekle ve orayi arttir
    for item in cartSession:
        # jQuery'den kaydolan menu id si ile Menu objesini cek
        menuItem = Menu.objects.get(id=item['id'])
        # Varsayilan olarak adeti 1 yap
        menuItem.count = 1
        menuItem.totalPrice = menuItem.price
        # Eger bu urun daha once sepete eklenmisse
        if menuItem in cart:
            # Onceki eklenmis urunu bul
            index = cart.index(menuItem)
            # Adet sayisini bir arttir
            cart[index].count += 1
            cart[index].totalPrice = cart[index].count * menuItem.price
        # Daha once sepette yoksa listeye ekle
        else:
            cart.append(menuItem)
        cartTotal += menuItem.price


    context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise, 'cart': cart, 'total':cartTotal}
    return render(request, "order/complated.html", context)








