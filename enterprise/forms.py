from django import forms

from PIL import Image
from django.utils.translation import ugettext as _
import tempfile, uuid
from .models import Enterprise


class EnterpriseForm(forms.ModelForm):

	logo = forms.ImageField(required=False, label=_('Your company logo'))
	name = forms.CharField(max_length=30, required=False, label=_('Your company name'))
	address = forms.CharField(max_length=200, required=False, label=_('Your company address'), help_text=_('This section appears under your company name on the order display.'))
	phone = forms.CharField(max_length=200, required=False, label=_('Your phone (for sms)'))
	# currency = forms.ChoiceField(widget=forms.Select(), choices=CURRENCY, label=_("Select Currency"), required=True)

	logo_x = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_y = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_width = forms.IntegerField(required=False, widget = forms.HiddenInput())
	logo_height = forms.IntegerField(required=False, widget = forms.HiddenInput())

	class Meta:
		model = Enterprise
		fields = ('logo', 'name', 'phone', 'address', 'currency' )


	def clean_logo(self):
		image = self.cleaned_data.get('logo', False)
		
		# Eger yeni resim yuklenmisse
		try:
			if image:
				if image._size > 4*1024*1024:
					raise ValidationError(_("The logo file cannot be larger than 4 mb!"))
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