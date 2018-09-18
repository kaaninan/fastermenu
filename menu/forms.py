from django import forms

from .models import *


class MenuForm(forms.ModelForm):
	name = forms.CharField(max_length=30, required=True, label='Ürün Adı*')
	pictures = forms.ImageField(required=False, label='Ürün Resmi', help_text='Ürün resmi eklemeniz, müşterilerinizin ürünü satın alma ihtimalini arttırır. (Zorunlu değil)')
	description = forms.CharField(max_length=200, required=False, label='Ürün Açıklaması', help_text='"Acılı sos ile servis edilir", gibi bir açıklama yazabilirsiniz.')
	price = forms.FloatField(label='Ürün Fiyatı (TL)*', required=True)
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