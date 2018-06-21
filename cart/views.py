from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json, pickle
from menu.models import *
from menu.forms import *
import ast

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def cart_view(request):

    sEnterprise = request.session.get('enterprise', 'enterprise')
    sTable = request.session.get('table', 'table')

    enterprise = get_object_or_404(Enterprise, name=sEnterprise)


    data = {}

    # just return a JsonResponse
    return JsonResponse(data)




def add_view(request):

    productId = request.POST.get('id', '')
    productCount = request.POST.get('count', '')
    productPrice = request.POST.get('price', '')
    productOptions = request.POST.get('option', '')
    # Option String List to Normal List
    if(productOptions != '-1'):
        productOptions = ast.literal_eval(productOptions)

    # print(productId)
    # print(productCount)
    # print(productPrice)
    # print(productOptions)


    menu = {}
    menu['id'] = productId
    menu['price'] = productPrice
    menu['count'] = productCount
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
                product['count'] = int(product['count']) + int(menu['count'])
                product['totalPrice'] = float(product['price'].replace(',','.')) * int(product['count'])
                print('Ekleniyor..')
                print(product)
                print('...')
                added = True
                newList.append(product)
                break
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

    

    data = {'OK':'OK'}
    return JsonResponse(data)



def show_view(request):
    
    if "cart" in request.session:
        result = request.session["cart"]

    else:
        result = False

    data = {'result':result}
    return JsonResponse(data)



def delete_view(request):
    if "cart" in request.session:
        del request.session['cart']
        data = {'result':'success'}
    else:
        data = {'result':'nothing'}
    return JsonResponse(data)