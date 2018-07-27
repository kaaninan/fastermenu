from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



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
			raise forms.ValidationError("Kullanıcı adınız veya parolanız uyuşmuyor. Lütfen kontrol ediniz!")
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
	email = forms.EmailField(max_length=254, help_text='Mail adresiniz aynı zamanda kullanıcı adınızdır.')
	first_name = forms.CharField(max_length=30, required=False, label='Adınız')
	last_name = forms.CharField(max_length=30, required=False, label='Soyadınız')
	password1 = forms.CharField(max_length=100, required=False, label='Yeni Şifre (İsteğe Bağlı)', help_text='Şifreniz en az 8 karakter olmalıdır.', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', )

	def clean_password1(self):
		password = self.cleaned_data.get("password1")
		if len(password) < 8 and password:
			raise forms.ValidationError("The password can not be less than 8 characters!")
		return password