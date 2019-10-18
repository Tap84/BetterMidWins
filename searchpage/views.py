from django.shortcuts import render
from django.http import HttpResponse
import cassiopeia as cass
import random
from .forms import SearchForm

# Create your views here.
def search(request):
    summ_name = "test"
    if request.method == "POST":
        form = SearchForm(request.POST)
        
        print(form.is_valid())
        if form.is_valid():
            summ_name=form.clean()
            print(summ_name)
        cass.set_riot_api_key("RGAPI-a39f9032-605b-4241-9294-490ca8bd42eb")  # This overrides the value set in your configuration/settings.
        cass.set_default_region("NA")

        summoner = cass.get_summoner(name=summ_name)
        print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
                                                                                level=summoner.level,
                                                                                region=summoner.region))

    #champions = cass.get_champions()
    #print(champions)
    #random_champion = random.choice(champions)
    #print("He enjoys playing champions such as {name}.".format(name=random_champion.name))


    return render(request, 'searchpage/searchpage.html',{'current_name':summ_name})

