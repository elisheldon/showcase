from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.translation import gettext as _
from django.urls import reverse
import csv
import os
import random
import string

from .forms import SchoolSearchForm, AddSchoolForm, SettingsForm
from .models import School, Staff
from student.models import Student

def teacher_check(request):
    # checks to see if the current user is in the staff group
    is_teacher = request.user.groups.filter(name='staff').exists()
    if not is_teacher:
        messages.add_message(request, messages.ERROR, _('You attempted to access a staff page, but you are not logged in as a staff member. Log in as a staff member and try again.'))
    return is_teacher

# Create your views here.
def index(request):
    if not teacher_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    staff = Staff.objects.get(user = request.user)
    schools = School.objects.filter(staff = staff)
    school = schools.first()
    if schools.count() == 0:
        return HttpResponseRedirect(reverse('teacher:schoolSearch'))
    students = Student.objects.filter(school_code = school.student_code)
    context = {
        'school': school,
        'students': students,
    }
    return render(request, 'teacher/students.html', context)

def schoolSearch(request):
    if not teacher_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    if request.method == 'POST':
        form = SchoolSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip = form.cleaned_data.get('zip')
            schools = School.objects.filter(name__icontains=name, city__icontains=city, state__icontains=state, zip__contains=zip)[:100]
            error = ''
            if schools.count() == 0:
                error = _('No schools found matching your search.')
            context = {
            'form': form,
            'schools': schools,
            'error': error,
            }
            return render(request, 'teacher/school_search.html', context)
    else:
        form = SchoolSearchForm()
    context = {
        'form': form
    }
    return render(request, 'teacher/school_search.html', context)

def addSchool(request):
    if not teacher_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    if request.method == 'POST':
        form = AddSchoolForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip = form.cleaned_data.get('zip')
            country = form.cleaned_data.get('country')
            similar_name_schools = School.objects.filter(name__icontains=name, city__icontains=city)
            similar_address_schools = School.objects.filter(address__icontains=address, city__icontains=city)
            similar_schools = similar_name_schools | similar_address_schools
            if similar_schools.count() == 0 or form.cleaned_data.get('confirmed'):
                newschool = School(name=name, address=address, city=city, state=state, country=country, zip=zip)
                newschool.save()
                return HttpResponseRedirect(reverse('teacher:schoolDetails', args={newschool.id}))
            else:
                similar_schools_distinct = similar_name_schools.distinct()
                form.data = form.data.copy()
                form.data['confirmed'] = True #next time the user hits submit, it will create the school regardless of possible matches
                context = {
                    'form': form,
                    'schools': similar_schools_distinct,
                }
                return render(request, 'teacher/add_school.html', context)
    else:
        form = AddSchoolForm()
    context = {
        'form': form
    }
    return render(request, 'teacher/add_school.html', context)

def schoolDetails(request, id):
    if not teacher_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    try:
        school = School.objects.get(id=id)
    except:
        raise Http404('School does not exist')
    staff = Staff.objects.get(user = request.user)
    schools_owned = School.objects.filter(owners = staff)
    already_owned = schools_owned.count() > 0
    try:
        context = {
            'school': school,
            'owner_name': school.owners.first().user.first_name + ' ' + school.owners.first().user.last_name,
            'owner_email': school.owners.first().user.email,
            'already_owned': already_owned,
        }
    except:
        context = {
            'school': school,
            'already_owned': already_owned,
        }
    return render(request, 'teacher/school_details.html', context)

@require_http_methods(['POST'])
def createSchoolCode(request):
    if not teacher_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    id = request.POST['id']
    try:
        school = School.objects.get(id=id)
    except:
        raise Http404('School does not exist')
    staff = Staff.objects.get(user = request.user)
    schools_owned = School.objects.filter(owners = staff)
    if schools_owned.count() == 0:
        # only allow one school per staff (for now, though the model is set up as manytomany for future expansion)
        random_code_is_unique = False
        while not random_code_is_unique:
            random_code = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
            try:
                school_with_code = School.objects.get(code = random_code)
            except:
                random_code_is_unique = True
        school.code = random_code
        random_student_code_is_unique = False
        while not random_student_code_is_unique:
            random_student_code = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
            try:
                school_with_student_code = School.objects.get(student_code = random_student_code)
            except:
                random_student_code_is_unique = True
        school.student_code = random_student_code
        school.owners.add(staff)
        school.staff.add(staff)
        school.save()
        context = {
            'school': school,
        }
        return render(request, 'teacher/school_code.html', context)
    else:
        messages
        return HttpResponse('A single account cannot create codes for multiple schools.')

@staff_member_required
def loadSchools(request):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/static/teacher/nces_us_schools.csv', newline='') as csvfile:
        schools = csv.DictReader(csvfile)
        ### non-bulk creation for sqlite
        #for school in schools:
            #newschool = School(name=school['name'], external_id=school['external_id'], address=school['address'], city=school['city'], state=school['state'], country='United States of America', zip=school['zip'])
            #newschool.save()

        ### bulk creation for postgresql
        newschools = [School(name=school['name'], external_id=school['external_id'], address=school['address'], city=school['city'], state=school['state'], country='United States of America', zip=school['zip']) for school in schools]
        School.objects.bulk_create(newschools, 1000)
    return HttpResponse('Finished importing schools!')

def settings(request):
    if not teacher_check(request):
        return HttpResponseRedirect(reverse('authentication:index'))
    staff = Staff.objects.get(user = request.user)
    schools = School.objects.filter(staff = staff)
    school = schools.first()
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            if not school: # if the teacher is adding a code without removing one (ie, their first code)
                code = form.cleaned_data.get('code')
                school = School.objects.get(code = code)
                first_code = True
            if staff in school.owners.all(): # if the user is the owner of this school
                if len(school.staff.all()) > 1: # if the user is not the only staff member of this school
                    school.staff.remove(staff) # remove the user as a staff member
                    school.owners.add(school.staff.first()) # make the next staff member the new owner
                    school.owners.remove(staff) # remove the user as the owner
                else:
                    messages.add_message(request, messages.ERROR, _('You cannot change schools while you are the primary point of contact for your current school with no other staff members to replace you.'))
                    context = {
                        'form': form,
                        'school': school,
                    }
                    return render(request, 'teacher/settings.html', context)
            elif not first_code:
                school.staff.remove(staff)
            code = form.cleaned_data.get('code')
            school = School.objects.get(code = code)
            school.staff.add(staff)
            school.save()
            messages.add_message(request, messages.SUCCESS, _('Successfully joined ') + school.name)
        context = {
            'form': form,
            'school': school,
        }
        return render(request, 'teacher/settings.html', context)
    else:
        try:
            code = school.code
        except:
            code = None
        form = SettingsForm(initial={'code': code })
    context = {
        'form': form,
        'school': school,
    }
    return render(request, 'teacher/settings.html', context)