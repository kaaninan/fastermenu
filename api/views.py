from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, QueryDict
from django.core import serializers
from django.contrib import messages
from django.db.models import Q
import json, pickle, uuid, ast, time, http.client, random
from django.utils.translation import ugettext as _
from django.core.serializers.json import DjangoJSONEncoder


from enterprise.models import *
from barcode.models import *
from cart.models import *



# ================================= CART ==================================================


def cart_add(request):

	productId = request.POST.get('id', '')
	productCount = request.POST.get('count', '')
	productPrice = request.POST.get('price', '') # not only price. price with added extra options
	productOptions = request.POST.get('option', '')
	displayAlert = request.POST.get('displayAlert', '') # For index.html jQuery
	# Option String List to Normal List
	if(productOptions != '-1'):
		productOptions = ast.literal_eval(productOptions)


	# Get menu from database
	# menu_db = Menu.objects.get(id=productId)

	menu = {}
	menu['id'] = int(productId)
	menu['price'] = (float(productPrice)/int(productCount))
	menu['count'] = int(productCount)
	menu['options'] = productOptions
	menu['totalPrice'] = float(productPrice)

	newList = list()

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

def cart_delete(request):

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

def cart_show(request):
	
	if "cart" in request.session:
		result = request.session["cart"]

	else:
		result = False

	data = {'result':result}
	return JsonResponse(data)

def cart_count(request):

	count = 0
	
	if "cart" in request.session:
		result = request.session["cart"]
		for item in result:
			count += item['count']

	else:
		result = False

	data = {'result':count}
	return JsonResponse(data)

def cart_update_count(request):

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
	menu['totalPrice'] = float(productPrice)

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

				print('Product Price: '+ str(product['price']))
				print('Product Count: '+ str(product['count']))
				print('Product Total Price: '+ str(float(product['price']) * product['count']))

				product['totalPrice'] = float(product['price']) * product['count']
				newList.append(product)
			else:
				newList.append(product)
		
		request.session['cart'] = newList


	data = {'status':'success'}
	return JsonResponse(data)

def cart_session_delete(request):
	# Delete Shopping Cart on session
	if "cart" in request.session:
		del request.session['cart']
	
	data = {'result':'success'}
	return JsonResponse(data)


def session_delete(request, option):
	if "line" in request.session and option == 'line':
		del request.session['line']

	if "cart" in request.session and option == 'cart':
		del request.session['cart']

	if "enterprise" in request.session and option == 'enterprise':
		del request.session['enterprise']

	if "table" in request.session and option == 'table':
		del request.session['table']
	
	data = {'result':'success'}
	return JsonResponse(data)




# ================================= ORDER ==================================================

