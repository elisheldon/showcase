from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from student.models import Student

# Create your views here.
@login_required
def index(request):
    return HttpResponse('Hello student!')