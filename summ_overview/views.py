from django.shortcuts import render, HttpResponse

import cassiopeia as cass
import random
from cassiopeia import Queue,Season
#just to load in champions without having to load on request as it takes a long time
#champsdummy = cass.get_champions()
#for champ in champsdummy:
    #champ.name
# Create your views here.
def analyze(request):
    with open('apikey.txt') as f:
        cass.set_riot_api_key(f.read().strip())
    cass.set_default_region("NA")
    context = dict()
    inputname = request.GET['summ_name']
    summoner = cass.Summoner(name = inputname)  
    try:
        summoner.id
    except:
        return HttpResponse("Summoner doesnt exist")  
    
    try:
        solo_rank = summoner.ranks[Queue.ranked_solo_fives]
    except:
        return HttpResponse("Summoner has no ranked solo 5v5 games")
    context['tier'] = solo_rank.tier
    context['division'] = solo_rank.division
    
    for entry in summoner.league_entries.fives.league.entries:
        if entry.summoner.name.lower() == inputname.lower():
            context['summ_name'] = entry.summoner.name
            context['wins'] = entry.wins
            context['losses'] = entry.losses
            #WL = (W/W+L) * 100 for %
            context['win_loss'] = round(context['wins'] / (context['wins'] + context['losses']) * 100, 2)
        
    match_history = summoner.match_history(queues={Queue.ranked_solo_fives},  end_index=5)
   
    context['5matches'] = list()
    for i in range(5):
        context['5matches'].append(match_history[i])
        
    return render(request, 'summ_overview/main_overview.html', context=context)
