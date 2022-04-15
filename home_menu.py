import pyb 

from constants import *
from commun import *

class Home_menu():
    def __init__(self) -> None:
        pass

    def draw_button(self, button, x, y):
        for index, line in enumerate(button.splitlines()):
            move(x, y+index)
            uart.write(line)
    
    def draw_last_score(self):
        pass


