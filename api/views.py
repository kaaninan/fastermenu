from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
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

