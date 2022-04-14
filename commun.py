import pyb 
from pyb import UART, Pin, LED, Timer, delay

button_start = """
   _______________  
  |               | 
  |     START     | 
  |_______________| 

"""

button_best_score = """
   _______________  
  |               | 
  |    RECORD     | 
  |_______________| 

"""

button_quit = """
   _______________  
  |               | 
  |     QUIT      | 
  |_______________| 

"""

button_back = """
   _______________  
  |               | 
  |     BACK      | 
  |_______________| 

"""

# UART init
uart_number = 2
uart = UART(uart_number)
uart.init(2_000_000, bits=8, parity=None, stop=1)

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