import pyb 
import lis3dsh_driver
import random

from pyb import UART, Pin, Timer, delay
from constants import PLAYER_CHOOSE, WINDOW_HEIGHT, WINDOW_LENGTH, SCORE, SEE_YOU_SOON, LAST_SCORE, HELP

button_start = """
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
▐▌                                       ▐▌
▐▌ ▐█▀▀▀█ ▀▀▀██▀▀▀▐█▀▀▀█▌▐█▀▀▀█ ▀▀▀██▀▀▀ ▐▌
▐▌ ▐█▄▄▄▄    ▐▌   ▐█▄▄▄█▌▐█▄▄▄█    ▐▌    ▐▌
▐▌      █    ▐▌   ▐▌   ▐▌▐▌  ▐▌    ▐▌    ▐▌
▐▌ ▐█▄▄▄█    ▐▌   ▐▌   ▐▌▐▌   ▐▌   ▐▌    ▐▌
▐▌                                       ▐▌
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

button_quit = """
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
▐▌                                       ▐▌
▐▌      ▐█▀▀▀█▌ ▐▌   ▐▌ ▐▌ ▀▀▀██▀▀▀      ▐▌
▐▌      ▐▌   ▐▌ ▐▌   ▐▌ ▐▌    ▐▌         ▐▌
▐▌      ▐▌  ▄▐▌ ▐▌   ▐▌ ▐▌    ▐▌         ▐▌
▐▌      ▐█▄▄▄█▌ ▐█▄▄▄█▌ ▐▌    ▐▌         ▐▌
▐▌            ▀                          ▐▌
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

game_name_label = """
 ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄               ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄ 
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌             ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌              ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌                  ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌▐░▌    ▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌   ▄▄▄▄▄▄▄▄▄▄▄    ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌ ▐░▌   ▐░▌
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  ▐░░░░░░░░░░░▌   ▐░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀    ▀▀▀▀▀▀▀▀▀▀▀    ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌   ▐░▌ ▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌                       ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌    ▐░▌▐░▌
▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌               ▐░▌                       ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌     ▐░▐░▌
▐░▌          ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌               ▐░▌                       ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌
 ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀                 ▀                         ▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀                                                                                                                                
"""

try_again_label = """
 ▀▀▀██▀▀▀▐█▀▀▀▀█ ▌    ▐  ▐█▀▀▀▀█▌▐█▀▀▀▀▀▐█▀▀▀▀█▌▐▌▐▌    ▐▌
    ▐▌   ▐█▄▄▄▄█ █▄▄▄▄█  ▐█▄▄▄▄█▌▐▌     ▐█▄▄▄▄█▌▐▌▐▌▐▌  ▐▌
    ▐▌   ▐▌  ▐▌    ▐▌    ▐▌    ▐▌▐▌ ▀▀▀█▐▌    ▐▌▐▌▐▌  ▐▌▐▌
    ▐▌   ▐▌   ▐▌   ▐▌    ▐▌    ▐▌▐█▄▄▄▄█▐▌    ▐▌▐▌▐▌    ▐▌
"""

loading_label = """
▐▌    ▐█▀▀▀█▌▐█▀▀▀█▌▐█▀▀▄  ▐▌▐▌    ▐▌▐█▀▀▀▀▀
▐▌    ▐▌   ▐▌▐█▄▄▄█▌▐▌   ▐▌▐▌▐▌▐▌  ▐▌▐▌     
▐▌    ▐▌   ▐▌▐▌   ▐▌▐▌   ▐▌▐▌▐▌  ▐▌▐▌▐▌ ▀▀▀█
▐█▄▄▄▄▐█▄▄▄█▌▐▌   ▐▌▐█▄▄▀  ▐▌▐▌    ▐▌▐█▄▄▄▄█
"""

