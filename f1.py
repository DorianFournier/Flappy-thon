from constants import PLAYER_HEIGHT, PLAYER_LENGTH, START_X_TUNNEL, X_PLAYER_CARACTER
import lis3dsh_driver
from commun import *

end_game_state = False
game_is_running_state = False
erase_old_tunnel = False
tunnel_already_draw = False
start_or_quit = 0
player_caracter = """"""
i = 0
player_caracter_name = ""

splash_screen_loading()
lis3dsh_driver.init_acc()

while(not end_game_state):
    draw_menu()

    while(-300 < start_or_quit < 300):
        start_or_quit = lis3dsh_driver.get_acc_value()
        blink_element(arrows, arrows_shadow, screen_placement(WINDOW_LENGTH,32,0), (WINDOW_HEIGHT//2)+1)
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

    y_player_caracter = screen_placement(WINDOW_HEIGHT, 14, 0)

    x_tunnel = START_X_TUNNEL
    y_tunnel_up = 0
    y_tunnel_down = 0

    score_counter = 0
    difficulty_level = "easy"
    tunnel_already_draw = False
    tunnel_up_base = ""
    tunnel_down_base = ""

    while(game_is_running_state):
        adapt_difficulty_level(score_counter)
        pattern_score_counter = transform_score_counter(score_counter)
        placement = 0
        for pattern in pattern_score_counter:
            draw_element(pattern, screen_placement(WINDOW_LENGTH, 32, 1) + (WINDOW_LENGTH//2) + 48 + placement, WINDOW_HEIGHT - 2)
            placement += 6

        start_or_quit = 0
        if (y_player_caracter > 0) and (y_player_caracter < 40):
            #print(f"y_player_caracter = {y_player_caracter}")
            if push_button.value():
                if y_player_caracter == 1:
                    pass
                else:
                    y_player_caracter = y_player_caracter-1
                draw_element(player_caracter, X_PLAYER_CARACTER, y_player_caracter)
            else:
                y_player_caracter = y_player_caracter+1
                draw_element(player_caracter, X_PLAYER_CARACTER, y_player_caracter)
        else:
            if(y_player_caracter == 0):
                y_player_caracter = 1
            if(y_player_caracter == 40):
                draw_element(player_shadow, X_PLAYER_CARACTER, y_player_caracter)
                y_player_caracter += 2
                game_over(player_caracter, score_counter, X_PLAYER_CARACTER, y_player_caracter)
                game_is_running_state = False
                break

        if not tunnel_already_draw:
            tunnel_already_draw = True
            y_tunnel_up = random_data_for_tunnel_up()
            y_tunnel_down = data_for_tunnel_down(y_tunnel_up, difficulty_level)
            tunnel_up_base = create_pattern_tunnel_up(y_tunnel_up)
            tunnel_down_base = create_pattern_tunnel_down(y_tunnel_down)

        draw_tunnels_up(tunnel_up_base, x_tunnel, y_tunnel_up)
        draw_tunnels_down(tunnel_down_base, x_tunnel, y_tunnel_down)

        x_tunnel -= 1
        if (x_tunnel == 0):
            score_counter += 1
            erase_old_tunnel = True
            tunnel_already_draw = False
            x_tunnel = START_X_TUNNEL

        if (X_PLAYER_CARACTER + PLAYER_LENGTH) >= x_tunnel:
            if y_player_caracter <= (y_tunnel_up + TUNNEL_HEIGHT):
                draw_element(player_shadow, X_PLAYER_CARACTER, y_player_caracter + 1)
                game_over(player_caracter, score_counter, X_PLAYER_CARACTER, y_player_caracter)
                game_is_running_state = False
            if (y_player_caracter + PLAYER_HEIGHT) >= y_tunnel_down:
                draw_element(player_shadow, X_PLAYER_CARACTER, y_player_caracter)
                game_over(player_caracter, score_counter, X_PLAYER_CARACTER, y_player_caracter + 1)
                game_is_running_state = False

        if erase_old_tunnel:
            i += 1
            draw_nothing(i)
            if i == 24:
                erase_old_tunnel = False
                i=0
    
splash_screen_ending()