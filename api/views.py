from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib import messages
import json, pickle, uuid

from enterprise.models import *
from barcode.models import *
from cart.models import *



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





# ================================= LINE ======================================================


def line_status(request):
	
	# Get Post Param
	id = request.POST.get('id', '')

	# Siparisi bul
	line = get_object_or_404(Line, id=id)


	data = {'lineStatus': line.isComplated}
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

	# messages.success(request, "İşlem Başarılı!")

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

	# messages.success(request, "İşlem Başarılı!")

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

	# messages.success(request, "İşlem Başarılı!")

	data = {'OK':'OK'}
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
				print(fieldItem['name'])
				subCatItem = MenuSubCategoryOption()
				subCatItem.subMenu = subCat
				subCatItem.name = fieldItem['name']
				subCatItem.price = fieldItem['price']
				subCatItem.save()

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

	# messages.success(request, "İşlem Başarılı!")

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
	if item.picture != '':
		data['picture'] = item.picture.url
	else:
		data['picture'] = 'none'

	# Get Options
	categories = list(MenuSubCategory.objects.filter(menu=item).values())
	for category in categories:
		options = MenuSubCategoryOption.objects.filter(subMenu=category['id'])
		category['options'] = list(options.values())
	data['options'] = categories

	# messages.success(request, "İşlem Başarılı!")

	data = {'details': data}
	return JsonResponse(data)