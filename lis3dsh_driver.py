from pyb import SPI, Pin, delay

CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI(1, SPI.MASTER, baudrate = 50000, polarity= 0, phase = 0)

def read_register_value(address = 0x00, nb_bytes = 0):
    CS.low()
    SPI_1.send(address | 0x80)
 
    tab_values = SPI_1.recv(nb_bytes)
    CS.high()

    return tab_values

def write_data_in_register(address = 0x00, value = 0x00):
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

    return data

def init_acc():
    write_data_in_register(address=0x20, value=0x77)

def get_acc_value():
    who_i_am = read_register_value(address=0x0F, nb_bytes = 1)
    
    x_accel = 0

    if who_i_am[0] == 0x3F:
        x_accel = read_acceleration(0x28)
    else:
        print("ACC no available")
    return x_accel
