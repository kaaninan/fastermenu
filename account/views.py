from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from account.forms import *
from account.models import *
from enterprise.models import *

def signup_view(request):
	
	# 1- Create Enterprise
	# 2- Create Acoount.Profile
	# 3- Create User

	if request.method == 'POST':
		form = SignUpForm(request.POST)
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
	else:
		form = SignUpForm()
	return render(request, 'registration/register.html', {'form': form})