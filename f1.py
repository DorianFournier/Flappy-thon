from constants import *
from commun import *
import pyb
import random
import lis3dsh_driver
from pyb import Timer

end_game = False
game_is_running = False
choose_your_player = False

x = 25
y = 30
#t_counter = Timer(4, freq=1)

score_counter = 0

x1 = 60
x2 = 190

i = 0
erase_old_tunnel = False
start_or_quit = 0

splash_screen()
player = " "

while(not end_game):
    draw_menu()
    
    while(-300 < start_or_quit < 300):
        start_or_quit = lis3dsh_driver.get_acc_value()
        print("startorquit : ", start_or_quit)
        if start_or_quit < -300:
            game_is_running = True 
            x,y = 25, 30
            clear_screen()
            #t_counter.callback(counter_timer)
            choose_your_player_func()
        elif start_or_quit > 300:
            end_game = True

    while(game_is_running):
        start_or_quit = 0

        #choose_your_player_func()
        clear_screen()
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
        random_data = random.randrange(0,67)
        print(random_data)
        
        tunnel_base_up = random.randrange(0, 40)
        draw_tunnels_down(x1, 40)
        draw_tunnels_up(x1, 20)

        x1 -= 1
        if (x1 == 0):
            score_counter+=1
            erase_old_tunnel = True   
            x1 = 200

        if erase_old_tunnel:
            i+=1
            draw_nothing(i)
            if i == 24:
                erase_old_tunnel = False
                i=0

splash_screen_ending()