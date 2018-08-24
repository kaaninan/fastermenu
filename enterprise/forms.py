from django import forms

from PIL import Image
import tempfile
from .models import Enterprise


class EnterpriseForm(forms.ModelForm):
	logo = forms.ImageField(required=False, label='Firmanınızın logosu')
	name = forms.CharField(max_length=30, required=False, label='Firmanınızın adı')
	address = forms.CharField(max_length=200, required=False, label='Firmanınızın adresi', help_text='Bu kısım, sipariş ekranınıda firma isminizin altında görünür.')

	logo_x = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_y = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_width = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_height = forms.IntegerField(required=False, widget = forms.HiddenInput())

	class Meta:
		model = Enterprise
		fields = ('logo', 'name', 'address' )


	def save(self):
		form = super(EnterpriseForm, self).save()

		name = self.cleaned_data.get('name')

		x = self.cleaned_data.get('logo_x')
		y = self.cleaned_data.get('logo_y')
		w = self.cleaned_data.get('logo_width')
		h = self.cleaned_data.get('logo_height')

		image = Image.open(form.logo)
		cropped_image = image.crop((x, y, w+x, h+y))
		resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
		
		tmpfile = tempfile.TemporaryFile()
		resized_image.save(tmpfile, 'PNG', quality=100)

		form.logo.save(name + '_logo.png', tmpfile)

		return form