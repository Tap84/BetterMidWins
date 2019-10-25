from django.shortcuts import render, HttpResponse

import cassiopeia as cass
import random
from cassiopeia import Queue,Season

#cass.get_champions()
# Create your views here.
def analyze(request):
    context = dict()
    inputname = request.GET['summ_name']
    summoner = cass.Summoner(name = inputname)    
    
    solo_rank = summoner.ranks[Queue.ranked_solo_fives]
    context['tier'] = solo_rank.tier
    context['division'] = solo_rank.division
    
    for entry in summoner.league_entries.fives.league.entries:
        if entry.summoner.name.lower() == inputname.lower():
            context['summ_name'] = entry.summoner.name
            context['wins'] = entry.wins
            context['losses'] = entry.losses
            #WL = (W/W+L) * 100 for %
            context['win_loss'] = round(context['wins'] / (context['wins'] + context['losses']) * 100, 2)
        
    match_history = summoner.match_history(queues={Queue.ranked_solo_fives}, seasons={Season.season_9}, end_index=3)
    

    
    
    
    
            
    context['3matches'] = list()
    for i in range(3):
        context['3matches'].append(match_history[i])


        
    return render(request, 'summ_overview/main_overview.html', context=context)
