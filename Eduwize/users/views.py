from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from eduwize_app.forms import UserCreationForm, StudentForm
from eduwize_app.models import Student

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '/')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect(next_url or 'eduwize_app:home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return redirect('eduwize_app:home')
    else:
        form = UserCreationForm
        context = {'form':form}
    return render(request, 'registration/register.html', context)

from eduwize_app.forms import RegistrationForm

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()

            student = Student.objects.create(
                user=user,
                profile_picture=form.cleaned_data['profile_picture'],
                bio=form.cleaned_data['bio'],
                date_of_birth=form.cleaned_data['date_of_birth']
            )

            login(request, user)
            return redirect('eduwize_app:home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

