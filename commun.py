import pyb 
from pyb import UART, Pin, LED, Timer, delay
from constants import *

button_start = """
   _______________  
  |               | 
  |     START     | 
  |_______________| 
"""

button_best_score = """é
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

game_name = """
 _____  _       ____  ____   __ __  ______  __ __   ___   ____  
|     || |     /    ||    \ |  |  ||      ||  |  | /   \ |    \ 
|   __|| |    |  o  ||  o  )|  |  ||      ||  |  ||     ||  _  |
|  |_  | |___ |     ||   _/ |  ~  ||_|  |_||  _  ||  O  ||  |  |
|   _] |     ||  _  ||  |   |___, |  |  |  |  |  ||     ||  |  |
|  |   |     ||  |  ||  |   |     |  |  |  |  |  ||     ||  |  |
|__|   |_____||__|__||__|   |____/   |__|  |__|__| \___/ |__|__|
                                                                
"""

game_over = """

  ____   ____  ___ ___    ___       ___   __ __    ___  ____  
 /    | /    ||   |   |  /  _]     /   \ |  |  |  /  _]|    \ 
|   __||  o  || _   _ | /  [_     |     ||  |  | /  [_ |  D  )
|  |  ||     ||  \_/  ||    _]    |  O  ||  |  ||    _]|    / 
|  |_ ||  _  ||   |   ||   [_     |     ||  :  ||   [_ |    \ 
|     ||  |  ||   |   ||     |    |     | \   / |     ||  .  \
|___,_||__|__||___|___||_____|     \___/   \_/  |_____||__|\_|
                                                              
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

tunnel_down = """
                          
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

def draw_element(element, x, y):
    for index, line in enumerate(element.splitlines()):
        move(x, y+index)
        uart.write(line)

def splash_screen():
    clear_screen()
    draw_element(game_name, 50, 25)
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
    draw_element(game_name, 50, 25)
    clear_screen()
    # need to exit while loop
