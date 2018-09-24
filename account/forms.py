from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _



class LoginForm(forms.ModelForm):
	
	class Meta:
		model = User
		fields = ('username', 'password', )

	def clean(self):
		cleaned_data = self.cleaned_data
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")

		user = authenticate(username=username, password=password)
		
		if user is None:
			raise forms.ValidationError(_('Your username or password does not match. Please check!'))
		else:
			return cleaned_data



class SignUpForm(UserCreationForm):
	enterprise = forms.CharField(max_length=100, required=True)
	
	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields.pop('password2')
	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', )




class ProfileUpdateForm(forms.ModelForm):
	email = forms.EmailField(max_length=254, help_text=_('Your e-mail address is also your username.'))
	first_name = forms.CharField(max_length=30, required=False, label=_('First Name'))
	last_name = forms.CharField(max_length=30, required=False, label=_('Last Name'))
	password1 = forms.CharField(max_length=100, required=False, label=_('New Password (optional)'), help_text=_('Your password must be at least 8 characters long.'), widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', )

	def clean_password1(self):
		password = self.cleaned_data.get("password1")
		if len(password) < 8 and password:
			raise forms.ValidationError(_("The password can not be less than 8 characters!"))
		return password