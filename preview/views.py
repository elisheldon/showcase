from django.http import JsonResponse
from webpreview import web_preview
from json import loads

# Create your views here.
def index(request):
    url = loads(request.body)['url']
    title, description, image = web_preview(url, parser='html.parser')
    return JsonResponse({'title': title, 'description': description, 'image': image})