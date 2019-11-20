from django.shortcuts import render
from django.shortcuts import HttpResponse
import cassiopeia as cass
from roleml import roleml
import requests


# Create your views here.
apikey = 1
with open('apikey.txt') as f:
    apikey = f.read().strip()
def single_game(request):
    
    context = dict()
    inputname = request.GET['summ_name']
    summoner = cass.Summoner(name = inputname)
    roles_match = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matches/{request.GET['match_id']}?api_key={apikey}").json()
    roles_match_timeline = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/{request.GET['match_id']}?api_key={apikey}").json()
    
    roles = roleml.predict(roles_match,roles_match_timeline)
    match = cass.Match(id = int(request.GET['match_id']))
    for player in match.participants:
        if player.summoner == summoner:
            enemy_team = player.enemy_team
        print(player.champion, roles[player.id])
        
    



    return HttpResponse(match.duration)
