from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext as _

from student.models import Student
from .forms import AddForm

def student_check(request):
    # checks to see if the current user is in the students group
    isStudent = request.user.groups.filter(name='students').exists()
    if not isStudent:
        messages.add_message(request, messages.ERROR, _('You attempted to access a student page, but you are not a student. Log in as a student and try again.'))
    return isStudent

# Create your views here.
def index(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    return render(request, 'student/index.html')

def add(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            return HttpResponse(form.cleaned_data.get('url'))
    else:
        form = AddForm()
    return render(request, 'student/add.html', {'form': form})

