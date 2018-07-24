from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=254, label='Email Adresi', help_text='Lütfen geçerli bir mail adresi giriniz.', widget=forms.TextInput(attrs={'autocomplete': 'email'}))
	first_name = forms.CharField(max_length=30, required=True, label='Adınız', widget=forms.TextInput(attrs={'autocomplete': 'given-name'}))
	last_name = forms.CharField(max_length=30, required=True, label='Soyadınız', widget=forms.TextInput(attrs={'autocomplete': 'family-name'}))
	enterprise = forms.CharField(max_length=100, required=True, label='İşletmenizin adı')

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )


class ProfileForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	password1 = forms.CharField(max_length=100, required=False, help_text='Yeni sifre')
	password2 = forms.CharField(max_length=100, required=False, help_text='Tekrar Yeni Sifre')

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )


class ProfileUpdateForm(forms.ModelForm):
	email = forms.EmailField(max_length=254, help_text='Mail adresiniz aynı zamanda kullanıcı adınızdır.')
	first_name = forms.CharField(max_length=30, required=False, label='Adınız')
	last_name = forms.CharField(max_length=30, required=False, label='Soyadınız')
	password1 = forms.CharField(max_length=100, required=False, label='Yeni sifre', help_text='Şifreniz en az 8 karakter olmalıdır.')

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', )

	def clean_password1(self):
		password = self.cleaned_data.get("password1")
		if len(password) < 8 and password:
			raise forms.ValidationError("The password can not be less than 8 characters!")
		return password