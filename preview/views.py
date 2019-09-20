from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.staticfiles import finders
from django.contrib.admin.views.decorators import staff_member_required

from webpreview import web_preview
from json import loads
from urllib.parse import urlparse

from preview.models import BlacklistUrl

# Create your views here.
def index(request):
    url = loads(request.body)['url']
    url_obj = urlparse(url)
    banned = BlacklistUrl.objects.filter(domain=url_obj.netloc)
    if banned:
        return HttpResponse('That URL is banned.')
    # https://github.com/ludbek/webpreview
    title, description, image = web_preview(url, parser='html.parser', headers = {'User-Agent': 'Mozilla/5.0'})
    return JsonResponse({'title': title, 'description': description, 'image': image})

@staff_member_required
def load_blacklist(request):
    url = finders.find('preview/blacklist.txt') # static from django.templatetags.static wasn't working
    with open(url) as blacklist:
        for line in blacklist:
            domain = BlacklistUrl(domain = line)
            domain.save() # this should be transactional (ie, not saving every time) if i do it again / before production;
            # PostgreSQL supports autokey primary key unlike sqlite3 per https://docs.djangoproject.com/en/2.2/ref/models/querysets/#bulk-create
    return HttpResponse('Successfully loaded blacklist.')
