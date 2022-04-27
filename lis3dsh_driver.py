import pyb 
from pyb import SPI, Pin, LED

CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI(1, SPI.MASTER, baudrate = 50000, polarity= 0, phase = 0)

l1 = pyb.LED(1)
l3 = pyb.LED(2)
l4 = pyb.LED(3)
l2 = pyb.LED(4)

leds = [l1,l4,l2,l3]
led_px, led_nx, led_py, led_ny = LED(1), LED(2), LED(3), LED(4) 

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

    data = (high << 8) | low
    
    if(data & 0x8000):
        data = data - (1<<16)
    
    data = data * 0.06
    #print("Data with conversion to mg : ", data)

    return data

tab_values = read_register_value(address=0x0F, nb_bytes = 1)
print(f"WHO I AM : {tab_values[0]}")

write_data_in_register(address=0x20, value=0x77)
tab_values = read_register_value(address=0x20, nb_bytes=1)
print(f"CTRL_REG4 : {tab_values[0]}")

def turn_off_led():
    for led in leds:
        led.off()

def get_acc_value():
    who_i_am = read_register_value(address=0x0F, nb_bytes = 1)
    x_accel = 0
    if(who_i_am[0] == 0x3F):
        #print("==========  New data  ===========")
        x_accel = read_acceleration(0x28)
        
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

        pyb.delay(10)
        #print(f"x accel : {x_accel}")
    else:
        print("ACC NO AVAILABLE")

    return x_accel

"""
LED placement on STM32 : 
              pyb.LED(3)
pyb.LED(2) l3          l1 pyb.LED(1) 
              pyb.LED(4)  
"""