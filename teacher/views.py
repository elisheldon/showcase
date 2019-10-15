from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
import csv
import os

from .forms import SchoolSearchForm
from .models import School

def teacher_check(request):
    # checks to see if the current user is in the teachers group
    is_teacher = request.user.groups.filter(name='staff').exists()
    if not is_teacher:
        messages.add_message(request, messages.ERROR, _('You attempted to access a staff page, but you are not logged in as a staff member. Log in as a staff member and try again.'))
    return is_teacher

# Create your views here.
def index(request):
    return render(request, 'teacher/teacher_base.html')

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
        response = requests.get()
        return None
    form = SchoolSearchForm()
    context = {
        'form': form
    }
    return render(request, 'teacher/school_search.html', context)

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
