from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from hashlib import sha1
import json
import logging

from teacher.models import Staff, School
from student.models import Student
from .forms import LoginForm, RegistrationForm, SocialForm
from student.views import student_check

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='students').exists():
            return HttpResponseRedirect(reverse('student:portfolio'))
        elif request.user.groups.filter(name='staff').exists():
            return HttpResponseRedirect(reverse('teacher:index'))
        else:
            return HttpResponseRedirect(reverse('authentication:social'))
    loginForm = LoginForm(prefix='login')
    registerForm = RegistrationForm(prefix='register')
    context = {
        'loginForm': loginForm,
        'registerForm': registerForm,
    }
    return render(request, 'authentication/index.html', context)

def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, prefix='login')
        print(form.data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if request.user.groups.filter(name='students').exists():
                    return HttpResponseRedirect(reverse('student:portfolio'))
                elif request.user.groups.filter(name='staff').exists():
                    return HttpResponseRedirect(reverse('teacher:index'))
                else:
                    logger.error('login_not_staff_or_student')
                    return HttpResponse('You are not a student or a staff member, something is wrong!')
            else:
                messages.add_message(request, messages.ERROR, _('Your username or password is incorrect, please try again.'))
                return HttpResponseRedirect(reverse('authentication:loginUser'))
        else:
            #messages.add_message(request, messages.ERROR, _('There was an error logging you in, please try again.'))
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('authentication:loginUser'))
    else:
        form = LoginForm(prefix='login')
        context = {
            'loginForm': form,
        }
        return render(request, 'authentication/login.html', context)

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
            age = form.cleaned_data.get('age')
            school_code = form.cleaned_data.get('school_code')
            user = get_user_model().objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name # this will be last initial if student is under 13 because of clean method on form
            if user_type == 'student':
                group = Group.objects.get(name='students')
                user.groups.add(group)
                user.save()
                student = Student.objects.create(user = user, age = age)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('student:portfolio'))
            elif user_type == 'staff':
                group = Group.objects.get(name='staff')
                user.groups.add(group)
                user.save()
                staff = Staff(user = user)
                staff.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if school_code:
                    school = School.objects.get(code = school_code)
                    school.staff.add(staff)
                    school.save()
                    return HttpResponseRedirect(reverse('teacher:index'))
                else:
                    return HttpResponseRedirect(reverse('teacher:schoolSearch'))
    else:
        form = RegistrationForm(prefix='register')
    return render(request, 'authentication/register.html', {'form': form})

def privacy(request):
    return render(request, 'authentication/privacy.html')

def terms(request):
    return render(request, 'authentication/terms.html')

def social(request):
    if request.method == 'POST':
        form = SocialForm(request.POST, prefix='register')
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            age = form.cleaned_data.get('age')
            school_code = form.cleaned_data.get('school_code')
            user = request.user
            if user_type == 'student':
                group = Group.objects.get(name='students')
                user.groups.add(group)
                if age < 13:
                    user.email = sha1(user.email.encode()).hexdigest()
                    user.last_name = user.last_name[0].upper()
                user.save()
                try:
                    student = Student.objects.create(user = user, age = age, school_code = school_code, google_credentials = json.dumps({'token': request.user.social_auth.get(provider='google-oauth2').extra_data['access_token']}))
                except:
                    student = Student.objects.create(user = user, age = age, school_code = school_code, azure_credentials = json.dumps({'token': request.user.social_auth.get(provider='microsoft-graph').extra_data['access_token']}))
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('student:portfolio'))
            elif user_type == 'staff':
                group = Group.objects.get(name='staff')
                user.groups.add(group)
                user.save()
                staff = Staff(user = user)
                staff.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if school_code:
                    school = School.objects.get(code = school_code)
                    school.staff.add(staff)
                    school.save()
                    return HttpResponseRedirect(reverse('teacher:index'))
                else:
                    return HttpResponseRedirect(reverse('teacher:schoolSearch'))
    else:
        form = SocialForm(prefix='register')
    return render(request, 'authentication/social.html', {'form': form})

def azure(request):
    response = HttpResponse(content='{"associatedApplications":[{"applicationId":"18c3c49f-bef0-495b-81bd-e0390698acf8"}]}', content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="microsoft-identity-association.json"'
    return response

def settings(request):
    if request.user.groups.filter(name='students').exists():
        return HttpResponseRedirect(reverse('student:settings'))
    elif request.user.groups.filter(name='staff').exists():
        return HttpResponseRedirect(reverse('teacher:settings'))
    else:
        return HttpResponseRedirect(reverse('authentication:index'))