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

# the 3 column entry you draw data from
with open('Sagarin_monte_carlo_week_6.csv', 'r') as f:
  reader = csv.reader(f)
  temp_data = list(reader)
 
data = np.array(temp_data)

#dt = np.dtype((str, 2000))   # 35-character string
#results_matrix = np.empty((IDs.size,3),dt)
overall_win_dict = dict({'Yale': [0,0,0,0,0,0,0,0], 'Harvard': [0,0,0,0,0,0,0,0],'Penn': [0,0,0,0,0,0,0,0],'Dartmouth': [0,0,0,0,0,0,0,0],'Princeton': [0,0,0,0,0,0,0,0],'Brown': [0,0,0,0,0,0,0,0],'Columbia': [0,0,0,0,0,0,0,0],'Cornell': [0,0,0,0,0,0,0,0],})
titles_dict = dict({'Yale': 0, 'Harvard': 0,'Penn': 0,'Dartmouth': 0,'Princeton': 0,'Brown': 0,'Columbia': 0,'Cornell': 0,})

for i in range(100000):
    win_dict = dict({'Yale': 2, 'Harvard': 5,'Penn': 5,'Dartmouth': 1,'Princeton': 5,'Brown': 3,'Columbia': 1,'Cornell': 2,})
    
    row_number = 0
    for team in data[:,0]:
        opponent = data[row_number,1]
        rand = random.random()
        if (float(data[row_number,2]) == 1):
            win_dict[team] = win_dict[team] + 1
        elif (rand < float(data[row_number,2])):
            win_dict[team] = win_dict[team] + 1
        elif (rand >= float(data[row_number,2])):
            win_dict[opponent] = win_dict[opponent] + 1
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
            
    
