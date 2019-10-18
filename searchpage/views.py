from django.shortcuts import render
from django.http import HttpResponse
import cassiopeia as cass
import random
from .forms import SearchForm
from pathlib import Path


with open('apikey.txt') as f:
    cass.set_riot_api_key(f.read().strip())
cass.set_default_region("NA")
champions = cass.get_champions()

# Create your views here.
def search(request):
    summ_name = 'kingtylerp'
    summoner = cass.get_summoner(name=summ_name)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            
            summ_name=form.cleaned_data['search']
            #print(summ_name)
        
        summoner = cass.get_summoner(name=summ_name)
        print(f"{summoner.name} is a level {summoner.level} summoner.")

    
    
    random_champion = random.choice(champions)
    
    print("He enjoys playing champions such as {name}.".format(name=random_champion.name))


    return render(request, 'searchpage/searchpage.html',{'current_name':summ_name, 'summoner':summoner})