choose_player_label = """
▐█▀▀▀▀▐▌   ▐▌▐█▀▀▀█▌▐█▀▀▀█▌▐█▀▀▀█▐▌▀▀▀▀    ▌    ▐▐█▀▀▀█▌▐▌   ▐▌▐█▀▀▀▀█    ▐█▀▀▀▀█▐▌    ▐█▀▀▀▀█▌▌    ▐▐▌▀▀▀▀▐█▀▀▀▀█ 
▐▌    ▐▌   ▐▌▐▌   ▐▌▐▌   ▐▌▐█▄▄▄▄▐▌        █▄▄▄▄█▐▌   ▐▌▐▌   ▐▌▐█▄▄▄▄█    ▐█▄▄▄▄█▐▌    ▐█▄▄▄▄█▌█▄▄▄▄█▐▌    ▐█▄▄▄▄█
▐▌    ▐█▄▄▄█▌▐▌   ▐▌▐▌   ▐▌     █▐▌▀▀▀       ▐▌  ▐▌   ▐▌▐▌   ▐▌▐▌  ▐▌     ▐▌     ▐▌    ▐▌    ▐▌  ▐▌  ▐▌▀▀▀ ▐▌  ▐▌
▐█▄▄▄▄▐▌   ▐▌▐█▄▄▄█▌▐█▄▄▄█▌▐█▄▄▄█▐▌▄▄▄▄      ▐▌  ▐█▄▄▄█▌▐█▄▄▄█▌▐▌   ▐▌    ▐▌     ▐█▄▄▄▄▐▌    ▐▌  ▐▌  ▐▌▄▄▄▄▐▌   ▐▌ 
"""

game_over_label = """
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄               ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░▌             ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░█▀▀▀▀▀▀▀█░▌ ▐░▌           ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
▐░▌          ▐░▌       ▐░▌▐░▌▐░▌ ▐░▌▐░▌▐░▌               ▐░▌       ▐░▌  ▐░▌         ▐░▌  ▐░▌          ▐░▌       ▐░▌
▐░▌ ▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌       ▐░▌   ▐░▌       ▐░▌   ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌     ▐░▌       ▐░▌    ▐░▌     ▐░▌    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░▌ ▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌   ▀   ▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░▌       ▐░▌     ▐░▌   ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀█░█▀▀ 
▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌               ▐░▌       ▐░▌      ▐░▌ ▐░▌      ▐░▌          ▐░▌     ▐░▌  
▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░█▄▄▄▄▄▄▄█░▌       ▐░▐░▌       ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌      ▐░▌ 
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌        ▐░▌        ▐░░░░░░░░░░░▌▐░▌       ▐░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀          ▀          ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀                                                                                                                 
"""

birdython_player = """
                                   
            ⬛️⬛️⬛️⬛️⬛️⬛️          
        ⬛️⬛️🟨🟨🟨🟨⬛️⬜️⬛️        
      ⬛️🟨🟨🟨🟨🟨⬛️⬜️⬜️⬜️⬛️      
  ⬛️⬛️⬛️⬛️🟨🟨🟨🟨⬛️⬜️⬜⬛️⬜️⬛️    
⬛️⬜️⬜️⬜️⬜️⬛️🟨🟨🟨⬛️⬜️⬜️⬛️⬜️⬛️    
⬛️⬜️⬜️⬜️⬜️⬜️⬛️🟨🟨🟨⬛️⬜️⬜️⬜️⬛️    
⬛️🟨⬜️⬜️⬜️🟨⬛️🟨🟨🟨🟨⬛️⬛️⬛️⬛️⬛️  
  ⬛️🟨🟨🟨⬛️🟨🟨🟨🟨⬛️🟧🟧🟧🟧🟧⬛️
    ⬛️⬛️⬛️🟨🟨🟨🟨⬛️🟧⬛️⬛️⬛️⬛️⬛️  
        ⬛️🟨🟨🟨🟨🟨⬛️🟧🟧🟧🟧⬛️  
          ⬛️⬛️🟨🟨🟨🟨⬛️⬛️⬛️⬛️    
              ⬛️⬛️⬛️⬛️             
                                   
"""