# not used
def order_get(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get orders
	data = Line.objects.filter(id=postID, enterprise__id=postEnterprise).prefetch_related('order_set', 'comment_set').values(
    	'orderDate', 'complatedDate', 'paidDate', 'isComplated', 'isPaid', 'totalPrice',
    	'order__menu__name', 'order__count', 'order__totalPrice', 'order__optionsReadable', 'comment__comment', 'comment__commentDate'
	)

	data = {'result': list(data)}
	return JsonResponse(data)



# ================================= LINE ==================================================


def line_add(request, tip=0, payment='default'):
	cartSession = request.session['cart']

	# Get Enterprise, Table and Shopping List from Session

	# Add Line
	line = Line()
	table_obj = Table.objects.get(id=request.session.get('table', ''))
	enterprise_obj = Enterprise.objects.get(id=request.session.get('enterprise', ''))
	line.table = table_obj
	line.enterprise = enterprise_obj
	line.orderDate = datetime.now();
	line.save()

	totalPrice = 0.0

	# Add Orders
	for item in cartSession:
		# Create Order
		menu = Menu.objects.get(id=item['id'])
		order = Order()
		order.menu = menu
		order.count = item['count']
		order.options = item['options']
		order.price = item['price']
		order.totalPrice = item['totalPrice']
		order.line = line
		order.enterprise = enterprise_obj

		totalPrice += item['totalPrice']

		# Add Readable Options

		optionsReadable = ''

		if order.options != '-1':
			orderListOption = []
			orderListDropadd = []
			for op in order.options:
				op_object = MenuSubCategoryOption.objects.get(id=op)
				op_type = op_object.subMenu.type
				if op_type == 'option':
					orderListOption.append(op_object)
				elif op_type == 'dropadd':
					orderListDropadd.append(op_object)

			if len(orderListOption) != 0:
				for index, item in enumerate(orderListOption):
					optionsReadable += item.name
					if index+1 != len(orderListOption):
						optionsReadable += ', '
					elif index+1 == len(orderListOption):
						optionsReadable += '\n'

			if len(orderListDropadd) != 0:
				for index, item in enumerate(orderListDropadd):
					optionsReadable += item.name
					if index+1 != len(orderListDropadd):
						optionsReadable += ', '
					elif index+1 == len(orderListDropadd):
						optionsReadable += ' hariç'

			order.optionsReadable = optionsReadable

		else:
			# Add menu description for default
			# order.optionsReadable = order.menu.description
			pass

		
		order.save();

	totalPricewithTip = totalPrice + (totalPrice/100*tip)

	line = Line.objects.get(id = line.id)
	line.price = totalPrice
	line.tip = totalPrice/100*tip
	line.payment = payment
	line.totalPrice = totalPricewithTip
	line.save()
	

	data = {'line': str(line.id)}
	return JsonResponse(data)

def line_delete(request):
	item = request.POST.get('id','')
	edit = request.POST.get('edit','')
	data = get_object_or_404(Line, id=item)
	data.delete()
	if(edit == ''):
		request.session['deleteLine'] = 'success'

	# Delete session as well
	new_session = list()
	if "line" in request.session:
		for line_item in request.session['line']:
			if int(line_item['id']) != int(item):
				new_session.append(line_item)
		request.session['line'] = new_session

	return JsonResponse({'status':'success'})

def line_get(request):

	data = list()

	# Birden fazla order ayni line'da bulunuyor
	new_data = Order.objects.filter(enterprise=request.user.profile.enterprise).select_related('line', 'menu', 'line__table').values(
		'id', 'menu__name', 'count', 'optionsReadable', 'price', 'line__totalPrice', 'line__table__name', 'line__table__id', 'line__id',
		'line__orderDate', 'line__isComplated', 'line__isPaid', 'line__isCanceled'
	).order_by('-line__orderDate')

	# Ayni line a ait orderlari ayni yere koy
	d = {}
	for name in new_data:
	    key = name['line__id']
	    if key not in d:
	        d[key] = []
	    d[key].append(name)


	for key, value in d.items():
	    temp = [key,value]
	    data.append(temp)

	return JsonResponse({'data':data})


def line_get_for_printer(request):

	data = list()

	# Birden fazla order ayni line'da bulunuyor
	new_data = Order.objects.filter(enterprise=request.GET.get('enterprise', '')).select_related('line', 'menu', 'line__table').values(
		'id', 'menu__name', 'count', 'optionsReadable', 'price', 'line__totalPrice', 'line__table__name', 'line__table__id', 'line__id',
		'line__orderDate', 'line__isComplated', 'line__isPaid', 'line__isCanceled', 'line__payment', 'line__isPrinted'
	).order_by('-line__orderDate')[:5]

	# Ayni line a ait orderlari ayni yere koy
	d = {}
	for name in new_data:
	    key = name['line__id']
	    if key not in d:
	        d[key] = []
	    d[key].append(name)


	for key, value in d.items():
	    temp = [key,value]
	    data.append(temp)

	return JsonResponse({'data':data})


def line_set_complated(request):

	item = request.POST.get('id','')

	data = Line.objects.get(enterprise=request.user.profile.enterprise, id=item)

	data.isComplated = True;
	data.complatedDate = datetime.now()
	data.save()

	return JsonResponse({'status':'success'})


def line_set_complated_table(request):

	table_ID = request.POST.get('id','')
	options = request.POST.get('options','') # 'all' or 'lineID1, lineID2 ...'

	if options == 'all':
		fetch = Line.objects.filter(table_id=int(table_ID)).update(isComplated=True, isPaid=True, paidDate=datetime.now())

		return JsonResponse({'status':'success'})


	return JsonResponse({'status':'nothing'})

def line_set_paid(request):

	item = request.POST.get('id','')

	data = Line.objects.get(enterprise=request.user.profile.enterprise, id=item)

	data.isPaid = True;
	data.paidDate = datetime.now()
	data.save()

	return JsonResponse({'status':'success'})


def line_set_canceled(request):

	item = request.POST.get('id','')

	data = Line.objects.get(enterprise=request.user.profile.enterprise, id=item)

	data.isCanceled = True;
	data.canceledDate = datetime.now()
	data.save()

	return JsonResponse({'status':'success'})


def line_set_printed(request):

	item = request.GET.get('id','')
	enterprise = request.GET.get('enterprise','')

	data = Line.objects.get(enterprise=enterprise, id=item)

	data.isPrinted = True;
	data.save()

	return JsonResponse({'status':'success'})




# ================================= TABLE ==================================================


def table_create(request):

	postOption = request.POST.get('option', '')
	postData = request.POST.get('data', '')

	postClientName = request.POST.get('client_name', '')
	postClientPhone = request.POST.get('client_phone', '')
	postClientAddress = request.POST.get('client_address', '')

	msg = '' # Return message

	# Control Table Count
	tables = Table.objects.filter(enterprise=request.user.profile.enterprise).count()
	

	# Option could be add-multiple or add-single
	if postOption == 'add-multiple':

		if (tables + int(postData)) >= 51:
			msg = 'En fazla 50 tane masa ekleyebilirsiniz. Daha fazlası için bizimle iletişime geçin.'

		else:
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
			msg = 'success'

	elif postOption == 'add-single':

		if (tables + 1) >= 51:
			msg = 'En fazla 50 tane masa ekleyebilirsiniz. Daha fazlası için bizimle iletişime geçin.'

		else:
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

			messages.success(request, "İşlem Başarılı!")
			msg = 'success'


	elif postOption == 'add-client':
		if (tables + 1) >= 51:
			msg = 'En fazla 50 tane masa ekleyebilirsiniz. Daha fazlası için bizimle iletişime geçin.'

		else:
			# First Create Unique Barcode ID
			barcodeID = barcode_create(request)
			barcodeID = json.loads(barcodeID.content.decode('ascii'))
			barcodeID = barcodeID['barcode']
			barcode = Barcode.objects.get(id=barcodeID)

			# Second Create Table Object
			table = Table()
			table.barcode = barcode
			table.active = True

			table.name = postClientName
			table.client_name = postClientName
			table.client_phone = postClientPhone
			table.client_address = postClientAddress

			table.enterprise = request.user.profile.enterprise
			table.save()

			messages.success(request, "İşlem Başarılı!")
			msg = 'success'



	data = {'msg':msg}
	return JsonResponse(data)

def table_update(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')
	postName = request.POST.get('name', '')
	postStatus = request.POST.get('status', '')

	postClientName = request.POST.get('client_name', '')
	postClientPhone = request.POST.get('client_phone', '')
	postClientAddress = request.POST.get('client_address', '')

	# Convert String to Bool
	if postStatus == 'true':
		postStatus = True
	else:
		postStatus = False


	# Check Client
	if postClientName != '':
		# Get item from database and update
		item = Table.objects.get(id=postID)
		item.name = postName
		item.active = postStatus
		item.client_name = postClientName
		item.client_phone = postClientPhone
		item.client_address = postClientAddress
		item.save()
	else:
		# Get item from database and update
		item = Table.objects.get(id=postID)
		item.name = postName
		item.active = postStatus
		item.save()

	messages.success(request, "İşlem Başarılı!")

	data = {'OK':'OK'}
	return JsonResponse(data)

def table_delete(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')

	# Get item from database and update
	item = Table.objects.get(id=postID)
	item.delete()

	messages.success(request, "İşlem Başarılı!")

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



# ================================= LINE ======================================================


def line_status(request):
	
	# Get Post Param
	id = request.POST.get('id', '')

	# Siparisi bul
	line = Line.objects.filter(id=id)
	serialize = serializers.serialize("json", line)


	data = {'line': serialize}
	return JsonResponse(data)



# ================================= CATEGORY ==================================================


def category_create(request):

	postName = request.POST.get('name', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get Enterprise
	enterprise = Enterprise.objects.get(id=postEnterprise)
	
	# Save Category
	item = Category()
	item.name = postName
	item.enterprise = enterprise
	item.save()

	messages.success(request, "İşlem Başarılı!")

	data = {'OK':'OK'}
	return JsonResponse(data)

def category_update(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')
	postName = request.POST.get('name', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get Enterprise
	enterprise = Enterprise.objects.get(id=postEnterprise)

	# Get item from database and update
	item = Category.objects.get(id=postID, enterprise=enterprise)
	item.name = postName
	item.save()

	messages.success(request, "İşlem Başarılı!")

	data = {'OK':'OK'}
	return JsonResponse(data)

def category_delete(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get Enterprise
	enterprise = Enterprise.objects.get(id=postEnterprise)

	# Get item from database and update
	item = Category.objects.get(id=postID, enterprise=enterprise)
	item.delete()

	messages.success(request, "İşlem Başarılı!")

	data = {'OK':'OK'}
	return JsonResponse(data)


def category_order(request):

	# Get Post Parameters
	postList = request.POST.get('list', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get Enterprise
	enterprise = Enterprise.objects.get(id=postEnterprise)

	d = json.loads(postList)
	
	for item in d:
		# Get item from database and update
		category = Category.objects.get(id=d[item], enterprise=enterprise)
		category.ordering = int(item)
		category.save()

	messages.success(request, "İşlem Başarılı!")

	data = {'status':'success'}
	return JsonResponse(data)



# ================================= MENU ==================================================


def menu_create(request):

	# ===================== GET DATA ====================

	postName = request.POST.get('name', '')
	postDescription = request.POST.get('description', '')
	postPicture = request.FILES.get('pictures', '')
	postPrice = request.POST.get('price', '')
	postStock = request.POST.get('stock', '')
	postCategory = request.POST.get('category', '')
	postEnterprise = request.POST.get('enterprise', '')
	postOptions = list()

	# Convert String to Bool
	if postStock == 'on':
		postStock = True
	else:
		postStock = False



	# Get Options as a List
	for key, item in request.POST.items():

		# Get Options
		# 1- optionName-X
		# 2- optionType-X
		# 3- optionFields-X (Dropadd)
		# 3- optionFields-X-p (Option)

		if 'optionName' in key:

			# key = optionName-0 or optionName-1
			params = key.split('-')

			optionName = item

			# Get Related optionType (only one for this optionName)
			optionType = request.POST['optionType-'+params[1]]
			optionFields = []

			if optionType == 'dropadd':

				# Get Field List (only one for this optionName) it is a list
				stt = 'optionFields-'+params[1]+'[]'
				for fieldItem in request.POST.getlist(stt):
					if fieldItem != '': # Sometimes it's empty, for any reason. I dont know yet :( (on jQuery side)
						objField = {}
						objField['name'] = fieldItem
						objField['price'] = 0
						optionFields.append(objField)


			elif optionType == 'option':

				# Get Field List (only one for this optionName) it is a list
				stt = 'optionFields-'+params[1]+'-p[]'

				# example data: ['1 Porsiyon', '0', '2 Porsiyon', '20']
				# [0] => Name - [1] => Price & [2] => Name - [3] => Price

				idx = 0
				for fieldItem in request.POST.getlist(stt):
					if idx % 2 == 0:
						name = fieldItem
						price = request.POST.getlist(stt)[idx+1]

						# Empty Control
						if price == '':
							price = 0

						objField = {}
						objField['name'] = name
						objField['price'] = price
						optionFields.append(objField)
					idx += 1

			# Create temp object and append postOption
			tempList = {}
			tempList['name'] = optionName
			tempList['type'] = optionType
			tempList['fields'] = optionFields
			postOptions.append(tempList)

	# ===================== END: GET DATA ====================


	# Get Enterprise & Category
	enterprise = Enterprise.objects.get(id=int(postEnterprise))
	category = Category.objects.get(id=int(postCategory))

	# Save Menu
	item = Menu()
	item.name = postName
	item.description = postDescription
	item.picture = postPicture
	item.price = float(postPrice)
	item.stock = postStock
	item.category = category
	item.enterprise = enterprise
	item.save()

	# Save SubCategories if exists
	if len(postOptions) > 0:
		for optionItem in postOptions:
			subCat = MenuSubCategory()
			subCat.name = optionItem['name']
			subCat.type = optionItem['type']
			subCat.menu = item
			subCat.enterprise = enterprise
			subCat.save()

			for fieldItem in optionItem['fields']:
				subCatItem = MenuSubCategoryOption()
				subCatItem.subMenu = subCat
				subCatItem.name = fieldItem['name']
				subCatItem.price = fieldItem['price']
				subCatItem.save()

	messages.success(request, _('Successful!'))

	data = {'OK':'OK'}
	return JsonResponse(data)

def menu_update(request):

	# Update Yapilirken;
	#	Belirtilen menu silinmez - Menuye bagli olan MenuSub ve MenuSubOption'lar silinir
	#	Menu guncellenir (id ayni kalir)
	#	Menu Sub Category guncellenir (id ler degisir)
	#	Menu Sub Category Options guncellenir (id ler degisir)

	
	# ===================== GET DATA ====================

	postID = request.POST.get('id', '')
	postName = request.POST.get('name', '')
	postDescription = request.POST.get('description', '')
	postPicture = request.FILES.get('pictures', '')
	postPrice = request.POST.get('price', '')
	postStock = request.POST.get('stock', '')
	postCategory = request.POST.get('category', '')
	postEnterprise = request.POST.get('enterprise', '')
	postOptions = list()

	# Convert String to Bool
	if postStock == 'on':
		postStock = True
	else:
		postStock = False



	# Get Options as a List
	for key, item in request.POST.items():

		# Get Options
		# 1- optionId-X
		# 1- optionName-X
		# 2- optionType-X
		# 3- optionFields-X (Dropadd)
		# 3- optionFields-X-p (Option)

		if 'optionName' in key:

			# key = optionName-0 or optionName-1
			params = key.split('-')

			optionName = item

			# Get Related optionType (only one for this optionName)
			optionId = request.POST['optionId-'+params[1]]
			optionType = request.POST['optionType-'+params[1]]
			optionFields = []

			if optionType == 'dropadd':

				# Get Field List (only one for this optionName) it is a list
				stt = 'optionFields-'+params[1]+'[]'
				for key, fieldItem in enumerate(request.POST.getlist(stt)):
					if fieldItem != '': # Sometimes it's empty, for any reason. I dont know yet :( (on jQuery side)
						# Get ID from another list
						stt = 'optionFieldsId-'+params[1]+'[]'
						listIds = request.POST.getlist(stt)

						objField = {}
						objField['id'] = listIds[key]
						objField['name'] = fieldItem
						objField['price'] = 0
						optionFields.append(objField)


			elif optionType == 'option':

				# Get Field List (only one for this optionName) it is a list
				stt = 'optionFields-'+params[1]+'-p[]'
				sti = 'optionFieldsId-'+params[1]+'-p[]'

				# example data: ['1 Porsiyon', '0', '2 Porsiyon', '20']
				# [0] => Name - [1] => Price & [2] => Name - [3] => Price

				# GET ID
				# example data: ['213', '431']
				# fields[0]+[1] => [0]
				# fields[2]+[3] => [1]
				# fields[4]+[5] => [2]
				# F = firstFieldKey / 2 = idList[key]

				idx = 0
				for fieldItem in request.POST.getlist(stt):
					if idx % 2 == 0:
						name = fieldItem
						price = request.POST.getlist(stt)[idx+1]
						id = request.POST.getlist(sti)[int(idx/2)]

						# Empty Control
						if price == '':
							price = 0

						objField = {}
						objField['id'] = id
						objField['name'] = name
						objField['price'] = price
						optionFields.append(objField)
					idx += 1

			# Create temp object and append postOption
			tempList = {}
			tempList['id'] = optionId
			tempList['name'] = optionName
			tempList['type'] = optionType
			tempList['fields'] = optionFields
			postOptions.append(tempList)

	# ===================== END: GET DATA ====================


	# Get Enterprise & Category
	enterprise = Enterprise.objects.get(id=int(postEnterprise))
	category = Category.objects.get(id=int(postCategory))


	# Update Menu Details
	item = get_object_or_404(Menu, id=postID)
	item.name = postName
	item.description = postDescription
	if postPicture != '':
		item.picture = postPicture
	item.price = float(postPrice)
	item.stock = postStock
	item.category = category
	item.enterprise = enterprise
	item.save()

	# Delete MenuSubCategories, automatically deleting SubOptions
	MenuSubCategory.objects.filter(enterprise=enterprise, menu=item).delete()

	# Update SubCategories
	if len(postOptions) > 0:
		for optionItem in postOptions:
			subCat = MenuSubCategory()
			subCat.name = optionItem['name']
			subCat.type = optionItem['type']
			subCat.menu = item
			subCat.enterprise = enterprise
			subCat.save()

			for fieldItem in optionItem['fields']:
				subCatItem = MenuSubCategoryOption()
				subCatItem.subMenu = subCat
				subCatItem.name = fieldItem['name']
				subCatItem.price = fieldItem['price']
				subCatItem.save()


	messages.success(request, "İşlem Başarılı!")

	data = {'OK':'OK'}
	return JsonResponse(data)

def menu_delete(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get Enterprise
	enterprise = Enterprise.objects.get(id=postEnterprise)

	# Get item from database and update
	item = Menu.objects.get(id=postID, enterprise=enterprise)
	item.delete()

	messages.success(request, "İşlem Başarılı!")

	data = {'OK':'OK'}
	return JsonResponse(data)

def menu_get(request):

	# Get Post Parameters
	postID = request.POST.get('id', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get Enterprise
	enterprise = Enterprise.objects.get(id=postEnterprise)

	# Get item from database
	item = Menu.objects.get(id=postID, enterprise=enterprise)

	data = {}
	data['name'] = item.name
	data['description'] = item.description
	data['price'] = item.price
	data['id'] = item.id
	data['stock'] = item.stock
	if item.picture:
		data['picture'] = item.picture.url
	else:
		data['picture'] = 'none'

	# Get Options
	categories = list(MenuSubCategory.objects.filter(menu=item).values())
	for category in categories:
		options = MenuSubCategoryOption.objects.filter(subMenu=category['id'])
		category['options'] = list(options.values())
	data['options'] = categories


	data = {'details': data}
	return JsonResponse(data)



# ================================= BIOT ==================================================

def biot_order(request):

	# API[source] => Connect FM Database get Table object and get Menu object
	

	# Get Post Parameters
	postEnterprise = request.GET.get('enterprise', '')
	postSource = request.GET.get('source', '')

	# Get Enterprise
	# enterprise = Enterprise.objects.get(id=postEnterprise)

	# Get Table
	table = Table.objects.get(id=postSource)
	enterprise = table.enterprise

	# Get Selected Menu
	menu = Biot.objects.filter(enterprise=enterprise)

	if menu.count() == 0:
		data = {'status': 'error', 'message':'menu not found'}
		return JsonResponse(data)
	
	else:
		# This is example menu DRAFT BAR - ORDEK
		dict = {'id': menu[0].menu.id, 'count': '1', 'price': str(menu[0].menu.price), 'option':'-1'}
		request.session['enterprise'] = enterprise.id
		request.session['table'] = postSource
		qdict = QueryDict('', mutable=True)
		qdict.update(dict)
		request.POST = qdict

		# Add Cart & Session
		cart_add(request)

		# Line Add
		line_id = line_add(request)
		payload = json.loads(line_id.content)

		biotlog = BiotLog()
		biotlog.enterprise = enterprise
		biotlog.table = table
		biotlog.line = Line.objects.get(id=payload['line'])
		biotlog.save()


		# Delete Shopping List from Session
		session_delete(request, 'cart')

		data = {'status': 'success'}
		return JsonResponse(data)


def biot_hepsiburada(request):

	# API[source] => Connect FM Database get Table object and get Menu object

	# Get Post Parameters
	postClient = request.GET.get('client', '')
	postOption = request.GET.get('option', '')

	def send_sms(message, phones):
	  sms_msg = {
	    'username' : '908505325216', # https://oim.verimor.com.tr/sms_settings/edit adresinden öğrenebilirsiniz.
	    'password' : 'BulutYazilim', # https://oim.verimor.com.tr/sms_settings/edit adresinden belirlemeniz gerekir.
	    'source_addr' : '08505325216', # Gönderici başlığı, https://oim.verimor.com.tr/headers adresinde onaylanmış olmalı, değilse 400 hatası alırsınız.
	    'messages' : [
	      {'msg': message, 'dest': phones}
	    ]
	  }

	  sms_msg = json.dumps(sms_msg)

	  conn = http.client.HTTPConnection('sms.verimor.com.tr', 80)
	  request_headers = {'Content-type': 'application/json'}
	  conn.request("POST", "/v2/send.json", sms_msg, request_headers)
	  response = conn.getresponse()
	  print(response.status, response.reason)


	  if response.status == 200:
	    data = response.read()
	    conn.close
	    return data
	  else:
	    conn.close
	    return False

	message = postClient

	if postOption == '1':
		message += ", https://www.hepsiburada.com/ariel-dag-esintisi-beyazlar-icin-9-kg-parlak-renkler-9-kg-toz-camasir-deterjani-p-HBV000007M8CD?magaza=Online%20Market - "
	else:
		message += ', https://www.hepsiburada.com/finish-bulasik-makinesi-deterjani-200-lu-hepsi-bir-arada-tablet-100x2-p-HBV00000BSK7T?magaza=Online%20Market - '

	message += str(random.randint(1,101))
	
	dest = "905309263819"

	# if postClient == 'Kagan':
	# 	dest = "905309263819"
	# elif postClient == 'Huseyin':
	# 	dest = "905327342028"
	# elif postClient == 'Orhan':
	# 	dest = "905323580404"
	# elif postClient == 'Evren':
	# 	dest = "905332821140"
	# elif postClient == 'Mutlu':
	# 	dest = "905322552998"
	# elif postClient == 'Other':
	# 	dest = "905309263819"

	if postClient == 'Other':
		dest = "905309263819"
	else:
		dest = "905309263819", "905322552998", "905332821140", "905323580404", "905327342028"
		
	campaign_id = send_sms(message, dest)
	if campaign_id == False:
	  campaign_id = "Fail"
	  print("Mesaj gönderilemedi.")
	else:
	  campaign_id = "success"
	  print("Kampanya ID:", campaign_id)


	comment = HPLog()
	comment.comment = campaign_id + ' - ' + postClient
	comment.save()

	data = {'status': campaign_id, 'client': postClient, 'option': postOption}
	return JsonResponse(data)


# ================================= WAITER CALL ===============================================


def waiter_call_create(request):

	postTable = request.POST.get('table', '')
	postEnterprise = request.POST.get('enterprise', '')

	# Get Enterprise
	enterprise = Enterprise.objects.get(id=postEnterprise)
	table = Table.objects.get(id=postTable)

	# Save Category
	item = Waiter()
	item.calledDate = datetime.now()
	item.table = table
	item.enterprise = enterprise
	item.save()

	data = {'status':'success'}
	return JsonResponse(data)

def waiter_call_complate(request):
	postID = request.POST.get('id', '')

	# Get item from database and update
	item = Waiter.objects.get(id=postID)
	item.complatedDate = datetime.now()
	item.isComplated = True
	item.save()

	data = {'status':'success'}
	return JsonResponse(data)





def waiter_call_list(request):
	postEnterprise = request.GET.get('enterprise', '')
	data = Waiter.objects.filter(enterprise__id=postEnterprise, isComplated=False).select_related('table').values('table__name', 'isComplated', 'id')
	serialize = json.dumps(list(data), cls=DjangoJSONEncoder)
	data = {'data':serialize}
	return JsonResponse(data)




