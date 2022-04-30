import lis3dsh_driver

from constants import ACC_DATA_MOVE_RIGHT, ACC_DATA_MOVE_LEFT,\
    PLAYER_HEIGHT, PLAYER_LENGTH, START_X_TUNNEL, TUNNEL_LENGTH,\
    X_PLAYER_CARACTER, WINDOW_HEIGHT, WINDOW_LENGTH, TUNNEL_HEIGHT
from commun import coo_y__for_tunnel_up, coo_y_for_tunnel_down,\
    splash_screen_loading, splash_screen_ending, draw_menu,\
    blink_element, screen_placement, choose_your_player, draw_element,\
    draw_element_bar, adapt_difficulty_level, transform_score_counter,\
    push_button, game_over, create_pattern_tunnel_down, draw_nothing,\
    create_pattern_tunnel_up, draw_tunnels_down, draw_tunnels_up
from graphic_elements import arrows, arrows_shadow, birdy_player_label,\
    thon_player_label, player_shadow, birdy_player

end_game_state = False
game_is_running_state = False

erase_old_tunnel = False

start_or_quit_menu = 0

player_caracter = ""
player_caracter_name = ""

column = 0

lis3dsh_driver.init_acc()
splash_screen_loading()

while(not end_game_state):
    draw_menu()

    while(ACC_DATA_MOVE_LEFT < start_or_quit_menu < ACC_DATA_MOVE_RIGHT):
        start_or_quit_menu = lis3dsh_driver.get_acc_value()
        blink_element(arrows, arrows_shadow, screen_placement(
            WINDOW_LENGTH, 32, 0), (WINDOW_HEIGHT//2) + 1)

        if start_or_quit_menu < ACC_DATA_MOVE_LEFT:
            game_is_running_state = True
            player_caracter = choose_your_player()
            if player_caracter == birdy_player:
                player_caracter_name = birdy_player_label
            else:
                player_caracter_name = thon_player_label
            draw_element_bar(player_caracter_name)
        elif start_or_quit_menu > ACC_DATA_MOVE_RIGHT:
            end_game_state = True

    y_player_caracter = screen_placement(WINDOW_HEIGHT, PLAYER_HEIGHT, 0)

    x_tunnel = START_X_TUNNEL
    y_tunnel_up = 0
    y_tunnel_down = 0

    score_counter = 0
    difficulty_level = "easy"
    tunnel_already_draw = False
    tunnel_up_base = ""
    tunnel_down_base = ""

    while(game_is_running_state):
        difficulty_level = adapt_difficulty_level(score_counter)
        pattern_score_counter = transform_score_counter(score_counter)
        placement = 0
        for pattern in pattern_score_counter:
            draw_element(pattern, screen_placement(
                WINDOW_LENGTH, 32, 1) + (WINDOW_LENGTH//2) + 48 + placement, WINDOW_HEIGHT - 2)
            placement += 6

        start_or_quit_menu = 0
        if (y_player_caracter > 1) and (y_player_caracter < 40):
            #print(f"y_player_caracter = {y_player_caracter}")
            if push_button.value():
                if y_player_caracter == 2:
                    pass
                else:
                    y_player_caracter = y_player_caracter - 1
                draw_element(player_caracter, X_PLAYER_CARACTER,
                             y_player_caracter)
            else:
                y_player_caracter = y_player_caracter + 1
                draw_element(player_caracter, X_PLAYER_CARACTER,
                             y_player_caracter)
        else:
            if(y_player_caracter == 1):
                y_player_caracter = 2
                # collision with the ground
            if(y_player_caracter == 40):
                draw_element(player_shadow, X_PLAYER_CARACTER,
                             y_player_caracter)
                y_player_caracter += 2
                game_over(player_caracter, score_counter,
                          X_PLAYER_CARACTER, y_player_caracter)
                game_is_running_state = False
                break

        if not tunnel_already_draw:
            tunnel_already_draw = True
            y_tunnel_up = coo_y__for_tunnel_up()
            y_tunnel_down = coo_y_for_tunnel_down(
                y_tunnel_up, difficulty_level)
            tunnel_up_base = create_pattern_tunnel_up(y_tunnel_up)
            tunnel_down_base = create_pattern_tunnel_down(y_tunnel_down)

        draw_tunnels_up(tunnel_up_base, x_tunnel)
        draw_tunnels_down(tunnel_down_base, x_tunnel, y_tunnel_down)

        x_tunnel -= 1
        if (x_tunnel == 0):
            score_counter += 1
            erase_old_tunnel = True
            tunnel_already_draw = False
            x_tunnel = START_X_TUNNEL

        if (X_PLAYER_CARACTER + PLAYER_LENGTH) >= x_tunnel:
            # collision with upper tunnel
            if y_player_caracter <= (y_tunnel_up + TUNNEL_HEIGHT):
                draw_element(player_shadow, X_PLAYER_CARACTER,
                             y_player_caracter + 1)
                game_over(player_caracter, score_counter,
                          X_PLAYER_CARACTER, y_player_caracter + 1)
                game_is_running_state = False
            # collision with lower tunnel
            if (y_player_caracter + PLAYER_HEIGHT) >= y_tunnel_down:
                draw_element(player_shadow, X_PLAYER_CARACTER,
                             y_player_caracter)
                game_over(player_caracter, score_counter,
                          X_PLAYER_CARACTER, y_player_caracter + 1)
                game_is_running_state = False

        if erase_old_tunnel:
            column += 1
            draw_nothing(column)
            if column == TUNNEL_LENGTH:
                erase_old_tunnel = False
                column = 0

splash_screen_ending()
