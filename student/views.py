from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.exceptions import PermissionDenied
from json import loads
from PIL import Image

from student.models import Student, Item, Link, Gallery, Photo
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
    public = student.pf_public
    context = {
        'items': items,
        'name': request.user.first_name,
        'public': public
    }
    return render(request, 'student/portfolio.html', context)

def add(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            student = Student.objects.get(user = request.user)
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            sub_item_type = form.cleaned_data.get('sub_item_type')
            if sub_item_type == 'link':
                url = form.cleaned_data.get('url')
                image = form.cleaned_data.get('image')
                link = Link.objects.create(url = url, image = image)
                item = Item.objects.create(student = student, sub_item = link, title = title, description = description)
            if sub_item_type == 'gallery':
                for file in request.FILES.getlist('photos'):
                    if file.size > 1024*1024*5:
                        messages.add_message(request, messages.ERROR, _('One of the photos you chose is too large. Please try again, making sure each photo is less than 5MB.'))
                        return render(request, 'student/add.html', {'form': form})
                    try:
                        im = Image.open(file)
                        im.verify()
                    except:    
                        messages.add_message(request, messages.ERROR, _('One of the files you selected was not a valid image. Make sure you select only images to upload, and try again.'))
                        return render(request, 'student/add.html', {'form': form})
                gallery = Gallery.objects.create()
                for file in request.FILES.getlist('photos'):
                    photo = Photo.objects.create(image = file, parent_gallery = gallery)
                    if not gallery.cover:
                        gallery.cover = photo
                        gallery.save()
                item = Item.objects.create(student = student, sub_item = gallery, title = title, description = description)
            messages.add_message(request, messages.SUCCESS, _('Successfully added %(title)s to your portfolio.') % {'title': title})
            return HttpResponseRedirect(reverse('student:add'))
        else:
            return render(request, 'student/add.html', {'form': form})
    else:
        form = AddForm()
        student = Student.objects.get(user = request.user)
        if student.age < 13:
            messages.add_message(request, messages.INFO, _('Stay safe! Remember not to include any personal information when adding an item to your Showcase.'))
        return render(request, 'student/add.html', {'form': form})

def remove(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    item_id = loads(request.body)['item_id']
    student = Student.objects.get(user = request.user)
    try:
        item = Item.objects.get(pk = item_id, student = student)
    except:
        raise PermissionDenied
    item.sub_item.delete()
    return HttpResponse(status=204)

def gallery(request, item_id):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    student = Student.objects.get(user = request.user)
    item = Item.objects.get(pk = item_id, student = student)
    if not item:
        raise PermissionDenied
    gallery = Gallery.objects.get(item = item)
    photos = Photo.objects.filter(parent_gallery = gallery)
    context = {
        'item': item,
        'gallery': gallery,
        'photos': photos,
    }
    return render(request, 'student/gallery.html', context)

def public(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    pf_public = loads(request.body)['public']
    student = Student.objects.get(user = request.user)
    try:
        student.pf_public = pf_public
        print(pf_public)
        student.save()
    except:
        raise PermissionDenied
    return HttpResponse(status=202)

def view(request, username):
    try:
        student = Student.objects.get(user__username = username)
        if not student.pf_public:
            raise ValueError('private')
    except:
        messages.add_message(request, messages.ERROR, _('That student does not exist or has set their Showcase to be private.'))
        return HttpResponseRedirect(reverse('authentication:index'))
    items = Item.objects.filter(student = student)
    context = {
        'items': items,
        'name': student.user.first_name,
    }
    return render(request, 'student/view.html', context)

