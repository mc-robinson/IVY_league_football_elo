# -*- coding: utf-8 -*-
"""
Created: Wed Sep  7 22:06:05 2016
Author: matthewrobinson (Python 3.5)

Description: ELO rankings of IVY football games, according to 538's criteria. 
K factor is raised to 30 because there are less games to work from. And only keep
half of rating after season because of high variability in ivy league football.
"""
import numpy as np
#import matplotlib.pyplot as plt
import csv

def update(win_ELO, loss_ELO, mov):
    k = 20
    mov_multiplier = (2.2 * np.log(mov + 1))/((0.001 * (win_ELO-loss_ELO))+2.2)
    
#    rp1 = 10 ** (win_ELO/400)
#    rp2 = 10 ** (loss_ELO/400)
#    exp_p1 = rp1 / float(rp1 + rp2)
#    exp_p2 = rp2 / float(rp1 + rp2)
    
    u_win = 1/(1+(10 ** ((win_ELO-loss_ELO)/400)))
    u_loss = 1/(1+(10 ** ((loss_ELO-win_ELO)/400)))
    
    s1 = 1
    s2 = 0
    new_win_ELO = win_ELO + k * mov_multiplier * (s1 - u_win)
    new_loss_ELO = loss_ELO + k * mov_multiplier * (s2 - u_loss)
    return [new_win_ELO,new_loss_ELO]
    
    

with open('games_ivy_football_ELO.csv', 'r') as f:
  reader = csv.reader(f)
  temp_data = list(reader)
 
data = np.array(temp_data)
#data = data[5:8,:]

ELO_dict = dict({'Yale': 1500, 'Harvard': 1500,'Penn': 1500,'Dartmouth': 1500,'Princeton': 1500,'Brown': 1500,'Columbia': 1500,'Cornell': 1500})

row_number = 0
for away_team in data[:,0]:
    home_team = data[row_number,2]
        
    if away_team == 'new':
        for key in ELO_dict:
            ELO_dict[key] = (0.5*ELO_dict[key]) + (0.5*1500)
    else:
        home_elo = ELO_dict[home_team] + 65
        away_elo = ELO_dict[away_team]
            
        home_score = float(data[row_number,3])
        away_score = float(data[row_number,1])
            
        mov = abs(home_score - away_score)
            
        if home_score > away_score:
            new_home_elo = update(home_elo,away_elo,mov)[0] - 65
            new_away_elo = update(home_elo,away_elo,mov)[1]
        elif home_score < away_score:
            new_away_elo = update(away_elo,home_elo,mov)[0]
            new_home_elo = update(away_elo,home_elo,mov)[1] - 65
            
        ELO_dict[home_team] = new_home_elo
        ELO_dict[away_team] = new_away_elo
    
    print(row_number)       
    row_number = row_number + 1

