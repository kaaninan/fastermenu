from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json, pickle, uuid

from enterprise.models import *
from barcode.models import *



# ================================= TABLE ==================================================



def table_create(request):

	postOption = request.POST.get('option', '')
	postData = request.POST.get('data', '')
	

	# Option could be add-multiple or add-single
	if postOption == 'add-multiple':
		
		for i in range(0, int(postData)):

			# First Create Unique Barcode ID
			barcodeID = barcode_create(request)
			barcodeID = json.loads(barcodeID.content.decode('ascii'))
			barcodeID = barcodeID['barcode']
			barcode = Barcode.objects.get(id=barcodeID)

			# Second Create Table Object
			table = Table()
			table.barcode = barcode
			table.name = i + 1
			table.active = True
			table.enterprise = request.user.profile.enterprise
			table.save()

	elif postOption == 'add-single':

		# First Create Unique Barcode ID
		barcodeID = barcode_create(request)
		barcodeID = json.loads(barcodeID.content.decode('ascii'))
		barcodeID = barcodeID['barcode']
		barcode = Barcode.objects.get(id=barcodeID)

		# Second Create Table Object
		table = Table()
		table.barcode = barcode
		table.name = postData
		table.active = True
		table.enterprise = request.user.profile.enterprise
		table.save()

	data = {'OK':'OK'}
	return JsonResponse(data)


