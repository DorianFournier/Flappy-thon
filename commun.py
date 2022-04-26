import pyb 
from pyb import UART, Pin, LED, Timer, delay
from constants import *

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
▐▌      ▐▌ ▄▄▐▌ ▐▌   ▐▌ ▐▌    ▐▌         ▐▌
▐▌      ▐█▄▄▄█▌ ▐█▄▄▄█▌ ▐▌    ▐▌         ▐▌
▐▌            ▀                          ▐▌
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

game_over_text = """

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

birdython = """
                                   
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


thon = """
                                 
⬛️            ⬛️⬛️⬛️⬛️⬛️         
⬛️⬛️      ⬛️⬛️🟦🟦🟦🟦🟦⬛️⬛️     
⬛️🟦⬛️  ⬛️🟦🟦🟦🟦🟦🟦⬛️🟦⬛️⬛️   
⬛️🟦🟦⬛️🟦🟦🟦🟦🟦🟦🟦⬛️🟦🟫🟦⬛️  
⬛️🟦⬜️⬛️🟦🟦🟦🟦⬜️⬜️⬜️⬛️🟦🟦🟦⬛️  
⬛⬜️⬛️  ⬛️🟦⬜️⬜️⬜️⬜️⬜️⬜️⬛️🟦⬛️   
⬛️⬛️      ⬛️⬛️⬜️⬜️🟦🟦🟦⬛️⬛️     
⬛️            ⬛️⬛️⬛️⬛️⬛️         
                                  
"""

tunnel_down = """\
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛   
"""

tunnel_down_shadow = """\
                         
                         
                         
                         
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

game_name = """
 ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄               ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄ 
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌             ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌             ▐░▌       ▐░▌ ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌             ▐░▌       ▐░▌     ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌▐░▌    ▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌ ▐░▌   ▐░▌
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀      ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌   ▐░▌ ▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌                            ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌    ▐░▌▐░▌
▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌                            ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌     ▐░▐░▌
▐░▌          ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌                            ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌
 ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀                              ▀            ▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀ 
                                                                                                                                  
"""

try_again = """
 ▀▀▀██▀▀▀▐█▀▀▀▀█ ▌    ▐  ▐█▀▀▀▀█▌▐█▀▀▀▀▀▐█▀▀▀▀█▌▐▌▐▌    ▐▌
    ▐▌   ▐█▄▄▄▄█ █▄▄▄▄█  ▐█▄▄▄▄█▌▐▌     ▐█▄▄▄▄█▌▐▌▐▌▐▌  ▐▌
    ▐▌   ▐▌  ▐▌    ▐▌    ▐▌    ▐▌▐▌ ▀▀▀█▐▌    ▐▌▐▌▐▌  ▐▌▐▌
    ▐▌   ▐▌   ▐▌   ▐▌    ▐▌    ▐▌▐█▄▄▄▄█▐▌    ▐▌▐▌▐▌    ▐▌
"""

loading = """
▐▌    ▐█▀▀▀█▌▐█▀▀▀█▌▐█▀▀▄  ▐▌▐▌    ▐▌▐█▀▀▀▀▀
▐▌    ▐▌   ▐▌▐█▄▄▄█▌▐▌   ▐▌▐▌▐▌▐▌  ▐▌▐▌ 
▐▌    ▐▌   ▐▌▐▌   ▐▌▐▌   ▐▌▐▌▐▌  ▐▌▐▌▐▌ ▀▀▀█
▐█▄▄▄▄▐█▄▄▄█▌▐▌   ▐▌▐█▄▄▀  ▐▌▐▌    ▐▌▐█▄▄▄▄█
"""

# UART init
uart_number = 2
uart = UART(uart_number)
uart.init(2_000_000, bits=8, parity=None, stop=1)

# Push button init
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)

#Timer
t_counter = Timer(4, freq=1)
def counter_timer(t_counter):
    global toggle 
    toggle = not toggle
    print("Toggle : ", toggle)

player_ok = False
toggle = False
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

def debug():
    move((WINDOW_LENGTH//2), WINDOW_HEIGHT//2)
    uart.write("#")

    move((WINDOW_LENGTH//2)//2, WINDOW_HEIGHT//2)
    uart.write("#")

    move(238- ((WINDOW_LENGTH//2)//2), WINDOW_HEIGHT//2)
    uart.write("#")

def draw_element(element, x, y):
    for index, line in enumerate(element.splitlines()):
        move(x, y+index)
        uart.write(line)

def splash_screen():
    clear_screen()
    draw_element(game_name, screen_placement(WINDOW_LENGTH, 130, 0), 20)
    draw_element(loading, screen_placement(WINDOW_LENGTH, 44, 0), 35)
    delay(3000)
    clear_screen()

def draw_nothing(col):
    for i in range (0, WINDOW_DOWN):
        move(col, i)
        uart.write(" \b")

# y = 40 (40 + 12 = 52 au total )
# si y = 40 : dessine la base du tunnel à 40 donc fin de base à 46, 
# il faut donc dessiner de 46 à 56 des bases
# dans l'exemple :
# y = 40, 40+6(taille haut tunnel) = 46 => 56 - 46 = 10, a dessiner aux ordonnées 
                # 47
                # 48
                # ...
                # 56
def draw_tunnels_down(x,y):
    draw_element(tunnel_down, x, y)
    y += 4
    while(y<WINDOW_HEIGHT):
        draw_element(tunnel_base, x, y)
        y += 1
    
def draw_tunnels_up(x,y):
    draw_element(tunnel_up, x, y)
    while(y):
        y -= 1
        draw_element(tunnel_base, x, y)

def game_over():
    clear_screen()
    draw_element(game_over_text, screen_placement(WINDOW_LENGTH, 115, 0), 20)
    draw_element(try_again, screen_placement(WINDOW_LENGTH, 62, 0), 45)
    delay(3000)
    clear_screen()
    # need to exit while loop

def splash_screen_ending():
    clear_screen()
    draw_element(game_name, screen_placement(WINDOW_LENGTH, 130, 0), 20)
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

def draw_menu():
    draw_element(game_name,screen_placement(WINDOW_LENGTH, 130, 0), 10)
    draw_element(button_start, screen_placement(WINDOW_LENGTH, 43, 1), 35)
    draw_element(button_quit,(WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 43, 1), 35)
    draw_element(arrows, screen_placement(WINDOW_LENGTH, 30, 0), 32)
    draw_element(HELP, screen_placement(WINDOW_LENGTH, 50, 0),55)
    draw_last_score(200,58)

def blink_element( x,y):
    print(toggle)
    if toggle:
      draw_element(cursor,x,y)
    else:
      draw_element(cursor_shadow, x,y)

def choose_your_player_func():
    player_ok = False
    draw_element(birdython, screen_placement(WINDOW_LENGTH, 22, 1), (WINDOW_HEIGHT//2) - 7)
    draw_element(thon, (WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 20, 1),  (WINDOW_HEIGHT//2) - 7)
    draw_element(cursor, WINDOW_LENGTH//2, WINDOW_HEIGHT//2+15)
    i = 0
    while(not player_ok):
      i+=1
      print(i)
      blink_element(WINDOW_LENGTH//2, WINDOW_HEIGHT//2)
      if i == 2000:
        player_ok = True
    #return player


