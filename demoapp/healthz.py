from django.http import HttpResponse
from django.conf import settings
import datetime

def ready(request):
    return HttpResponse("OK", content_type="text/plain")

def alive(request):
    return HttpResponse("OK", content_type="text/plain")

def echo(request):
    currentDT = datetime.datetime.now()
    return HttpResponse(currentDT.strftime("%Y-%m-%d %H:%M:%S") + " -> Pod Name: " + settings.KUBE_POD_NAME + "\n", content_type="text/plain")
