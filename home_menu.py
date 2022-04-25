import pyb 

from constants import LAST_SCORE
from commun import *

def draw_button( button, x, y):
    for index, line in enumerate(button.splitlines()):
        move(x, y+index)
        uart.write(line)

def user_name():
    move(10,10)
    uart.write("ENTER YOUR de :")
    username = input("ENTER YOUR NAME")
    uart.write(username)
    

def draw_last_score(x, y):
    data = []
    with open('best_scores.txt', 'r') as file_records:
        data = file_records.readlines()
        
    if data:
        last_score =  data[-1]
    else:
        last_score = '0'

    move(x, y)
    uart.write(LAST_SCORE + last_score)

def add_current_score(name, score):
    with open('best_scores.txt', 'w') as file_records:
        data = file_records.readlines()
    pass