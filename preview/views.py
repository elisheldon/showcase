from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.staticfiles import finders
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
import urllib
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
        banned = BlacklistUrl.objects.filter(domain=f'{url_obj.domain}.{url_obj.suffix}')
        if banned:
            return JsonResponse({'title': 'This URL has been blocked', 'description': 'Make sure you are only adding school-approriate content to your portfolio - this should be your best work!', 'image': '', 'url': ''})
        title, description, image = web_preview(url, parser='html.parser', headers = {'User-Agent': 'Mozilla/5.0'})
        return JsonResponse({'title': title, 'description': description, 'image': image, 'url': url})
    except:
        return HttpResponseBadRequest()

@staff_member_required
def load_blacklist(request):
    #url = settings.STATIC_URL + 'preview/blacklist.txt'
    url = 'https://elasticbeanstalk-us-west-2-315679056419.s3-us-west-2.amazonaws.com/static/preview/blacklist.txt'
    with urllib.request.urlopen(url) as blacklist:
        domains = [BlacklistUrl(domain = line.rstrip().decode('UTF-8')) for line in blacklist]
        BlacklistUrl.objects.bulk_create(domains, 1000)
    return HttpResponse('Successfully loaded blacklist.')
