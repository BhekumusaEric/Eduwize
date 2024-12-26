from django.shortcuts import render , redirect
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import *
from django.http import HttpResponseRedirect , Http404
from eduwize_app.forms import UserCreationForm , StudentForm
from eduwize_app.models import Student

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request , authenticated_user)
            return (redirect('/home.html'))
    else:
        form = UserCreationForm
        context = {'form':form}
    return render(request , 'registration/register.html' , context)

def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            # Save the new user
            user = user_form.save()

            # Automatically log the user in after successful signup
            login(request, user)

            # Create the student profile and link it to the user
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            # Redirect to profile page or any other page
            return redirect('eduwize_app/home.html')

    else:
        user_form = UserCreationForm()
        student_form = StudentForm()

    return render(request, 'registration/signup.html', {'user_form': user_form, 'student_form': student_form})

