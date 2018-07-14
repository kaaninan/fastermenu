from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	enterprise = forms.CharField(max_length=100, required=True, help_text='İşletmenizin adı')

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )