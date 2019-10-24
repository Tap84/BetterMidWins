from django.shortcuts import render, HttpResponse

import cassiopeia as cass
import random
from cassiopeia import Queue

#champions = cass.get_champions()

# Create your views here.
def analyze(request):
    context = dict()
    context['summ_name'] = request.GET['summ_name']
    summoner = cass.Summoner(name = context['summ_name'])
    #print(summoner.rank_last_season)
    
    print(summoner)
    print(summoner.match_history)
    solo_rank = summoner.ranks[Queue.ranked_solo_fives]
    context['tier'] = solo_rank.tier
    context['division'] = solo_rank.division
    
    print(summoner.league_entries.fives.league.entries[1].league_points)
    
    #context['wins'] = solo_rank.wins
    #context['losses'] = solo_rank.losses
    
    
    
        
    
    #random_champ = random.choice(champions)
    return render(request, 'summ_overview/main_overview.html', context=context)
    #return HttpResponse(request.GET['summ_name'] + " plays " + random_champ.name)