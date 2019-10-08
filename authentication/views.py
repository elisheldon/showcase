from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

from teacher.models import Teacher
from student.models import Student
from .forms import LoginForm, RegistrationForm
from student.views import student_check

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='students').exists():
            return HttpResponseRedirect(reverse('student:portfolio'))
    loginForm = LoginForm(prefix='login')
    registerForm = RegistrationForm(prefix='register')
    context = {
        'loginForm': loginForm,
        'registerForm': registerForm,
    }
    return render(request, 'authentication/index.html', context)

def loginUser(request):
    form = LoginForm(request.POST, prefix='login')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if request.user.groups.filter(name='students').exists():
                return HttpResponseRedirect(reverse('student:portfolio'))
            elif request.user.groups.filter(name='teachers').exists():
                return HttpResponseRedirect(reverse('teachers:index'))
            else:
                return HttpResponse('You are not a student or a teacher.')
        else:
            messages.add_message(request, messages.ERROR, _('Your username or password is incorrect, please try again.'))
            return HttpResponseRedirect(reverse('authentication:index'))
    else:
        messages.add_message(request, messages.ERROR, _('There was an error logging you in, please try again.'))
        return HttpResponseRedirect(reverse('authentication:index'))

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:index'))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, prefix='register')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            user_type = form.cleaned_data.get('user_type')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            user = get_user_model().objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            if user_type == 'student':
                group = Group.objects.get(name='students')
                user.groups.add(group)
                user.save()
                student = Student.objects.create(user = user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('student:portfolio'))
            elif userType == 'teacher':
                group = Group.objects.get(name='teachers')
                user.groups.add(group)
                user.save()
                teacher = Teacher(user = user)
                teacher.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('teacher:index'))
    else:
        form = RegistrationForm(prefix='register')
    return render(request, 'authentication/register.html', {'form': form})

def privacy(request):
    return render(request, 'authentication/privacy.html')