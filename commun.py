import random

from lis3dsh_driver import get_acc_value
from pyb import UART, Pin, Timer, delay
from constants import EASY_SPACE, GAME_START, HARD_SPACE, HELP_CHOOSE_PLAYER, HELP_CHOOSE_PLAYER_SHADOW, IMPOSSIBLE_SPACE, MEDIUM_SPACE, PLAYER_CHOOSE, TUNNEL_DOWN_MINIMUM_Y, TUNNEL_HEIGHT, WINDOW_HEIGHT, WINDOW_HEIGHT_RUNNING_STATE, WINDOW_LENGTH, LAST_SCORE, HELP

### Texts
button_start = """\
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
▐▌                                       ▐▌
▐▌ ▐█▀▀▀█ ▀▀▀██▀▀▀▐█▀▀▀█▌▐█▀▀▀█ ▀▀▀██▀▀▀ ▐▌
▐▌ ▐█▄▄▄▄    ▐▌   ▐█▄▄▄█▌▐█▄▄▄█    ▐▌    ▐▌
▐▌      █    ▐▌   ▐▌   ▐▌▐▌  ▐▌    ▐▌    ▐▌
▐▌ ▐█▄▄▄█    ▐▌   ▐▌   ▐▌▐▌   ▐▌   ▐▌    ▐▌
▐▌                                       ▐▌
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

button_quit = """\
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
▐▌                                       ▐▌
▐▌      ▐█▀▀▀█▌ ▐▌   ▐▌ ▐▌ ▀▀▀██▀▀▀      ▐▌
▐▌      ▐▌   ▐▌ ▐▌   ▐▌ ▐▌    ▐▌         ▐▌
▐▌      ▐▌  ▄▐▌ ▐▌   ▐▌ ▐▌    ▐▌         ▐▌
▐▌      ▐█▄▄▄█▌ ▐█▄▄▄█▌ ▐▌    ▐▌         ▐▌
▐▌            ▀                          ▐▌
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

game_name_label = """\
 ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄               ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄ 
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌             ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌              ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌                  ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌▐░▌    ▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌   ▄▄▄▄▄▄▄▄▄▄▄    ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌ ▐░▌   ▐░▌
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  ▐░░░░░░░░░░░▌   ▐░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀    ▀▀▀▀▀▀▀▀▀▀▀    ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌   ▐░▌ ▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌                       ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌    ▐░▌▐░▌
▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌               ▐░▌                       ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌     ▐░▐░▌
▐░▌          ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌               ▐░▌                       ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌
 ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀                 ▀                         ▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀ 
"""

try_again_label = """\
 ▀▀▀██▀▀▀▐█▀▀▀▀█ ▌    ▐    ▐█▀▀▀▀█▌▐█▀▀▀▀▀▐█▀▀▀▀█▌▐▌▐▌    ▐▌
    ▐▌   ▐█▄▄▄▄█ █▄▄▄▄█    ▐█▄▄▄▄█▌▐▌     ▐█▄▄▄▄█▌▐▌▐▌▐▌  ▐▌
    ▐▌   ▐▌  ▐▌    ▐▌      ▐▌    ▐▌▐▌ ▀▀▀█▐▌    ▐▌▐▌▐▌  ▐▌▐▌
    ▐▌   ▐▌   ▐▌   ▐▌      ▐▌    ▐▌▐█▄▄▄▄█▐▌    ▐▌▐▌▐▌    ▐▌
"""

loading_label = """\
▐▌    ▐█▀▀▀█▌▐█▀▀▀█▌▐█▀▀▄  ▐▌▐▌    ▐▌▐█▀▀▀▀▀ 
▐▌    ▐▌   ▐▌▐█▄▄▄█▌▐▌   ▐▌▐▌▐▌▐▌  ▐▌▐▌      
▐▌    ▐▌   ▐▌▐▌   ▐▌▐▌   ▐▌▐▌▐▌  ▐▌▐▌▐▌ ▀▀▀█ 
▐█▄▄▄▄▐█▄▄▄█▌▐▌   ▐▌▐█▄▄▀  ▐▌▐▌    ▐▌▐█▄▄▄▄█ 
"""

loading_bar_label = """\
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

loading_bar_content="""\
░░░░░░░░░░
"""

line_label = """\
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

