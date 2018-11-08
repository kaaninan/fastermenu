from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import *


class MenuForm(forms.ModelForm):
	name = forms.CharField(max_length=30, required=True, label=_("Product Name*"))
	pictures = forms.ImageField(required=False, label=_('Picture'), help_text=_('Adding a product image increases the likelihood that your customers will buy the product. (Not required)'))
	description = forms.CharField(max_length=200, required=False, label=_('Description'), help_text=_('You can write a description, such as "chili sauce is served with."'))
	price = forms.FloatField(label=_('Price'), required=True)
	
	logo_x = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_y = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_width = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_height = forms.IntegerField(required=False, widget = forms.HiddenInput())


	def clean_pictures(self):
		image = self.cleaned_data.get('pictures', False)
		
		# Eger yeni resim yuklenmisse
		try:
			if image:
				if image._size > 4*1024*1024:
					raise ValidationError(_("The picture file cannot be larger than 4 mb!"))
				self._isNew = True
				return image
			else:
				raise ValidationError("Couldn't read uploaded image")
		except Exception as e:
			pass


	def save(self):
		form = super(EnterpriseForm, self).save()

		name = self.cleaned_data.get('name')

		x = self.cleaned_data.get('logo_x')
		y = self.cleaned_data.get('logo_y')
		w = self.cleaned_data.get('logo_width')
		h = self.cleaned_data.get('logo_height')

		# Eger yeni resim yuklenmisse kaydet
		try:
			if self._isNew:
				image = Image.open(form.logo)
				cropped_image = image.crop((x, y, w+x, h+y))
				resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
				
				tmpfile = tempfile.TemporaryFile()
				resized_image.save(tmpfile, 'PNG', quality=100)

				form.logo.save(name + '_logo_'+uuid.uuid4().hex[:5]+'.png', tmpfile)
		except Exception as e:
			pass

		return form


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