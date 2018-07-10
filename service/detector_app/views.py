from django.http import HttpResponse

from .models import detector


def index(request):
    if detector.is_ready():
        response = "It works!"
    else:
        response = "Ops"
    return HttpResponse(response)
