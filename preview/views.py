from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.staticfiles import finders
from django.contrib.admin.views.decorators import staff_member_required
import requests
from webpreview import web_preview
from json import loads
import tldextract

from preview.models import BlacklistUrl

# Create your views here.
def index(request):
    try: 
        url_in = loads(request.body)['url']
        # get final url of any link shorteners, per https://alexwlchan.net/2016/07/chasing-redirects-and-url-shorteners/
        url = requests.get(url_in).url
        url_obj = tldextract.extract(url)
        banned = BlacklistUrl.objects.filter(domain=f'{url_obj.domain}.{url_obj.suffix}\n') #\n because that's how i loaded them into the database - remove it after next blacklist load
        if banned:
            return JsonResponse({'title': 'This URL has been blocked', 'description': 'Make sure you are only adding school-approriate content to your portfolio - this should be your best work!', 'image': ''})
        title, description, image = web_preview(url, parser='html.parser', headers = {'User-Agent': 'Mozilla/5.0'})
        return JsonResponse({'title': title, 'description': description, 'image': image, 'url': url})
    except:
        return HttpResponseBadRequest()

@staff_member_required
def load_blacklist(request):
    url = finders.find('preview/blacklist.txt') # static from django.templatetags.static wasn't working
    with open(url) as blacklist:
        for line in blacklist:
            domain = BlacklistUrl(domain = line.rstrip())
            domain.save() # this should be transactional (ie, not saving every time) if i do it again / before production;
            # PostgreSQL supports autokey primary key unlike sqlite3 per https://docs.djangoproject.com/en/2.2/ref/models/querysets/#bulk-create
    return HttpResponse('Successfully loaded blacklist.')
