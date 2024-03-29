from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
import json
from PIL import Image
import pathlib
import magic
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
import requests
import logging

from .models import Student, Item, Link, Gallery, Photo, Document
from .forms import AddForm, SettingsForm
from teacher.models import School, Staff

logger = logging.getLogger(__name__)

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
    public_link = request.scheme + '://' + request.get_host() + '/student/view/' + request.user.username
    context = {
        'items': items,
        'name': request.user.first_name,
        'public': public,
        'link': public_link,
    }
    return render(request, 'student/portfolio.html', context)

def add(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    student = Student.objects.get(user = request.user)
    try:
        google_credentials = json.loads(student.google_credentials)
        googleOAuthToken = google_credentials['token']
    except:
        googleOAuthToken = ''
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            sub_item_type = form.cleaned_data.get('sub_item_type')
            
            if sub_item_type == 'link' or sub_item_type == 'drive' or sub_item_type == 'onedrive':
                linkType = ContentType.objects.get_for_model(Link)
                linkCount = Item.objects.filter(student = student, sub_item_type = linkType).count()
                if linkCount >= 100:
                    messages.add_message(request, messages.ERROR, _('Showcase currently has a limit of 100 links per account. Please remove one or more links from your Showcase, then try again.'))
                    context = {
                        'form': form,
                        'googleOAuthToken': googleOAuthToken,
                    }
                    logger.warn('limit_link_count')
                    return render(request, 'student/add.html', context)
                url = form.cleaned_data.get('url')
                image = form.cleaned_data.get('image')
                link = Link.objects.create(url = url, image = image)
                item = Item.objects.create(student = student, sub_item = link, title = title, description = description)
                if sub_item_type == 'link':
                    logger.info('add_link')
                elif sub_item_type == 'drive':
                    logger.info('add_gdrive')
                else:
                    logger.info('add_onedrive')
            if sub_item_type == 'gallery':
                galleryType = ContentType.objects.get_for_model(Gallery)
                galleryCount = Item.objects.filter(student = student, sub_item_type = galleryType).count()
                photoType = ContentType.objects.get_for_model(Photo)
                photoCount = Item.objects.filter(student = student, sub_item_type = photoType).count()
                if galleryCount >= 10 or photoCount >= 30:
                    messages.add_message(request, messages.ERROR, _('Showcase currently has a limit of 10 galleries and 30 photos per account. Please remove one or more galleries from your Showcase, then try again.'))
                    context = {
                        'form': form,
                        'googleOAuthToken': googleOAuthToken,
                    }
                    if photoCount >= 30:
                        logger.warn('limit_photo_count')
                    else:
                        logger.warn('limit_gallery_count')
                    return render(request, 'student/add.html', context)
                for file in request.FILES.getlist('photos'):
                    if file.size > 1024*1024*5:
                        messages.add_message(request, messages.ERROR, _('One of the photos you chose is too large. Please try again, making sure each photo is less than 5MB.'))
                        context = {
                            'form': form,
                            'googleOAuthToken': googleOAuthToken,
                        }
                        logger.warn('limit_photo_size')
                        return render(request, 'student/add.html', context)
                    try:
                        im = Image.open(file)
                        im.verify()
                    except:    
                        messages.add_message(request, messages.ERROR, _('One of the files you selected was not a valid image. Make sure you select only images to upload, and try again.'))
                        context = {
                            'form': form,
                            'googleOAuthToken': googleOAuthToken,
                        }
                        logger.warn('error_photo_valid')
                        return render(request, 'student/add.html', context)
                gallery = Gallery.objects.create()
                logger.info('add_gallery')
                for file in request.FILES.getlist('photos'):
                    photo = Photo.objects.create(image = file, parent_gallery = gallery)
                    logger.info('add_photo')
                    if not gallery.cover:
                        gallery.cover = photo
                        gallery.save()
                item = Item.objects.create(student = student, sub_item = gallery, title = title, description = description)
            if sub_item_type == 'document':
                documentType = ContentType.objects.get_for_model(Document)
                documentCount = Item.objects.filter(student = student, sub_item_type = documentType).count()
                if documentCount >= 20:
                    messages.add_message(request, messages.ERROR, _('Showcase currently has a limit of 20 documents per account. Please remove one or more documents from your Showcase, then try again.'))
                    context = {
                        'form': form,
                        'googleOAuthToken': googleOAuthToken,
                    }
                    logger.warn('limit_doc_count')
                    return render(request, 'student/add.html', context)
                file = request.FILES['file']
                if file.size > 1024*1024*2:
                    messages.add_message(request, messages.ERROR, _('The file you chose is too large. Please try again, making sure your file is less than 2MB.'))
                    form.data = form.data.copy()
                    form.data['title'] = ''
                    context = {
                        'form': form,
                        'googleOAuthToken': googleOAuthToken,
                    }
                    logger.warn('limit_doc_size')
                    return render(request, 'student/add.html', context)
                mime = magic.from_buffer(file.read(), mime=True)
                if mime not in ['application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.ms-powerpoint','application/vnd.openxmlformats-officedocument.presentationml.presentation','application/vnd.oasis.opendocument.text','application/vnd.oasis.opendocument.presentation','application/vnd.oasis.opendocument.spreadsheet','application/pdf','text/plain','text/csv','text/html','application/x-iwork-keynote-sffkey','application/x-iwork-pages-sffpages','application/x-iwork-numbers-sffnumbers']:
                    messages.add_message(request, messages.ERROR, _('The file type you chose is not currently allowed. Showcase accepts uploading documents, spreadsheets, presentations and PDFs. Please try again with another file type.'))
                    form.data = form.data.copy()
                    form.data['title'] = ''
                    context = {
                        'form': form,
                        'googleOAuthToken': googleOAuthToken,
                    }
                    logger.warn('error_doc_mime')
                    return render(request, 'student/add.html', context)
                extension = pathlib.Path(file.name).suffix
                if extension[1:] in ['doc','docx','odt','txt','pages']:
                    icon = 'fas fa-file-alt'
                elif extension[1:] in ['xls','xlsx','ods','numbers']:
                    icon = 'fas fa-file-excel'
                elif extension[1:] in ['ppt','pptx','key']:
                    icon = 'fas fa-file-powerpoint'
                elif extension[1:] == 'pdf':
                    icon = 'fas fa-file-pdf'
                elif extension[1:] in ['html','htm']:
                    icon = 'fas fa-file-code'
                else:
                    messages.add_message(request, messages.ERROR, _('The file type you chose is not currently allowed. Showcase accepts uploading documents, spreadsheets, presentations and PDFs. Please try again with another file type.'))
                    form.data = form.data.copy()
                    form.data['title'] = ''
                    context = {
                        'form': form,
                        'googleOAuthToken': googleOAuthToken,
                    }
                    logger.warn('error_doc_ext')
                    return render(request, 'student/add.html', context)
                document = Document.objects.create(file = file, icon = icon)
                item = Item.objects.create(student = student, sub_item = document, title = title, description = description)
                logger.info('add_doc')
            messages.add_message(request, messages.SUCCESS, _('Successfully added %(title)s to your portfolio.') % {'title': title})
            return HttpResponseRedirect(reverse('student:add'))
        else:
            context = {
                'form': form,
                'googleOAuthToken': googleOAuthToken,
            }
            return render(request, 'student/add.html', context)
    else:
        form = AddForm()
        context = {
            'form': form,
            'googleOAuthToken': googleOAuthToken,
        }
        if student.age < 13:
            messages.add_message(request, messages.INFO, _('Stay safe! Remember not to include any personal information when adding an item to your Showcase.'))
        return render(request, 'student/add.html', context)

def remove(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    item_id = json.loads(request.body)['item_id']
    student = Student.objects.get(user = request.user)
    try:
        item = Item.objects.get(pk = item_id, student = student)
    except:
        raise PermissionDenied
    logger.info('delete_item')
    item.sub_item.delete()
    return HttpResponse(status=202)

def gallery(request, item_id):
    item = Item.objects.get(pk = item_id)
    student = item.student
    public_view = False
    if not request.user.is_authenticated: # if the user isn't logged in
        public_view = student.pf_public
    teacher_view = False
    if student.school_code:
        school = School.objects.get(student_code = student.school_code)
        if request.user.groups.filter(name='staff').exists(): #if the viewing user is a staff member of any school
            staff = Staff.objects.get(user = request.user)
            if staff in school.staff.all():
                teacher_view = True
    self_view = False
    try:
        current_student = Student.objects.get(user = request.user)
        if item.student == current_student:
            self_view = True
    except:
        None    
    if not public_view and not self_view and not teacher_view:
        messages.add_message(request, messages.ERROR, _('That gallery does not exist or the student has set their Showcase to be private.'))
        return HttpResponseRedirect(reverse('authentication:index'))
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
    pf_public = json.loads(request.body)['public']
    student = Student.objects.get(user = request.user)
    try:
        student.pf_public = pf_public
        student.save()
    except:
        raise PermissionDenied
    if student.pf_public:
        logger.info('make_public_lock')
    return HttpResponse(status=202)

def view(request, username):
    try:
        student = Student.objects.get(user__username = username)
        teacher_view = False
        if student.school_code:
            school = School.objects.get(student_code = student.school_code)
            if request.user.groups.filter(name='staff').exists(): #if the viewing user is a staff member of any school
                staff = Staff.objects.get(user = request.user)
                if staff in school.staff.all():
                    teacher_view = True
                    logger.info('view_teacher')
        if student.pf_public:
            logger.info('view_public')
        if not student.pf_public and not teacher_view:
            raise ValueError('private') #just triggers the except below
    except:
        messages.add_message(request, messages.ERROR, _('That student does not exist or has set their Showcase to be private.'))
        return HttpResponseRedirect(reverse('authentication:index'))
    items = Item.objects.filter(student = student)
    context = {
        'items': items,
        'name': student.user.first_name,
    }
    return render(request, 'student/view.html', context)
       

def get_google_scopes(request):
    user = request.user
    student = Student.objects.get(user = user)
    if request.GET.get('scope') and not request.GET.get('code'):
        # scope set by Showcase code, lack of code param indicates this is not a successful callback from Google
        scopes = request.GET.get('scope').split(' ')
        flow = google_auth_oauthlib.flow.Flow.from_client_config(json.loads(os.environ['GOOGLE_CONFIG']), scopes)
        flow.redirect_uri = request.build_absolute_uri(reverse('student:get_google_scopes'))
        authorization_url, state = flow.authorization_url(include_granted_scopes='true', access_type='offline')
        response = HttpResponseRedirect(authorization_url)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    elif request.GET.get('code'):
        # code param indicates this is a successful callback from Google
        flow = google_auth_oauthlib.flow.Flow.from_client_config(json.loads(os.environ['GOOGLE_CONFIG']), request.GET.get('scope'))
        flow.redirect_uri = request.build_absolute_uri(reverse('student:get_google_scopes'))
        flow.fetch_token(code = request.GET.get('code'))
        credentials = flow.credentials
        student.google_credentials = json.dumps({'token': credentials.token, 'refresh_token': credentials.refresh_token, 'token_uri': credentials.token_uri, 'client_id': credentials.client_id, 'client_secret': credentials.client_secret, 'scopes': credentials.scopes})
        student.save()
        return HttpResponse('<script type="text/javascript">window.opener.launchGooglePicker("' + credentials.token + '");window.close()</script>')
    else:
        try:
            return HttpResponse(request.GET.get('error'))
        except:
            return HttpResponse('An unknown error occurred', status=500)

def settings(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    student = Student.objects.get(user = request.user)
    school = None
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            pf_public = form.cleaned_data.get('pf_public')
            if code and code != student.school_code:
                student.school_code = code
                school = School.objects.get(student_code = code)
                logger.info('change_student_code')
                messages.add_message(request, messages.SUCCESS, _('Successfully joined ') + school.name)
            elif code != student.school_code: # if the student removed their school code
                student.school_code = ''
                logger.info('remove_student_code')
                messages.add_message(request, messages.SUCCESS, _('Your account is no longer linked with a school.'))
            if pf_public != str(student.pf_public):
                student.pf_public = pf_public
                if pf_public == 'True':
                    messages.add_message(request, messages.SUCCESS, _('Your Showcase is now public'))
                    logger.info('make_public_settings')
                else:
                    messages.add_message(request, messages.SUCCESS, _('Your Showcase is now private'))
            student.save()
    else:
        form = SettingsForm(initial={'code': student.school_code, 'pf_public': student.pf_public})
    try:
        school = School.objects.get(student_code = student.school_code)
    except:
        None
    public_url = request.scheme + '://' + request.get_host() + '/student/view/' + request.user.username
    context = {
        'form': form,
        'school': school,
        'public_url': public_url,
    }
    return render(request, 'student/settings.html', context)

def pin(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    item_id = json.loads(request.body)['item_id']
    student = Student.objects.get(user = request.user)
    try:
        item = Item.objects.get(pk = item_id, student = student)
    except:
        raise PermissionDenied
    item.pinned = not item.pinned
    item.save()
    logger.info('pin_item')
    return HttpResponse(status=202)

def edit(request):
    if not student_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    item_id = json.loads(request.body)['item_id']
    print(item_id)
    item_title = json.loads(request.body)['item_title']
    item_description = json.loads(request.body)['item_description']
    student = Student.objects.get(user = request.user)
    try:
        item = Item.objects.get(pk = item_id, student = student)
    except:
        raise PermissionDenied
    if item_title != item.title or item_description != item.description:
        item.title = item_title
        item.description = item_description
        item.save()
        logger.info('edit_item')
        return HttpResponse(status=202)
    else:
        return HttpResponse(status=400)