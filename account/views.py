from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import password_reset

from account.forms import *
from account.models import *
from enterprise.models import *

def login_view(request):
	if  request.user.is_authenticated:
		return redirect('enterprise:index')

	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('enterprise:index')

	return render(request, 'registration/login.html', {'form': form})


def signup_view(request):
	
	# 1- Create Enterprise
	# 2- Create Acoount.Profile
	# 3- Create User

	if  request.user.is_authenticated:
		return redirect('enterprise:index')
	
	form = SignUpForm(request.POST or None)
	if form.is_valid():
		
		# Set username as a email
		user = form.save(commit=False)
		user.username = form.cleaned_data.get('email')
		user = form.save()

		# Create new Enterprise
		enterprise = Enterprise()
		enterprise.name = form.cleaned_data.get('enterprise')
		print (enterprise.name)
		enterprise.save()

		# Connect Enterprise to Acoounts.Profile model
		profile = Profile()
		profile.user = user
		profile.enterprise = enterprise
		profile.save()

		user.profile = profile
		user.save()

		raw_password = form.cleaned_data.get('password1')
		user = authenticate(username=user.username, password=raw_password)
		login(request, user)
		return redirect('enterprise:index')

	return render(request, 'registration/register.html', {'form': form})


from django.core.mail import send_mail



def forget_password_view(request):

	if  request.user.is_authenticated:
		return redirect('enterprise:index')


	if request.method == 'POST':
		form = PasswordResetForm({'email': request.POST.get('email','')})
		if form.is_valid():
			form.save(request=request, email_template_name='registration/password_reset_email.html', )
			return redirect('enterprise:password_reset_done')
	else:
		return render(request, 'registration/password_reset_form.html', {})
