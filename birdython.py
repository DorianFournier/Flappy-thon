import pyb 
from pyb import UART, SPI, Pin, LED, Timer, delay

push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)
timer_counter = Timer(5, freq=0.2)

WINDOW_DOWN = 65
WINDOW_UP   = 0

x = 25
y = 30

counter = 0


x1 = 60
x2 = 190

i = 0
erase_old_tunnel = False
flag_game_running = False
flag_menu = False
flag_splash_screen = True

# UART init
uart_number = 2
uart = UART(uart_number)
uart.init(2_000_000, bits=8, parity=None, stop=1)

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

def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")

def move(x,y):
    uart.write("\x1b[{};{}H".format(y,x))

def draw_bridython(x, y):
    for index, line in enumerate(birdython.splitlines()):
        move(x, y+index)
        uart.write(line)

def draw_element(element, x, y):
    for index, line in enumerate(element.splitlines()):
        move(x, y+index)
        uart.write(line)

def spash_screen():
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

def timer(timer_counter):
    pyb.LED(1).toggle()

def game_over():
    clear_screen()
    draw_element(game_name, 50, 25)
    # need to exit while loop

#timer_counter.callback(led1)

#draw_bridython(25,10)
#clear_screen()

spash_screen()

while True:
    counter += 1
    if (y > 5) and (y < 45):
        print(f"y = {y}")
        if push_button.value():
            y = y-1
            draw_bridython(x,y)
        else:
            y = y+1
            draw_bridython(x,y)
    else:
        print(f"y = {y}")
        print("do not move")
        if(y == 5):
            y = 6
        if(y == 45):
            y = 44
            game_over()
            break

    draw_tunnels_down(x1, 40)
    draw_tunnels_down(x2, 50)
    draw_tunnels_up(x1, 20)
    draw_tunnels_up(x2, 30)

    x1 -= 1
    x2 -= 1
    if (x1 == 0):
        erase_old_tunnel = True   
        x1 = 200
    if (x2 == 0):
        erase_old_tunnel = True   
        x2 = 200
    
    if erase_old_tunnel:
        i+=1
        draw_nothing(i)
        if i == 24:
            erase_old_tunnel = False
            i=0
    
    # 🟧🟨🟩🟦🟪🟫🟥