choose_player_label = """\
▐█▀▀▀▀▐▌   ▐▌▐█▀▀▀█▌▐█▀▀▀█▌▐█▀▀▀█▐█▀▀▀▀    ▌    ▐▐█▀▀▀█▌▐▌   ▐▌▐█▀▀▀▀█    ▐█▀▀▀▀█▐▌    ▐█▀▀▀▀█▌▌    ▐▐█▀▀▀▀▐█▀▀▀▀█ 
▐▌    ▐▌   ▐▌▐▌   ▐▌▐▌   ▐▌▐█▄▄▄▄▐▌        █▄▄▄▄█▐▌   ▐▌▐▌   ▐▌▐█▄▄▄▄█    ▐█▄▄▄▄█▐▌    ▐█▄▄▄▄█▌█▄▄▄▄█▐▌    ▐█▄▄▄▄█
▐▌    ▐█▄▄▄█▌▐▌   ▐▌▐▌   ▐▌     █▐▌▀▀▀       ▐▌  ▐▌   ▐▌▐▌   ▐▌▐▌  ▐▌     ▐▌     ▐▌    ▐▌    ▐▌  ▐▌  ▐▌▀▀▀ ▐▌  ▐▌
▐█▄▄▄▄▐▌   ▐▌▐█▄▄▄█▌▐█▄▄▄█▌▐█▄▄▄█▐█▄▄▄▄      ▐▌  ▐█▄▄▄█▌▐█▄▄▄█▌▐▌   ▐▌    ▐▌     ▐█▄▄▄▄▐▌    ▐▌  ▐▌  ▐█▄▄▄▄▐▌   ▐▌ 
"""

see_you_soon_label = """\
▐█▀▀▀█▐█▀▀▀▀▐█▀▀▀▀    ▌    ▐▐█▀▀▀█▌▐▌   ▐▌    ▐█▀▀▀█▐█▀▀▀█▌▐█▀▀▀█▌▐▌    ▐▌
▐█▄▄▄▄▐▌    ▐▌        █▄▄▄▄█▐▌   ▐▌▐▌   ▐▌    ▐█▄▄▄▄▐▌   ▐▌▐▌   ▐▌▐▌▐▌  ▐▌    
     █▐▌▀▀▀ ▐▌▀▀▀       ▐▌  ▐▌   ▐▌▐▌   ▐▌         █▐▌   ▐▌▐▌   ▐▌▐▌  ▐▌▐▌
▐█▄▄▄█▐█▄▄▄▄▐█▄▄▄▄      ▐▌  ▐█▄▄▄█▌▐█▄▄▄█▌    ▐█▄▄▄█▐█▄▄▄█▌▐█▄▄▄█▌▐▌    ▐▌
"""

score_label = """\
█▀▀█▐█▀▀▀▐█▀▀█▌█▀▀▀█▐█▀▀▀   ▐▌  
█▄▄▄▐▌   ▐▌  ▐▌█▄▄▄█▐▌▄▄        
▄▄▄█▐█▄▄▄▐█▄▄█▌█  ▐▌▐█▄▄▄   ▐▌  
"""

game_over_label = """\
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄               ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░▌             ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░█▀▀▀▀▀▀▀█░▌ ▐░▌           ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
▐░▌          ▐░▌       ▐░▌▐░▌▐░▌ ▐░▌▐░▌▐░▌               ▐░▌       ▐░▌  ▐░▌         ▐░▌  ▐░▌          ▐░▌       ▐░▌
▐░▌ ▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌       ▐░▌   ▐░▌       ▐░▌   ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌     ▐░▌       ▐░▌    ▐░▌     ▐░▌    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░▌ ▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌   ▀   ▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░▌       ▐░▌     ▐░▌   ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀█░█▀▀ 
▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌               ▐░▌       ▐░▌      ▐░▌ ▐░▌      ▐░▌          ▐░▌     ▐░▌  
▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░█▄▄▄▄▄▄▄█░▌       ▐░▐░▌       ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌      ▐░▌ 
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌        ▐░▌        ▐░░░░░░░░░░░▌▐░▌       ▐░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀          ▀          ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀ 
"""

counter_3 = """\
 ▄▄▄▄▄▄▄▄▄▄ 
 ▀▀▀▀▀▀▀▀▀█▌
          ▐▌
 ▄▄▄▄▄▄▄▄▄█▌
 ▀▀▀▀▀▀▀▀▀█▌
          ▐▌
 ▄▄▄▄▄▄▄▄▄█▌
 ▀▀▀▀▀▀▀▀▀▀ 
"""

