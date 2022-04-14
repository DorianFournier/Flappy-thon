import pyb 
from pyb import UART, SPI, Pin, LED

WIDTH = 50
HEIGHT = 50

# UART init
uart_number = 2
uart = UART(uart_number)
uart.init(9600, bits=8, parity=None, stop=1)

#SPI init
CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI(1, SPI.MASTER, baudrate = 50000, polarity= 0, phase = 0)

#LED init
l1 = pyb.LED(1)
l3 = pyb.LED(2)
l4 = pyb.LED(3)
l2 = pyb.LED(4)

leds = [l1,l4,l2,l3]
led_px, led_nx, led_py, led_ny = LED(1), LED(2), LED(3), LED(4)

state_x = 30
state_y = 30
x_accel = 0
y_accel = 0

led = pyb.LED(2)
led.on()
pyb.delay(500)
led.toggle()

def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")


def move(x,y):
    uart.write("\x1b[{};{}H".format(y,x))


def read_register_value(address = 0x00, nb_bytes = 0):
    CS.low()
    SPI_1.send(address | 0x80)
 
    tab_values = SPI_1.recv(nb_bytes)
    CS.high()

    return tab_values


def write_data_in_register(address = 0x00, value = 0x00):
    """
    This method write data in a register
    Args : 
        - address : 
        - value   : 
    """
    CS.low()
    SPI_1.send(address)
    SPI_1.send(value)
    CS.high()


def read_acceleration(add):
    low = read_register_value(address= add, nb_bytes=1)
    high = read_register_value(address= add+1, nb_bytes=1)

    return convert_value(high, low)


def convert_value(high, low):
    high = int.from_bytes(high, "big", True)
    low  = int.from_bytes(low, "big", False)

    print("high : ", high)
    print("low : ", low)

    data = (high << 8) | low
    
    if(data & 0x8000):
        data = data - (1<<16)
    
    data = data * 0.06
    print("Data with conversion to mg : ", data)

    return data


def turn_off_led():
    for led in leds:
        led.off()


tab_values = read_register_value(address=0x0F, nb_bytes = 1)
print(f"WHO I AM : {tab_values[0]}")

write_data_in_register(address=0x20, value=0x77)
tab_values = read_register_value(address=0x20, nb_bytes=1)
print(f"CTRL_REG4 : {tab_values[0]}")

clear_screen()
move(state_x,state_y)
uart.write('+')

while True:
    print("==========  New data  ===========")
    x_accel = read_acceleration(0x28)
    y_accel = read_acceleration(0x2A)
    z_accel = read_acceleration(0x2C)
    
    # amazing telecran
    state_x_temp = state_x
    state_y_temp = state_y

    if (state_x <= WIDTH) or (state_x >= 10) :

        if x_accel > 325:
            state_x += 1
            move(state_x, state_y)

        if x_accel < -325:
            state_x -= 1
            move(state_x, state_y)

    if (state_y <= HEIGHT) or (state_y >= 10):

        if y_accel > 325:
            state_y -= 1
            move(state_x, state_y)
    
        if y_accel < -325:
            state_y += 1
            move(state_x, state_y)

    if (state_x != state_x_temp) or (state_y != state_y_temp):
        uart.write("#\b \b#")

    if state_x == WIDTH+1:
        state_x = WIDTH
    if state_y == HEIGHT+1:
        state_y = HEIGHT

    if state_x == 9:
        state_x = 0
    if state_y == 9:
        state_y = 0

    pyb.delay(100)

    # turn on/off led
    if x_accel > 300:
        turn_off_led()
        l1.on()
    elif x_accel < 200:
        turn_off_led()

    if x_accel < -300:
        turn_off_led()
        l3.on()
    elif x_accel < -200:
        turn_off_led()

    if y_accel > 300:
        turn_off_led()
        l4.on()
    elif y_accel < -200:
        turn_off_led()

    if y_accel < -300:
        turn_off_led()
        l2.on()
    elif y_accel < -200:
        turn_off_led()

    #print(f"x accel : {x_accel}")
    #print(f"y accel : {y_accel}")
    #print(f"z accel : {z_accel}")

#LED placement on STM32 : 
#               pyb.LED(3)
#   pyb.LED(2)              pyb.LED(1)
#               pyb.LED(4)  
