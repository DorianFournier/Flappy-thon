from constants import *
from commun import *
import home_menu
import pyb
import random

end_game = False
game_is_running = False
choose_your_player = False

x = 25
y = 30

score_counter = 0

x1 = 60
x2 = 190

i = 0
erase_old_tunnel = False

splash_screen()

while(not end_game):
    debug()

    #draw_element(game_name_2,((WINDOW_LENGTH//2)-(130//2)), 10)
    #draw_element(P1,((WINDOW_LENGTH//2)-(35//2)), 25)
    #home_menu.draw_button(button_start2, (((WINDOW_LENGTH//2)//2)-34//2), 35)
    #home_menu.draw_button(button_quit2,(WINDOW_LENGTH//2)+(((WINDOW_LENGTH//2)//2)-34//2), 35)
    #home_menu.draw_last_score(200,58)
    #draw_element(arrows, ((WINDOW_LENGTH//2)-15), 32)
    #draw_element(HELP, ((WINDOW_LENGTH//2)-50//2),50 )
    #draw_element(HELP2, ((WINDOW_LENGTH//2)-50//2), 53)

    draw_element(game_name,screen_placement(WINDOW_LENGTH, 130, 0), 10)
    draw_element(P1,screen_placement(WINDOW_LENGTH, 35, 0), 25)
    home_menu.draw_button(button_start2, screen_placement(WINDOW_LENGTH, 34, 1), 35)
    home_menu.draw_button(button_quit2,(WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 34, 1), 35)
    draw_element(arrows, screen_placement(WINDOW_LENGTH, 30, 0), 32)
    draw_element(HELP, screen_placement(WINDOW_LENGTH, 50, 0),50 )
    home_menu.draw_last_score(200,58)
    
    x = 25
    y = 30
    delay(5000)
    clear_screen()
    game_is_running = True  
    while(game_is_running):
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

        tunnel_base_up = random.randrange(0, 40)
        draw_tunnels_down(x1, 40)
        #draw_tunnels_down(x2, 50)
        draw_tunnels_up(x1, 20)
        #draw_tunnels_up(x2, 30)

        x1 -= 1
        #x2 -= 1
        if (x1 == 0):
            score_counter+=1
            erase_old_tunnel = True   
            x1 = 200
        #if (x2 == 0):
        #    erase_old_tunnel = True   
        #    x2 = 200
        
        if erase_old_tunnel:
            i+=1
            draw_nothing(i)
            if i == 24:
                erase_old_tunnel = False
                i=0