counter_2 = """\
 ▄▄▄▄▄▄▄▄▄▄ 
 ▀▀▀▀▀▀▀▀▀█▌
          ▐▌
          ▐▌
 ▄▄▄▄▄▄▄▄▄█▌
▐█▀▀▀▀▀▀▀▀▀ 
▐█▄▄▄▄▄▄▄▄▄ 
 ▀▀▀▀▀▀▀▀▀▀ 
"""

counter_1 = """\
     ▄▄     
    ▄█▌     
   ▐▌▐▌     
  ▐▌ ▐▌     
 ▀   ▐▌     
     ▐▌     
 ▄▄▄▄██▄▄▄▄ 
 ▀▀▀▀▀▀▀▀▀▀ 
"""

counter_0 = """\
 ▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄ 
▐█▀▀▀▀▀▀▀▀▀▐█▀▀▀▀▀▀▀█▌
▐▌         ▐▌       ▐▌
▐▌ ▄▄▄▄▄▄▄ ▐▌       ▐▌
▐▌ ▀▀▀▀▀▀█▌▐▌       ▐▌
▐▌       ▐▌▐▌       ▐▌
▐█▄▄▄▄▄▄▄█▌▐█▄▄▄▄▄▄▄█▌
 ▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀ 
"""
score_9 = """\
█▀▀█
█▄▄█
▄▄▄█
"""
score_8 = """\
█▀▀█
█▄▄█
█▄▄█
"""
score_7 = """\
█▀▀█
   █
   █
"""
score_6 = """\
█▀▀▀
█▄▄▄
█▄▄█
"""
score_5 = """\
█▀▀▀
█▄▄▄
▄▄▄█
"""
score_4 = """\
█   
█  █
▀▀▀█ 
"""
score_3 = """\
▀▀▀█
▄▄▄█
▄▄▄█ 
"""
score_2 = """\
▀▀▀█
█▀▀▀
█▄▄▄ 
"""
score_1 = """\
▄▐▌  
▀▐▌  
▄██▄ 
"""
score_0 = """\
█▀▀█ 
█  █ 
█▄▄█ 
"""

thon_player_label = """\
▀▀██▀▀ █   █ █▀▀▀█ █▌ █
  ▐▌   █▄▄▄█ █   █ █▐▌█
  ▐▌   █   █ █▄▄▄█ █ ▐█
"""
birdy_player_label = """\
█▀▀█  █ █▀▀▀▄ █▀▀▄ █  █
█▄▄██ █ █▀▀█▀ █  █ █▄▄█
█▄▄▄█ █ █   █ █▄▄▀  ▐▌
"""

### Players
birdy_player = """\
                          
⬛️⬛️⬛️      ⬛️⬛️⬛️⬛️⬛️⬛️  
⬛️🟧⬛️  ⬛️⬛️🟨🟨🟨🟨⬛️⬜️⬛️  
⬛️⬛️  ⬛️🟨🟨🟨🟨🟨⬛️⬜️⬜️⬜️⬛️  
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

birdy_player_game_over = """\
⬛️⬛️⬛️      ⬛️⬛️⬛️⬛️⬛️⬛️
⬛️🟧⬛️  ⬛️⬛️🟨🟨🟨🟨⬛️⬜️⬛️
⬛️⬛️  ⬛️🟨🟨🟨🟨🟨⬛️⬜️⬜️⬜️⬛️
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

thon_player = """\
                              
    ⬛️⬛️⬛️                ⬛️⬛️ 
      ⬛️                ⬛️🟧🟧⬛️ 
  ⬛️  ⬛️  ⬛️           ⬛️🟧🟧🟧⬛️ 
    ⬛️  ⬛️            ⬛️⬛️⬛️⬛️⬛️⬛️
⬛️            ⬛️⬛️⬛️⬛️⬛️          
⬛️⬛️      ⬛️⬛️🟦🟦🟦🟦🟦⬛️⬛️      
⬛️🟦⬛️  ⬛️🟦🟦🟦🟦🟦🟦⬛️🟦⬛️⬛️    
⬛️🟦🟦⬛️🟦🟦🟦🟦🟦🟦🟦⬛️🟦🟫🟦⬛️  
⬛️🟦⬜️⬛️🟦🟦🟦🟦⬜️⬜️⬜️⬛️🟦🟦🟦⬛️⬛️
⬛⬜️⬛️  ⬛️🟦⬜️⬜️⬜️⬜️⬜️⬜️⬛️🟦⬛️    
⬛️⬛️      ⬛️⬛️⬜️⬜️🟦🟦🟦⬛️⬛️  
⬛️            ⬛️⬛️⬛️⬛️⬛️    
                          
"""

