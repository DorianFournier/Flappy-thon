from commun import *
import pyb
import lis3dsh_driver

from pyb import Timer

end_game_state = False
game_is_running_state = False
erase_old_tunnel = False
start_or_quit = 0
player_caracter = """"""
i = 0
player_caracter_name = ""

splash_screen_loading()

while(not end_game_state):
    draw_menu()
    
    while(-300 < start_or_quit < 300):
        start_or_quit = lis3dsh_driver.get_acc_value()
        print("start or quit : ", start_or_quit)
        if start_or_quit < -300:
            game_is_running_state = True 
            player_caracter = choose_your_player()
            if player_caracter == birdy_player:
                player_caracter_name = birdy_player_label
            else:
                player_caracter_name = thon_player_label
            draw_element_bar(player_caracter_name)
        elif start_or_quit > 300:
            end_game_state = True

    x = 30
    y = screen_placement(WINDOW_HEIGHT, 14, 0)
    x_tunnel = 200
    score_counter = 0

    while(game_is_running_state):
        pattern_score_counter = transform_score_counter(score_counter)
        placement = 0
        for pattern in pattern_score_counter:
            draw_element(pattern, screen_placement(WINDOW_LENGTH, 32, 1) + (WINDOW_LENGTH//2) + 48 + placement, WINDOW_HEIGHT - 2)
            placement += 6

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
            if(y == 5):
                y = 6
            if(y == 45):
                game_over(score_counter)
                game_is_running_state = False
                break
        
        draw_tunnels_down(x_tunnel, 47)
        draw_tunnels_up(x_tunnel, 20)

        x_tunnel -= 1
        if (x_tunnel == 0):
            score_counter += 1
            erase_old_tunnel = True   
            x_tunnel = 200
        
        if (x+35) >= x_tunnel:
            if y <= 20:
                game_over(score_counter)
                game_is_running_state = False
            if y+13 >= 50:
                game_over(score_counter)
                game_is_running_state = False
        

        if erase_old_tunnel:
            i += 1
            draw_nothing(i)
            if i == 24:
                erase_old_tunnel = False
                i=0
    
splash_screen_ending()