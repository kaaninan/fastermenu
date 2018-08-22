from django import forms

from .models import Enterprise


class EnterpriseForm(forms.ModelForm):
	logo = forms.ImageField(required=False, label='Firmanınızın logosu')
	name = forms.CharField(max_length=30, required=False, label='Firmanınızın adı')
	address = forms.CharField(max_length=200, required=False, label='Firmanınızın adresi', help_text='Bu kısım, sipariş ekranınıda firma isminizin altında görünür.')

	class Meta:
		model = Enterprise
		fields = ('logo', 'name', 'address' )