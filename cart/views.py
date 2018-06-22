from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json, pickle
from menu.models import *
from menu.forms import *
import ast


def show_view(request):
    
    if "cart" in request.session:
        result = request.session["cart"]

    else:
        result = False

    data = {'result':result}
    return JsonResponse(data)


def add_view(request):

    productId = request.POST.get('id', '')
    productCount = request.POST.get('count', '')
    productPrice = request.POST.get('price', '')
    productOptions = request.POST.get('option', '')
    displayAlert = request.POST.get('displayAlert', '')
    # Option String List to Normal List
    if(productOptions != '-1'):
        productOptions = ast.literal_eval(productOptions)


    menu = {}
    menu['id'] = int(productId)
    menu['price'] = float(productPrice)
    menu['count'] = int(productCount)
    menu['options'] = productOptions
    menu['totalPrice'] = float(productPrice.replace(',','.'))

    str_menu = json.dumps(menu)

    newList = list()

    # deneme = serializers.serialize("json", menu)

    # Listeyi Cek, For'da dondur, yeni liste olustur
    # eger ayni urunden varsa countu arttir ve liseteye ekle, yeni urunse direk yeni listeye ekle
    # sessionu sil ve yeni listeyi ekle

    
    added = False

    # Daha once sepet session'u olusturulmus mu?
    if "cart" in request.session:
        productList = request.session['cart']

        # Daha once ayni urun eklenmis mi?
        for product in productList:
            # product = json.loads(product)
            if product['id'] == menu['id'] and product['options'] == menu['options']:
                # Edit Already Saved Product Count
                product['count'] = product['count'] + menu['count']
                product['totalPrice'] = float(product['price']) * product['count']
                added = True
                newList.append(product)
            else:
                newList.append(product)

        # Yeni bir urun ise
        if(added == False):
            newList.append(menu)
        
        request.session['cart'] = newList

    else:
        productList = []
        productList.append(menu)
        request.session['cart'] = productList

    
    if displayAlert:
        request.session['added'] = 'success'
    
    data = {'OK':'OK'}
    return JsonResponse(data)


def delete_view(request):

    productId = request.POST.get('id', '')
    productCount = request.POST.get('count', '')
    productPrice = request.POST.get('price', '')
    productOptions = request.POST.get('option', '')
    # Option String List to Normal List
    if(productOptions != '-1'):
        productOptions = ast.literal_eval(productOptions)

    menu = {}
    menu['id'] = int(productId)
    menu['price'] = float(productPrice)
    menu['count'] = int(productCount)
    menu['options'] = productOptions
    menu['totalPrice'] = float(productPrice.replace(',','.'))

    str_menu = json.dumps(menu)

    newList = list()

    # Listeyi Cek, For'da dondur, yeni liste olustur
    # eger ayni urunden varsa yeni liseteye ekleme, eski urunleri tekrar yeni listeye ekle
    # sessionu sil ve yeni listeyi ekle

    
    # Daha once sepet session'u olusturulmus mu?
    if "cart" in request.session:
        productList = request.session['cart']

        # Eklenen urunu yeni listeye ekleme
        for product in productList:
            if product['id'] == menu['id'] and product['options'] == menu['options']:
                pass
            else:
                newList.append(product)
        
        request.session['cart'] = newList


    data = {'OK':'OK'}
    return JsonResponse(data)


def update_count_view(request):

    productId = request.POST.get('id', '')
    productCount = request.POST.get('count', '')
    productPrice = request.POST.get('price', '')
    productOptions = request.POST.get('option', '')
    # Option String List to Normal List
    if(productOptions != '-1'):
        productOptions = ast.literal_eval(productOptions)


    menu = {}
    menu['id'] = int(productId)
    menu['price'] = float(productPrice)
    menu['count'] = int(productCount)
    menu['options'] = productOptions
    menu['totalPrice'] = float(productPrice.replace(',','.'))

    str_menu = json.dumps(menu)

    newList = list()

    # Listeyi Cek, For'da dondur, yeni liste olustur
    # eger ayni urunden varsa yeni liseteye ekleme, eski urunleri tekrar yeni listeye ekle
    # sessionu sil ve yeni listeyi ekle

    
    # Daha once sepet session'u olusturulmus mu?
    if "cart" in request.session:
        productList = request.session['cart']

        # Eklenmis olan urunu listeden bul
        for product in productList:
            # product = json.loads(product)
            if product['id'] == menu['id'] and product['options'] == menu['options']:
                # Edit Already Saved Product Count
                product['count'] = menu['count']
                product['totalPrice'] = float(product['price']) * product['count']
                newList.append(product)
            else:
                newList.append(product)
        
        request.session['cart'] = newList


    data = {'OK':'OK'}
    return JsonResponse(data)


def count_view(request):

    count = 0
    
    if "cart" in request.session:
        result = request.session["cart"]
        for item in result:
            print(item)
            count += item['count']

    else:
        result = False

    data = {'result':count}
    return JsonResponse(data)


def delete_session_view(request):
    if "cart" in request.session:
        del request.session['cart']
        data = {'result':'success'}
    else:
        data = {'result':'nothing'}
    return JsonResponse(data)