thon_player_game_over = """\
    ⬛️⬛️⬛️                  ⬛️⬛️
      ⬛️                  ⬛️🟧🟧⬛️
  ⬛️  ⬛️  ⬛️             ⬛️🟧🟧🟧⬛️
    ⬛️  ⬛️              ⬛️⬛️⬛️⬛️⬛️⬛️
⬛️            ⬛️⬛️⬛️⬛️⬛️
⬛️⬛️      ⬛️⬛️🟦🟦🟦🟦🟦⬛️⬛️
⬛️🟦⬛️  ⬛️🟦🟦🟦🟦🟦🟦⬛️🟦⬛️⬛️
⬛️🟦🟦⬛️🟦🟦🟦🟦🟦🟦🟦⬛️🟦🟫🟦⬛️
⬛️🟦⬜️⬛️🟦🟦🟦🟦⬜️⬜️⬜️⬛️🟦🟦🟦⬛️⬛️
⬛⬜️⬛️  ⬛️🟦⬜️⬜️⬜️⬜️⬜️⬜️⬛️🟦⬛️
⬛️⬛️      ⬛️⬛️⬜️⬜️🟦🟦🟦⬛️⬛️
⬛️            ⬛️⬛️⬛️⬛️⬛️
"""

player_shadow = """\
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
"""

### Tunnels
tunnel_down = """\
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛   
"""

tunnel_up = """\
   ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛   
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
 ⬛️🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛️ 
 ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️ 
"""

tunnel_base = """\
   ⬛️🟩🟩🟩🟩🟩🟩🟩⬛   
"""

arrows = """\
      ⬛⬛
    ⬛🟦⬛
  ⬛🟦🟦⬛⬛⬛⬛⬛
⬛🟦⬛🟦🟦🟦🟦🟦⬛
⬛🟦🟦🟦🟦🟦🟦🟦⬛
  ⬛🟦🟦⬛⬛⬛⬛⬛  ⬛⬛
    ⬛🟦⬛          ⬛🟨⬛
      ⬛⬛  ⬛⬛⬛⬛⬛🟨🟨⬛
            ⬛🟨🟨🟨🟨🟨⬛🟨⬛
            ⬛🟨🟨🟨🟨🟨🟨🟨⬛
            ⬛⬛⬛⬛⬛🟨🟨⬛
                    ⬛🟨⬛
                    ⬛⬛
"""

cursor = """\
     ⬛⬛⬛    
   ⬛🟦⬛🟨⬛   
 ⬛🟦🟦⬛🟨🟨⬛ 
 ⬛⬛⬛⬛⬛⬛⬛ 
"""

cursor_shadow = """\
                 
                 
                 
                 
"""

# UART init
uart_number = 2
uart = UART(uart_number)
uart.init(2_000_000, bits=8, parity=None, stop=1)

# Push button init
push_button = Pin("PA0", Pin.IN, Pin.PULL_DOWN)

# Timer init
t_counter = Timer(4, freq=2)

def counter_timer(t_counter):
    global toggle_var
    global counter_var
    counter_var += 1
    toggle_var = not toggle_var

toggle_var = False
counter_var = 0

t_counter.callback(counter_timer)

choose_player_flag = False

def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")

def move(x,y):
    uart.write("\x1b[{};{}H".format(y,x))

