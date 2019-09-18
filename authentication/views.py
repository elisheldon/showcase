from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from teacher.models import Teacher
from student.models import Student
from .forms import LoginForm, RegistrationForm

# Create your views here.
def index(request):
    form = LoginForm()
    return render(request, 'authentication/index.html', {'form': form})

def loginUser(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Hello logged in user!')
        else:
            messages.add_message(request, messages.ERROR, 'Your username or password is incorrect, please try again.')
            return HttpResponseRedirect(reverse('authentication:index'))
    else:
        messages.add_message(request, messages.ERROR, 'There was an error logging you in, please try again.')
        return HttpResponseRedirect(reverse('authentication:index'))

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:index'))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            userType = form.cleaned_data.get('userType')
            firstName = form.cleaned_data.get('firstName')
            lastName = form.cleaned_data.get('lastName')

            user = User.objects.create_user(username, email, password1)
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            if userType == 'student':
                student = Student(user = user)
                student.save()
                login(request, user)
                return HttpResponseRedirect(reverse('student:index'))
            elif userType == 'teacher':
                teacher = Teacher(user = user)
                teacher.save()
                login(request, user)
                return HttpResponseRedirect(reverse('teacher:index'))
    else:
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})