thon_player = """
                                 
⬛️            ⬛️⬛️⬛️⬛️⬛️         
⬛️⬛️      ⬛️⬛️🟦🟦🟦🟦🟦⬛️⬛️     
⬛️🟦⬛️  ⬛️🟦🟦🟦🟦🟦🟦⬛️🟦⬛️⬛️   
⬛️🟦🟦⬛️🟦🟦🟦🟦🟦🟦🟦⬛️🟦🟫🟦⬛️  
⬛️🟦⬜️⬛️🟦🟦🟦🟦⬜️⬜️⬜️⬛️🟦🟦🟦⬛️⬛️  
⬛⬜️⬛️  ⬛️🟦⬜️⬜️⬜️⬜️⬜️⬜️⬛️🟦⬛️   
⬛️⬛️      ⬛️⬛️⬜️⬜️🟦🟦🟦⬛️⬛️     
⬛️            ⬛️⬛️⬛️⬛️⬛️         
                                  
"""

### Tunnels

tunnel_down = """\
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛   
"""

tunnel_up = """\
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛   
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️ 
"""

tunnel_base = """\
   ⬛️🟩🟩🟩🟩🟩🟩🟩⬛   
"""

tunnel_down_shadow = """\
                         
                         
                         
                         
"""

arrows = """
      ⬛⬛
    ⬛🟦⬛
  ⬛🟦🟦⬛⬛⬛⬛⬛
⬛🟦⬛🟦🟦🟦🟦🟦⬛
⬛🟦🟦🟦🟦🟦🟦🟦⬛
  ⬛🟦🟦⬛⬛⬛⬛⬛  ⬛⬛
    ⬛🟦⬛          ⬛🟨⬛
      ⬛⬛  ⬛⬛⬛⬛⬛🟨🟨⬛
            ⬛🟨🟨🟨🟨🟨⬛🟨⬛
            ⬛🟨🟨🟨🟨🟨🟨🟨⬛
            ⬛⬛⬛⬛⬛🟨🟨⬛
                    ⬛🟨⬛
                    ⬛⬛
"""

cursor = """\
     ⬛⬛⬛    
   ⬛🟦⬛🟨⬛   
 ⬛🟦🟦⬛🟨🟨⬛ 
 ⬛⬛⬛⬛⬛⬛⬛ 
"""
cursor_shadow = """\
              
              
              
              
"""

# UART init
uart_number = 2
uart = UART(uart_number)
uart.init(2_000_000, bits=8, parity=None, stop=1)

# Push button init
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)

# Timer init
t_counter = Timer(4, freq=2)

def counter_timer(t_counter):
    global toggle 
    global counter_var
    counter_var += 1
    toggle = not toggle
    print("Toggle : ", toggle)

choose_player_flag = False
toggle = False
counter_var = 0
t_counter.callback(counter_timer)

def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")

def move(x,y):
    uart.write("\x1b[{};{}H".format(y,x))