def screen_placement(window_parts = WINDOW_HEIGHT, element_size = 0, mode = 0):
    """
    mode : 0 => middle x
    mode : 1 => middle middle x
    """
    if mode:
      placement = ((window_parts//2)//2)-(element_size//2)
    else:
      placement = (window_parts//2)-(element_size//2)
    return placement

def draw_element(element, x, y):
    for index, line in enumerate(element.splitlines()):
        move(x, y+index)
        uart.write(line)

def splash_screen_loading():
    clear_screen()
    draw_element(game_name_label, screen_placement(WINDOW_LENGTH, 130, 0), 20)
    draw_element(loading_label, screen_placement(WINDOW_LENGTH, 44, 0), 35)
    draw_element(loading_bar_label, screen_placement(WINDOW_LENGTH, 40, 0), 43)
    i = 0
    while (counter_var < 10):
      delay(500)
      if (counter_var % 2 == 0):
        draw_element(loading_bar_content, screen_placement(WINDOW_LENGTH, 50, 0)+i, 44)
      i += 5

    clear_screen()

def draw_nothing(col):
    for i in range (0, WINDOW_HEIGHT_RUNNING_STATE):
        move(col, i)
        uart.write(" \b")

def draw_tunnels_down(x,y):
    draw_element(tunnel_down, x, y)
    y += 4
    while(y < WINDOW_HEIGHT_RUNNING_STATE):
        draw_element(tunnel_base, x, y)
        y += 1
    
def draw_tunnels_up(x,y):
    draw_element(tunnel_up, x, y)
    while(y):
        y -= 1
        draw_element(tunnel_base, x, y)

def game_over(player_caracter ,last_score, x, y):
    counter_temp = counter_var
    if player_caracter == birdy_player:
      game_over_player = birdy_player_game_over
    else:
      game_over_player = thon_player_game_over
    while (counter_var < counter_temp + 6):
      blink_element(game_over_player, player_shadow, x, y)
    clear_screen()
    draw_element(game_over_label, screen_placement(WINDOW_LENGTH, 115, 0), 20)
    draw_element(try_again_label, screen_placement(WINDOW_LENGTH, 62, 0), 35)
    add_last_score(last_score)
    delay(3000)
    clear_screen()

def splash_screen_ending():
    clear_screen()
    draw_element(game_name_label, screen_placement(WINDOW_LENGTH, 130, 0), 20)
    draw_element(see_you_soon_label, screen_placement(WINDOW_LENGTH, 74, 0), 35)
    delay(3000)
    clear_screen()

def user_name():
    move(10,10)
    uart.write("ENTER YOUR de :")
    username = input("ENTER YOUR NAME")
    uart.write(username)

def draw_last_score(x, y):
    data = []
    with open('last_scores.txt', 'r') as file_last_scores:
        data = file_last_scores.readlines()
        
    if data:
        last_score =  data[-1]
    else:
        last_score = '0'

    move(x, y)
    uart.write(LAST_SCORE + last_score)

def add_last_score(last_score):
    with open('last_scores.txt', 'w') as file_last_scores:
        file_last_scores.write(str(last_score))

def draw_menu():
    draw_element(game_name_label,screen_placement(WINDOW_LENGTH, 130, 0), 10)
    draw_element(button_start, screen_placement(WINDOW_LENGTH, 44, 1), 33)
    draw_element(button_quit,(WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 44, 1), 33)
    draw_element(arrows, screen_placement(WINDOW_LENGTH, 32, 0), 30)
    draw_element(HELP, screen_placement(WINDOW_LENGTH, 50, 0),55)
    draw_last_score(200,58)

def blink_element(first_element, second_element, x,y):
    if toggle_var:
      draw_element(first_element,x,y)
    else:
      draw_element(second_element, x,y)

def choose_your_player():
    clear_screen()
    choose_player_flag = False

    draw_element(birdy_player, screen_placement(WINDOW_LENGTH, 36, 1), (WINDOW_HEIGHT//2) - 7)
    draw_element(thon_player, (WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 36, 1),  (WINDOW_HEIGHT//2) - 7)
    draw_element(choose_player_label, screen_placement(WINDOW_LENGTH, 115, 0),5)
    draw_element(HELP_CHOOSE_PLAYER, screen_placement(WINDOW_LENGTH, 53, 0), 15)

    counter_temp = counter_var
    while (counter_var < counter_temp + 4):
      blink_element(cursor, cursor_shadow, screen_placement(WINDOW_LENGTH,17,0), WINDOW_HEIGHT//2+15)

    while(not choose_player_flag):
      
      blink_element(cursor, cursor_shadow, screen_placement(WINDOW_LENGTH,17,0), WINDOW_HEIGHT//2+15)
      choose_player_acc_data = get_acc_value()
      
      if choose_player_acc_data < -300:
          player_choose = birdy_player
          choose_player_flag = True
      elif choose_player_acc_data > 300:
          player_choose = thon_player
          choose_player_flag = True
    
    draw_element(cursor_shadow, screen_placement(WINDOW_LENGTH,17,0), WINDOW_HEIGHT//2+15)
    draw_element(HELP_CHOOSE_PLAYER_SHADOW,screen_placement(WINDOW_LENGTH, 53, 0), 15)

    draw_element(GAME_START, screen_placement(WINDOW_LENGTH, 23, 0), 22)
    counter_temp = counter_var
    while (counter_var < counter_temp + 8):
      if player_choose == birdy_player:
        draw_element(PLAYER_CHOOSE + "BIRDY PLAYER !", screen_placement(WINDOW_LENGTH, 33, 0), 45)
        blink_element(cursor, cursor_shadow, screen_placement(WINDOW_LENGTH, 10, 1), (WINDOW_HEIGHT//2) +15)
      else:
        draw_element(PLAYER_CHOOSE + "THON PLAYER !", screen_placement(WINDOW_LENGTH, 28, 0), 45)
        blink_element(cursor, cursor_shadow, (WINDOW_LENGTH//2)+screen_placement(WINDOW_LENGTH, 10, 1), (WINDOW_HEIGHT//2) +15)
      if counter_var == counter_temp:
        draw_element(counter_3, screen_placement(WINDOW_LENGTH, 12, 0), screen_placement(WINDOW_HEIGHT, 8, 0))
      if counter_var == (counter_temp + 2):
        draw_element(counter_2, screen_placement(WINDOW_LENGTH, 12, 0), screen_placement(WINDOW_HEIGHT, 8, 0))
      if counter_var == (counter_temp + 4):
        draw_element(counter_1, screen_placement(WINDOW_LENGTH, 12, 0), screen_placement(WINDOW_HEIGHT, 8, 0))
      if counter_var == (counter_temp + 6):
        draw_element(counter_0, screen_placement(WINDOW_LENGTH, 22, 0), screen_placement(WINDOW_HEIGHT, 8, 0))
    clear_screen()
    return player_choose

def transform_score_counter(score_counter):
    pattern_score_counter = ["","","","",""]
    digits_score_counter = [int(a) for a in str(score_counter)]
    placement = 0
    for digit in digits_score_counter:
      if digit == 0:
        pattern_score_counter[placement] = score_0
      if digit == 1:
        pattern_score_counter[placement] = score_1
      if digit == 2:
        pattern_score_counter[placement] = score_2
      if digit == 3:
        pattern_score_counter[placement] = score_3
      if digit == 4:
        pattern_score_counter[placement] = score_4
      if digit == 5:
        pattern_score_counter[placement] = score_5
      if digit == 6:
        pattern_score_counter[placement] = score_6
      if digit == 7:
        pattern_score_counter[placement] = score_7
      if digit == 8:
        pattern_score_counter[placement] = score_8
      if digit == 9:
        pattern_score_counter[placement] = score_9
      placement +=1

    return pattern_score_counter

def draw_element_bar(player_name):
    draw_element(line_label, 0, WINDOW_HEIGHT - 4)
    draw_element(score_label, screen_placement(WINDOW_LENGTH, 32, 1) + (WINDOW_LENGTH//2) + 15,WINDOW_HEIGHT - 2)
    draw_element(player_name, 3,WINDOW_HEIGHT-2)

def random_data_for_tunnel_up():
    random_data_tunnel_up = random.randrange(3,21)
    print("random_data_tunnel_up : ",random_data_tunnel_up)

    return random_data_tunnel_up

def data_for_tunnel_down(y_tunnel_up, difficulty_level):
    y_tunnel_down = 0

    if difficulty_level == "easy":
      y_tunnel_down = y_tunnel_up + TUNNEL_HEIGHT + EASY_SPACE
    if difficulty_level == "medium":
      y_tunnel_down = y_tunnel_up + TUNNEL_HEIGHT + MEDIUM_SPACE
    if difficulty_level == "hard":
      y_tunnel_down = y_tunnel_up + TUNNEL_HEIGHT + HARD_SPACE
    if difficulty_level == "impossible":
      y_tunnel_down = y_tunnel_up + TUNNEL_HEIGHT + IMPOSSIBLE_SPACE
  
    print("y_tunnel_down : ", y_tunnel_down)

    return y_tunnel_down

def adapt_difficulty_level(score_counter):
    if score_counter < 4 :
      difficulty_level = "easy"
    elif 4 < score_counter < 8:
      difficulty_level = "medium"
    elif 8 < score_counter < 12:
      difficulty_level = "hard"
    else:
      difficulty_level = "impossible"

    return difficulty_level