def table_update(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')
	postName = request.POST.get('name', '')
	postStatus = request.POST.get('status', '')

	# Convert String to Bool
	if postStatus == 'true':
		postStatus = True
	else:
		postStatus = False

	# Get item from database and update
	item = Table.objects.get(id=postID)
	item.name = postName
	item.active = postStatus
	item.save()

	data = {'OK':'OK'}
	return JsonResponse(data)




def table_delete(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')

	# Get item from database and update
	item = Table.objects.get(id=postID)
	item.delete()

	data = {'OK':'OK'}
	return JsonResponse(data)




# ================================= BARCODE ==================================================


def barcode_create(request):

	# Create Unique Barcode

	loop = True
	while loop:
		# Create unique string
		uID = uuid.uuid4().hex[:5]

		# Check if it was saved before
		query = Barcode.objects.filter(barcode=uID).count()

		if query != 0:
			pass
		else:
			barcode = Barcode()
			barcode.barcode = uID
			barcode.active = True
			barcode.save()
			loop = False

	data = {'barcode': barcode.id}
	return JsonResponse(data)


# def show_view(request):
	
#     if "cart" in request.session:
#         result = request.session["cart"]

#     else:
#         result = False

#     data = {'result':result}
#     return JsonResponse(data)




# def delete_view(request):

#     productId = request.POST.get('id', '')
#     productCount = request.POST.get('count', '')
#     productPrice = request.POST.get('price', '')
#     productOptions = request.POST.get('option', '')
#     # Option String List to Normal List
#     if(productOptions != '-1'):
#         productOptions = ast.literal_eval(productOptions)

#     menu = {}
#     menu['id'] = int(productId)
#     menu['price'] = float(productPrice)
#     menu['count'] = int(productCount)
#     menu['options'] = productOptions
#     menu['totalPrice'] = float(productPrice.replace(',','.'))

#     str_menu = json.dumps(menu)

#     newList = list()

#     # Listeyi Cek, For'da dondur, yeni liste olustur
#     # eger ayni urunden varsa yeni liseteye ekleme, eski urunleri tekrar yeni listeye ekle
#     # sessionu sil ve yeni listeyi ekle

	
#     # Daha once sepet session'u olusturulmus mu?
#     if "cart" in request.session:
#         productList = request.session['cart']

#         # Eklenen urunu yeni listeye ekleme
#         for product in productList:
#             if product['id'] == menu['id'] and product['options'] == menu['options']:
#                 pass
#             else:
#                 newList.append(product)
		
#         request.session['cart'] = newList


#     data = {'OK':'OK'}
#     return JsonResponse(data)


# def update_count_view(request):

#     productId = request.POST.get('id', '')
#     productCount = request.POST.get('count', '')
#     productPrice = request.POST.get('price', '')
#     productOptions = request.POST.get('option', '')
#     # Option String List to Normal List
#     if(productOptions != '-1'):
#         productOptions = ast.literal_eval(productOptions)


#     menu = {}
#     menu['id'] = int(productId)
#     menu['price'] = float(productPrice)
#     menu['count'] = int(productCount)
#     menu['options'] = productOptions
#     menu['totalPrice'] = float(productPrice.replace(',','.'))

#     newList = list()

#     # Listeyi Cek, For'da dondur, yeni liste olustur
#     # eger ayni urunden varsa yeni liseteye ekleme, eski urunleri tekrar yeni listeye ekle
#     # sessionu sil ve yeni listeyi ekle

	
#     # Daha once sepet session'u olusturulmus mu?
#     if "cart" in request.session:
#         productList = request.session['cart']

#         # Eklenmis olan urunu listeden bul
#         for product in productList:
#             # product = json.loads(product)
#             if product['id'] == menu['id'] and product['options'] == menu['options']:
#                 # Edit Already Saved Product Count
#                 product['count'] = menu['count']

#                 # print('Product Price: '+ str(product['price']))
#                 # print('Product Count: '+ str(product['count']))
#                 # print('Product Total Price: '+ str(float(product['price']) * product['count']))

#                 product['totalPrice'] = float(product['price']) * product['count']
#                 newList.append(product)
#             else:
#                 newList.append(product)
		
#         request.session['cart'] = newList


#     data = {'OK':'OK'}
#     return JsonResponse(data)


# def count_view(request):

#     count = 0
	
#     if "cart" in request.session:
#         result = request.session["cart"]
#         for item in result:
#             print(item)
#             count += item['count']

#     else:
#         result = False

#     data = {'result':count}
#     return JsonResponse(data)



# # List Orders Page API for enterprise

# def get_line(request):

#     data = list(Line.objects.filter(enterprise=request.user.profile.enterprise).values())


#     for item in data:
#         item['table'] = Table.objects.get(id=item['table_id']).name
#         order = list(Order.objects.filter(line=item['id']).values())
#         item['order'] = []
#         for orderItem in order:
#             menu = Menu.objects.get(id=orderItem['menu_id'])
#             # orderObject = {}
#             orderItem['name'] = menu.name
#             # orderObject[''] = menu.name
#             item['order'].append(orderItem)
#         # item['table'] = item.table.name
#         # order = Order.objects.filter(line=item)
#         # item.order = order

#     # dictionaries = [ obj.as_dict() for obj in self.get_queryset() ]
#     # return HttpResponse(json.dumps({"data": data}), content_type='application/json')

#     return JsonResponse({'data':data})



# def line_set_complated(request):

#     item = request.POST.get('id','')

#     data = Line.objects.get(enterprise=request.user.profile.enterprise, id=item)

#     data.isComplated = True;
#     data.complatedDate = datetime.now()
#     data.save()

#     return JsonResponse({'status':'success'})


# def line_set_paid(request):

#     item = request.POST.get('id','')

#     data = Line.objects.get(enterprise=request.user.profile.enterprise, id=item)

#     data.isPaid = True;
#     data.paidDate = datetime.now()
#     data.save()

#     return JsonResponse({'status':'success'})


# def add_line_view(request):
#     cartSession = request.session['cart']

#     # Add Line
#     line = Line()
#     line.table = Table.objects.get(name=request.session.get('table', ''))
#     line.enterprise = Enterprise.objects.get(name=request.session.get('enterprise', ''))
#     line.orderDate = datetime.now();
#     line.save()

#     totalPrice = 0.0

#     # Add Orders
#     for item in cartSession:
#         # Create Order
#         menu = Menu.objects.get(id=item['id'])
#         order = Order()
#         order.menu = menu
#         order.count = item['count']
#         order.options = item['options']
#         order.price = item['price']
#         order.totalPrice = item['totalPrice']
#         order.line = line
#         order.enterprise = Enterprise.objects.get(name=request.session.get('enterprise', ''))

#         totalPrice += item['totalPrice']

#         # Add Readable Options

#         optionsReadable = ''

#         if order.options != '-1':
#             orderListOption = []
#             orderListDropadd = []
#             for op in order.options:
#                 op_object = SubMenuCategoryOption.objects.get(id=op)
#                 op_type = op_object.subMenu.type
#                 if op_type == 'option':
#                     print(op_object)
#                     orderListOption.append(op_object)
#                 elif op_type == 'dropadd':
#                     print(op_object)
#                     orderListDropadd.append(op_object)

#             if len(orderListOption) != 0:
#                 for index, item in enumerate(orderListOption):
#                     optionsReadable += item.name
#                     if index+1 != len(orderListOption):
#                         optionsReadable += ', '
#                     elif index+1 == len(orderListOption):
#                         optionsReadable += '\n'

#             if len(orderListDropadd) != 0:
#                 for index, item in enumerate(orderListDropadd):
#                     optionsReadable += item.name
#                     if index+1 != len(orderListDropadd):
#                         optionsReadable += ', '
#                     elif index+1 == len(orderListDropadd):
#                         optionsReadable += ' hariç'

#             order.optionsReadable = optionsReadable

#         else:
#             order.optionsReadable = order.menu.description

		
#         order.save();


#     line = Line.objects.get(id = line.id)
#     line.totalPrice = totalPrice
#     line.save()
	

#     data = {'OK':'OK'}
#     return JsonResponse(data)


# # Delete Shopping Cart on session

# def delete_session_view(request):
#     if "cart" in request.session:
#         del request.session['cart']
#         data = {'result':'success'}
#     else:
#         data = {'result':'nothing'}
#     return JsonResponse(data)