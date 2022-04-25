import pyb 
from pyb import UART, Pin, LED, Timer, delay
from constants import *

button_start = """
   _______________  
  |               | 
  |     START     | 
  |_______________| 
"""

button_best_score = """
   _______________  
  |               | 
  |  BEST SCORES  | 
  |_______________| 
"""

button_quit = """
   _______________  
  |               | 
  |     QUIT      | 
  |_______________| 
"""

button_back = """
   _______________  
  |               | 
  |     BACK      | 
  |_______________| 
"""


button_quit2 = """
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
▐     ___   _   _  ___  _____    ▌
▐    / _ \ | | | ||_ _||_   _|   ▌
▐   | (_) || |_| | | |   | |     ▌
▐    \__\_\ \___/ |___|  |_|     ▌
▐                                ▌
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

button_start2 = """
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
▐  ___  _____   _    __   _____  ▌
▐ / __||_   _| /_\  | _ \|_   _| ▌
▐ \__ \  | |  / _ \ |   /  | |   ▌
▐ |___/  |_| /_/ \_\|_|_\  |_|   ▌
▐                                ▌
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
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

tunnel_down = """
                          
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️  
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️  
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️  
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛    
"""

tunnel_down_shadow = """
                          
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️  
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️  
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️  
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛    
"""

tunnel_up = """ 
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛    
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️  
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️  
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️  
                          
"""

tunnel_base = """
   ⬛️🟩🟩🟩🟩🟩🟩🟩⬛   
"""

arrow_right  = """
          ⬛⬛
          ⬛🟨⬛
  ⬛⬛⬛⬛⬛🟨🟨⬛
  ⬛🟨🟨🟨🟨🟨⬛🟨⬛
  ⬛🟨🟨🟨🟨🟨🟨🟨⬛
  ⬛⬛⬛⬛⬛🟨🟨⬛
          ⬛🟨⬛
          ⬛⬛
"""

arrow_left = """
        ⬛⬛
      ⬛🟦⬛
    ⬛🟦🟦⬛⬛⬛⬛⬛
  ⬛🟦⬛🟦🟦🟦🟦🟦⬛
  ⬛🟦🟦🟦🟦🟦🟦🟦⬛
    ⬛🟦🟦⬛⬛⬛⬛⬛
      ⬛🟦⬛
        ⬛⬛
        """

arrows = """
      ⬛⬛
    ⬛🟦⬛
  ⬛🟦🟦⬛⬛⬛⬛⬛
⬛🟦⬛🟦🟦🟦🟦🟦⬛
⬛🟦🟦🟦🟦🟦🟦🟦⬛
  ⬛🟦🟦⬛⬛⬛⬛⬛   ⬛⬛
    ⬛🟦⬛           ⬛🟨⬛
      ⬛⬛   ⬛⬛⬛⬛⬛🟨🟨⬛
             ⬛🟨🟨🟨🟨🟨⬛🟨⬛
             ⬛🟨🟨🟨🟨🟨🟨🟨⬛
             ⬛⬛⬛⬛⬛🟨🟨⬛
                     ⬛🟨⬛
                     ⬛⬛
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

def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")

def move(x,y):
    uart.write("\x1b[{};{}H".format(y,x))

def screen_placement(window_parts = WINDOW_HEIGHT, element_size = 0, mode = 0):
    """
    mode : 0 => middle x
    mode : 1 => middle middle x
    mode : 2 => middle x,y 
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
    start_drawing_bases = y + 5
    y += 5
    for base in range(0, (WINDOW_DOWN-start_drawing_bases)):
        draw_element(tunnel_base, x, y)
        y += 1
    
def draw_tunnels_up(x,y):
    draw_element(tunnel_up, x, y)
    start_drawing_bases = y
    for base in range(0, (start_drawing_bases)):
        draw_element(tunnel_base, x, y)
        y -= 1

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