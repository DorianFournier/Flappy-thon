import pyb 
from pyb import UART, SPI, Pin, LED, Timer, delay
import commun
from commun import *

timer_counter = Timer(5, freq=0.2)

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



splash_screen()

while True:
    counter += 1
    if (y > 5) and (y < 45):
        print(f"y = {y}")
        if push_button.value():
            y = y-1
            draw_element(birdython, x,y)
        else:
            y = y+1
            draw_element(birdython, x,y)
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
