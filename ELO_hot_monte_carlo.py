# -*- coding: utf-8 -*-
"""
Created: Tue Sep  6 21:38:40 2016
Author: matthewrobinson (Python 3.5)

Description: using this to run monte carlo simulation of 2016 season
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import random

def update(win_ELO, loss_ELO):
    k = 20
    mov_multiplier = 1 ###(2.2 * np.log(mov + 1))/((0.001 * (win_ELO-loss_ELO))+2.2)
    
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
    
def win_probability(p1, p2):
    diff = p1 - p2
    p = 1 - 1 / (1 + 10 ** (diff / 400.0))
    return p


# the 3 column entry you draw data from
with open('CSV_for_ELO_2016.csv', 'r') as f:
  reader = csv.reader(f)
  temp_data = list(reader)
 
data = np.array(temp_data)

#dt = np.dtype((str, 2000))   # 35-character string
#results_matrix = np.empty((IDs.size,3),dt)
overall_win_dict = dict({'Yale': [0,0,0,0,0,0,0,0], 'Harvard': [0,0,0,0,0,0,0,0],'Penn': [0,0,0,0,0,0,0,0],'Dartmouth': [0,0,0,0,0,0,0,0],'Princeton': [0,0,0,0,0,0,0,0],'Brown': [0,0,0,0,0,0,0,0],'Columbia': [0,0,0,0,0,0,0,0],'Cornell': [0,0,0,0,0,0,0,0],})
titles_dict = dict({'Yale': 0, 'Harvard': 0,'Penn': 0,'Dartmouth': 0,'Princeton': 0,'Brown': 0,'Columbia': 0,'Cornell': 0,})
###ELO_dict = dict({'Yale': 1491.983696, 'Harvard': 1872.472758,'Penn': 1626.569371,'Dartmouth': 1753.370082,'Princeton': 1467.996793,'Brown': 1465.227635,'Columbia': 1161.181953,'Cornell': 1161.197711})

for i in range(100000):
    win_dict = dict({'Yale': 2, 'Harvard': 5,'Penn': 5,'Dartmouth': 1,'Princeton': 5,'Brown': 3,'Columbia': 1,'Cornell': 2,})
    ELO_dict = dict({'Yale': 1415.790085, 'Harvard': 1869.786805,'Penn': 1708.568172,'Dartmouth': 1639.080365,'Princeton': 1682.693627,'Brown': 1426.925792,'Columbia': 1108.664791,'Cornell': 1148.490363})
    row_number = 0
    for team in data[:,0]:
        opponent = data[row_number,1]
        rand = random.random()
        win_prob = win_probability(ELO_dict[team]+65,ELO_dict[opponent])
        
        if (win_prob == 1):
            win_dict[team] = win_dict[team] + 1
            ELO_dict[team] = update(ELO_dict[team]+65,ELO_dict[opponent])[0]-65
            ELO_dict[opponent] = update(ELO_dict[team]+65,ELO_dict[opponent])[1]
        elif (rand < win_prob):
            win_dict[team] = win_dict[team] + 1
            ELO_dict[team] = update(ELO_dict[team]+65,ELO_dict[opponent])[0]-65
            ELO_dict[opponent] = update(ELO_dict[team]+65,ELO_dict[opponent])[1]
        elif (rand >= win_prob):
            win_dict[opponent] = win_dict[opponent] + 1
            ELO_dict[opponent] = update(ELO_dict[opponent],ELO_dict[team]+65)[0]
            ELO_dict[team] = update(ELO_dict[opponent],ELO_dict[team]+65)[1] - 65
        row_number = row_number + 1
        
    max_wins = 0
    for key in win_dict:
        if win_dict[key] > max_wins:
            max_wins = win_dict[key]
            
    for key in win_dict:
        if win_dict[key] == max_wins:      
            titles_dict[key] = titles_dict[key] + 1
            
    for key in win_dict:
        overall_win_dict[key][win_dict[key]] = overall_win_dict[key][win_dict[key]] + 1
            
    print(i)

average_wins_dict = dict({'Yale': 0, 'Harvard': 0,'Penn': 0,'Dartmouth': 0,'Princeton': 0,'Brown': 0,'Columbia': 0,'Cornell': 0,})
for key in overall_win_dict:
    for i in range (len(overall_win_dict[key])):   
        average_wins_dict[key] = average_wins_dict[key] + (overall_win_dict[key][i]*i/100000)
        