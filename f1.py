from constants import *
from commun import *
from home_menu import *
import pyb

home_menu = Home_menu()
end_game = False
game_is_running = False

x = 25
y = 30

counter = 0

x1 = 60
x2 = 190

i = 0
erase_old_tunnel = False

splash_screen()

while(not end_game):
    draw_element(game_name, 25, 20)
    home_menu.draw_button(button_start, 30, 40)
    home_menu.draw_button(button_quit, 60, 40)
    # aera button start :
    # 30,40 -----(20)-----  50,40
    # -
    # -
    # -
    # 30,44 -----(20)-----  50,44
    x = 25
    y = 30
    delay(5000)
    clear_screen()
    game_is_running = True
    while(game_is_running):
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
                game_is_running = False
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