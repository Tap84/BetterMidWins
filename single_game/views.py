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

    user_role = None
    user_part_data = match.participants[0]
    direct_opponent = match.participants[1]
    opponent_team = match.participants[0].enemy_team
    user_team = match.participants[0].team

    #Finding role of user
    for player in match.participants:
        if player.summoner == summoner:
            user_part_data = player
            user_team = player.team
            opponent_team = player.enemy_team
            user_role = roles[player.id]

    #Finding opponent
    
    for player in match.participants:
        #print(roles[player.id])
        if roles[player.id] == user_role and player.summoner != summoner:
            direct_opponent = player
    
            
    #Getting data
    """
    CS Comparison
    CS % of team
    Champion damage dealt
    Damage % of team
    Objective Damage
    K/D/A
    Kill Participation %
    Vision Score
    Control wards
    """
    user_stats = user_part_data.stats
    opp_stats = direct_opponent.stats
    #Teams Stats

    ally_cs_total = 0
    ally_dmg_total = 0
    ally_obj_dmg_total = 0
    ally_kill_total = 0
    
    opponent_dmg_total = 0
    opponent_cs_total = 0
    opponent_obj_dmg_total = 0
    opponent_kill_total = 0

    for player in user_team.participants:
        ally_dmg_total += player.stats.total_damage_dealt_to_champions
        ally_cs_total += player.stats.total_minions_killed
        ally_obj_dmg_total += player.stats.damage_dealt_to_objectives
        ally_kill_total += player.stats.kills
    for player in opponent_team.participants:
        opponent_dmg_total += player.stats.total_damage_dealt_to_champions
        opponent_cs_total += player.stats.total_minions_killed 
        opponent_obj_dmg_total += player.stats.damage_dealt_to_objectives  
        opponent_kill_total += player.stats.kills
    #CS and CS%
    context['u_cs'] = user_stats.total_minions_killed
    context['o_cs'] = opp_stats.total_minions_killed
    context['u_cs_per'] = round(context['u_cs'] / ally_cs_total, 2)
    context['o_cs_per'] = round(context['o_cs'] / opponent_cs_total, 2)

    #DMG and DMG%
    context['u_dmg'] = user_stats.total_damage_dealt_to_champions
    context['o_dmg'] = opp_stats.total_damage_dealt_to_champions
    context['u_dmg_per'] = round(context['u_dmg'] / ally_dmg_total, 2)
    context['o_dmg_per'] = round(context['o_dmg'] / opponent_dmg_total, 2)

    #OBJ DMG
    context['u_obj_dmg'] = user_stats.damage_dealt_to_objectives
    context['o_obj_dmg'] = opp_stats.damage_dealt_to_objectives
    context['u_obj_dmg_per'] = round(context['u_obj_dmg'] / ally_obj_dmg_total, 2)
    context['o_obj_dmg_per'] = round(context['o_obj_dmg'] / opponent_obj_dmg_total, 2)

    #KDA
    context['u_kda'] = round(user_stats.kda, 2)
    context['o_kda'] = round(opp_stats.kda, 2)

    #Kill Participation %
    context['u_kp'] = round( (user_stats.kills+user_stats.assists) / ally_kill_total, 2)
    context['o_kp'] = round( (opp_stats.kills+opp_stats.assists) / opponent_kill_total, 2)

    #Vision score and Control Wards
    context['u_vision'] = user_stats.vision_score
    context['o_vision'] = opp_stats.vision_score
    context['u_control_wards'] = user_stats.vision_wards_bought_in_game
    context['o_control_wards'] = opp_stats.vision_wards_bought_in_game

    #Game Analysis
    context['weaknesses'] = []
    context['strengths'] = []
    #CS Info
    if (context['o_cs'] - context['u_cs']) > 40:
        context['weaknesses'].append(f"Your CS is significantly lower than your opponent(You: {context['u_cs']}, Opponent: {context['o_cs']}), consider practicing your CSing, or spend more time farming and less time fighting.")
    elif (context['o_cs'] - context['u_cs']) < -40:
        context['strengths'].append(f"Your CS is significantly higher than your opponent(You: {context['u_cs']}, Opponent: {context['o_cs']}), you may be able to sacrifice some CS in order to push your advantage, or keep up the farming if you prefer a lategame match.")
    
    if (context['o_cs_per'] - context['u_cs_per']) > .05:
        context['weaknesses'].append(f"Your CS percent of your team is significantly lower than your opponent(You: {context['u_cs_per']}, Opponent: {context['o_cs_per']}). If you were playing a strong scaling champion, you should aim to increase this number in order to enable yourself to carry the game.")
    elif (context['o_cs_per'] - context['u_cs_per']) < -.05:
        context['strengths'].append(f"Your CS percent of your team is significantly higher than your opponent(You: {context['u_cs_per']}, Opponent: {context['o_cs_per']}). You should be able to carry games more often if you continue this trend.")
    
    #DMG Info
    if (context['o_dmg'] - context['u_dmg']) > 15000:
        context['weaknesses'].append(f"Your Damage to Champions is significantly lower than your opponent(You: {context['u_dmg']}, Opponent: {context['o_dmg']}), ignore this if one of you is a poke champion and the other isnt, if you can increase this number you will be more effective in teamfights.")
    elif (context['o_dmg'] - context['u_dmg']) < -15000:
        context['strengths'].append(f"Your Damage to Champions is significantly higher than your opponent(You: {context['u_dmg']}, Opponent: {context['o_dmg']}), ignore this if you are a poke champion and your opponent isnt, this means you are generally more effective at outputting damage than your opponent.")
    
    if (context['o_dmg_per'] - context['u_dmg_per']) > .10:
        context['weaknesses'].append(f"Your Damage percent of your team is significantly lower than your opponent(You: {context['u_dmg_per']}, Opponent: {context['o_dmg_per']}). If you can increase this number, it means you will will be the weak link in damage output on your team more often.")
    elif (context['o_dmg_per'] - context['u_dmg_per']) < -.10:
        context['strengths'].append(f"Your Damage percent of your team is significantly higher than your opponent(You: {context['u_dmg_per']}, Opponent: {context['o_dmg_per']}). You should be able to carry games more often if you continue this trend.")
    
    return render(request, 'single_game/single_game.html', context=context)
