from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext as _
from django.conf import settings

from student.models import Student, Item, Link
from .forms import AddForm

def student_check(request):
    # checks to see if the current user is in the students group
    is_student = request.user.groups.filter(name='students').exists()
    if not is_student:
        messages.add_message(request, messages.ERROR, _('You attempted to access a student page, but you are not logged in as a student. Log in as a student and try again.'))
    return is_student

# Create your views here.
def portfolio(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    student = Student.objects.get(user = request.user)
    items = Item.objects.filter(student = student)
    context = {
        'items': items
    }
    return render(request, 'student/portfolio.html', context)

def add(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            item_type = form.cleaned_data.get('item_type')
            if item_type == 'link':
                url = form.cleaned_data.get('url')
                image = form.cleaned_data.get('image')# [delete me later if everything is working, otherwise keep everything before the hash AND after the closing bracket] if form.cleaned_data.get('image') else settings.STATIC_URL + 'student/default_images/link.svg'
                link = Link(url = url, image = image)
                link.save()
            student = Student.objects.get(user = request.user)
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            item = Item(student = student, item = link, title = title, description = description)
            item.save()
            return HttpResponseRedirect(reverse('student:add'))
    else:
        form = AddForm()
    return render(request, 'student/add.html', {'form': form})