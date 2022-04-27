from commun import *
import pyb
import lis3dsh_driver

from pyb import Timer

end_game = False
game_is_running = False
erase_old_tunnel = False

x = 25
y = 30
score_counter = 0
x1 = 60
i = 0
start_or_quit = 0
player_caracter = """"""

splash_screen_loading()

while(not end_game):
    draw_menu()
    
    while(-300 < start_or_quit < 300):
        start_or_quit = lis3dsh_driver.get_acc_value()
        if start_or_quit < -300:
            game_is_running = True 
            x,y = 25, 30
            #global player_caracter
            player_caracter = choose_your_player()
        elif start_or_quit > 300:
            end_game = True

    while(game_is_running):
        start_or_quit = 0
        if (y > 5) and (y < 45):
            print(f"y = {y}")
            if push_button.value():
                if y == 6:
                    pass
                else:
                    y = y-1
                draw_element(player_caracter, x, y)
            else:
                y = y+1
                draw_element(player_caracter, x, y)
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