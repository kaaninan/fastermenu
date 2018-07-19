from django import forms

from .models import Enterprise


class MenuForm(forms.ModelForm):
	# logo = forms.ImageField(required=False, label='Firmanınızın logosu')
	# name = forms.CharField(max_length=30, required=False, label='Firmanınızın adı')
	# size = forms.IntegerField(required=False, help_text='Firma büyüklüğü')

	class Meta:
		model = Menu
		fields = ('name', 'pictures', 'description', 'price', 'stock', 'category')