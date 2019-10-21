from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def analyze(request):
    print(request)
    return HttpResponse("Analyze!")

