from django.shortcuts import render, HttpResponse

import cassiopeia as cass
import random

#champions = cass.get_champions()

# Create your views here.
def analyze(request):
    context = dict()
    S
    context['summ_name'] = request.GET['summ_name']
    summoner = cass.get_summoner(name = context['summ_name'])
    print(summoner.rank_last_season)
    #random_champ = random.choice(champions)
    return render(request, 'summ_overview/main_overview.html', context=context)
    #return HttpResponse(request.GET['summ_name'] + " plays " + random_champ.name)