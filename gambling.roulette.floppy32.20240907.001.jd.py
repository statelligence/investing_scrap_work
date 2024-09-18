# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 08:49:28 2024

@author: johnd
"""
import random
import statistics as st
#%%
def game(number):
    #bet 15 on odd/even, and 10 on first 3rd
    number -= 100
    #roulette wheel - 0 is 0 and 37 is 00
    list1 = list(range(37))
    #get spin
    spin_val = random.choice(list1)
    #if its 0 or 00 you don't get paid
    if spin_val == 0 or spin_val == 37:
        return number
    #figuring out if you get paid
    else:
        #if its even you get 2-1, this is reb/black equivalent
        if spin_val % 2 == 0:
            number += 120
        #if its less than 13, first 1rd you get 3-1, this is 3rds equivalent
        if spin_val < 13:
            number += 120
    return number
#%%
red_list = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19,21, 23,25,27,30,32,34,36]
middle_list = [2, 5, 8, 11,14, 17,20,23, 26, 29, 32,35]
def game2(number):
    #bet 15 on odd/even, and 10 on first 3rd
    number -= 100
    #roulette wheel - 0 is 0 and 37 is 00
    list1 = list(range(37))
    #get spin
    spin_val = random.choice(list1)
    #if its 0 or 00 you don't get paid
    if spin_val in red_list:
        number += 120
    if spin_val in middle_list:
        number += 120
    return number
#%%
bank_roll_list = []

#simulations
#100 took only a few seconds
sims = 1000000
starting_stack = 400
sims_left = sims

while sims_left > 0:
    stack = starting_stack
    #if you go below being able to play you lose (24)
    #if you go above 135 (35 is big win) you win and cash out
    while stack > 100 and stack < 550:
        
        stack = game(stack)
    #append the return
    bank_roll_list.append(stack)
    #debit the sims
    sims_left -=1
#%%
profit = sum(bank_roll_list) - sims*starting_stack

mean = sum(bank_roll_list) / len(bank_roll_list) 
variance = sum([((x - mean) ** 2) for x in bank_roll_list]) / len(bank_roll_list) 
res = variance ** 0.5
std_mean = res/starting_stack

print('profit is $', profit)
print('average is $', mean)
print('stdev is ', std_mean)
#%%
#winnning
win_list = [x for x in bank_roll_list if x>starting_stack]
#losing
lose_list = [y for y in bank_roll_list if y<starting_stack]

print(len(win_list), ' won')
print(len(lose_list), ' lost')
#%%
bank_roll_list2 = []

#simulations
#100 took only a few seconds
sims_left = sims

while sims_left > 0:
    stack = starting_stack
    #if you go below being able to play you lose (24)
    #if you go above 135 (35 is big win) you win and cash out
    while stack > 100 and stack < 550:
        
        stack = game2(stack)
    #append the return
    bank_roll_list2.append(stack)
    #debit the sims
    sims_left -=1

#%%
profit = sum(bank_roll_list2) - sims*starting_stack
pct_profit = profit/(sims*starting_stack)*100

mean = sum(bank_roll_list2) / len(bank_roll_list2) 
variance = sum([((x - mean) ** 2) for x in bank_roll_list2]) / len(bank_roll_list2) 
res = variance ** 0.5
std_mean = res/starting_stack

print('profit is $', profit, ' which is ', pct_profit, '%')
print('average is $', mean)
print('stdev is ', std_mean)
#%%
#winnning
win_list2 = [x for x in bank_roll_list2 if x>starting_stack]
#losing
lose_list2 = [y for y in bank_roll_list2 if y<starting_stack]

print(len(win_list2), ' won')
print(len(lose_list2), ' lost')
#%%