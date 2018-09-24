from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import *


class MenuForm(forms.ModelForm):
	name = forms.CharField(max_length=30, required=True, label=_("Product Name*"))
	pictures = forms.ImageField(required=False, label=_('Picture'), help_text=_('Adding a product image increases the likelihood that your customers will buy the product. (Not required)'))
	description = forms.CharField(max_length=200, required=False, label=_('Description'), help_text=_('You can write a description, such as "chili sauce is served with."'))
	price = forms.FloatField(label=_('Price ($)'), required=True)
	# stock = forms.BooleanField(label='Ürün stokta mı?', initial=True)

	class Meta:
		model = Menu
		fields = ('name', 'pictures', 'description', 'price')



class BiotForm(forms.ModelForm):

	class Meta:
		model = Biot
		fields = ('menu', )

	def __init__(self, *args, **kwargs):
		self.enterprise = kwargs.pop('enterprise', None)
		super(BiotForm, self).__init__(*args, **kwargs)
		self.fields['menu'].queryset = Menu.objects.filter(enterprise=self.enterprise)