def screen_placement(window_parts = WINDOW_HEIGHT, element_size = 0, mode = 0):
    """
    mode : 0 => middle x
    mode : 1 => middle middle x
    """
    if mode:
      placement = ((window_parts//2)//2)-(element_size//2)
    else:
      placement = (window_parts//2)-(element_size//2)
    return placement

def draw_element(element, x, y):
    for index, line in enumerate(element.splitlines()):
        move(x, y+index)
        uart.write(line)

def splash_screen_loading():
    clear_screen()
    draw_element(game_name_label, screen_placement(WINDOW_LENGTH, 130, 0), 20)
    draw_element(loading_label, screen_placement(WINDOW_LENGTH, 44, 0), 35)
    delay(3000)
    clear_screen()

def draw_nothing(col):
    for i in range (0, WINDOW_HEIGHT):
        move(col, i)
        uart.write(" \b")

def draw_tunnels_down(x,y):
    draw_element(tunnel_down, x, y)
    y += 4
    while(y < WINDOW_HEIGHT):
        draw_element(tunnel_base, x, y)
        y += 1
    
def draw_tunnels_up(x,y):
    draw_element(tunnel_up, x, y)
    while(y):
        y -= 1
        draw_element(tunnel_base, x, y)

def game_over():
    clear_screen()
    draw_element(game_over_label, screen_placement(WINDOW_LENGTH, 115, 0), 20)
    draw_element(try_again_label, screen_placement(WINDOW_LENGTH, 62, 0), 45)
    delay(3000)
    clear_screen()
    # need to exit while loop

def splash_screen_ending():
    clear_screen()
    draw_element(game_name_label, screen_placement(WINDOW_LENGTH, 130, 0), 20)
    draw_element(SEE_YOU_SOON, screen_placement(WINDOW_LENGTH, 22, 0), 35)
    delay(3000)
    clear_screen()

def user_name():
    move(10,10)
    uart.write("ENTER YOUR de :")
    username = input("ENTER YOUR NAME")
    uart.write(username)

def draw_last_score(x, y):
    data = []
    with open('last_scores.txt', 'r') as file_records:
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

def draw_menu():
    draw_element(game_name_label,screen_placement(WINDOW_LENGTH, 130, 0), 10)
    draw_element(button_start, screen_placement(WINDOW_LENGTH, 43, 1), 35)
    draw_element(button_quit,(WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 43, 1), 35)
    draw_element(arrows, screen_placement(WINDOW_LENGTH, 30, 0), 32)
    draw_element(HELP, screen_placement(WINDOW_LENGTH, 50, 0),55)
    draw_last_score(200,58)

def blink_element(first_element, second_element, x,y):
    if toggle:
      draw_element(first_element,x,y)
    else:
      draw_element(second_element, x,y)

def choose_your_player():
    choose_player_flag = False

    draw_element(birdython_player, screen_placement(WINDOW_LENGTH, 22, 1), (WINDOW_HEIGHT//2) - 7)
    draw_element(thon_player, (WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 20, 1),  (WINDOW_HEIGHT//2) - 7)
    draw_element(choose_player_label, screen_placement(WINDOW_LENGTH, 115, 0),5)

    delay(300)

    while(not choose_player_flag):

      blink_element(cursor, cursor_shadow, screen_placement(WINDOW_LENGTH,10,0), WINDOW_HEIGHT//2+15)
      choose_player_acc_data = lis3dsh_driver.get_acc_value()
      
      if choose_player_acc_data < -300:
          player_choose = birdython_player
          choose_player_flag = True
      elif choose_player_acc_data > 300:
          player_choose = thon_player
          choose_player_flag = True
    
    draw_element(cursor_shadow, screen_placement(WINDOW_LENGTH,10,0), WINDOW_HEIGHT//2+15)
    counter_var = 0
    while (counter_var < 840):
      counter_var += 1
      print(counter_var)
      if player_choose == birdython_player:
        draw_element(PLAYER_CHOOSE + "BIRDYTHON PLAYER !", screen_placement(WINDOW_LENGTH, 33, 0), 45)
        blink_element(cursor, cursor_shadow, screen_placement(WINDOW_LENGTH, 10, 1), (WINDOW_HEIGHT//2) +15)
      else:
        draw_element(PLAYER_CHOOSE + "THON PLAYER !", screen_placement(WINDOW_LENGTH, 28, 0), 45)
        blink_element(cursor, cursor_shadow, (WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 10, 1), (WINDOW_HEIGHT//2) +15)
    
    clear_screen()
    return player_choose

def random_data_for_tunnels():
    #random_data = random.randrange(0,67)
    #print(random_data)
    pass