from django.http import HttpResponse


def detect(request):
    return HttpResponse("Hello, world. You're at the detector app.")
