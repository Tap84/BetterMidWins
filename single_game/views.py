from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def analyze(request):
    return HttpResponse(request.GET['summ_name'])

