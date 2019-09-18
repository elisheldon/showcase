from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext as _

from student.models import Student

def student_check(request):
    # checks to see if the current user is in the students group
    isStudent = request.user.groups.filter(name='students').exists()
    messages.add_message(request, messages.ERROR, _('You attempted to access a student page, but you are not a student. Log in as a student and try again.'))
    return isStudent

# Create your views here.
def index(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    return HttpResponse(f'Hello {request.user.first_name}!')

