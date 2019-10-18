from django.shortcuts import render
from django.http import HttpResponse
import cassiopeia as cass
from .forms import SearchForm
from pathlib import Path


with open('apikey.txt') as f:
    cass.set_riot_api_key(f.read().strip())
cass.set_default_region("NA")
#champions = cass.get_champions()

# Create your views here.
def search(request):
    return render(request, 'searchpage/searchpage.html')

