from analogio import AnalogIn
import board
import digitalio
import math
import neopixel
import time

# RUN MODE:
CALLIBRATION = 1
MEASUREMENT = 2

run_mode = CALLIBRATION

# pins
led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

sensor_temp_pin1 = AnalogIn(board.A1)
sensor_temp_pin2 = AnalogIn(board.A2)

sensor_light_pin = AnalogIn(board.A0)

# constants
MAX_VAL = 65536
R1 = 10500  # Ohms
Vin = 3.3  # Volts
B = 3470

# files
csv_filenames = {
        CALLIBRATION: 'temp_sensor_calibration.csv',
        MEASUREMENT: 'plant_envdata.csv',
        }

# colors
RED = (0x10, 0, 0)
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
OFF = (0, 0, 0)

# neopixel - setup and test
status = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
status[0] = BLUE
time.sleep(0.3)
status[0] = OFF

# I/O errors

ENOENT = 2 # no such file/directory
ENOSPC = 28 # no space left
EROFS =  30 # read-only filesystem

error_codes = {
    0: (RED, 0.3),  # default
    ENOSPC: (RED, 0.5),
    EROFS: (RED, 0.1),
}

def file_exists(filename):
    try:
        f = open(filename)
        f.close()
    except OSError as e:
        if e.args[0] == ENOENT:
            return False
        else:
            raise e
    return True

def write_to_file(filename, row):
    line =  ", ".join([str(e) for e in row])
    try:
        with open(filename, "a") as f:
            f.write(line + "\n")
        status[0] = GREEN
        time.sleep(0.1)
        status[0] = OFF
    except OSError as e:
        if e.args[0] == EROFS:
            print(line)
        else:
            print("Error (%d) opening file: %s"%(e.args[0], filename))
            response = error_codes.get(e.args[0], error_codes[0])
            while True:
                status[0] = response[0]
                time.sleep(response[1])
                status[0] = OFF
                time.sleep(response[1])


def get_temperature(temp_pin):
    # acquire pin value, calculate voltage, then resistance
    # and finally temperature
    # YOUR CODE 
    return 0


def get_light(temp_pin):
    # acquire pin value, calculate volate and return it
    # YOUR CODE
    return 0


def measurement_mode():
    n_samples = 10
    sample_delay = 0.1  # seconds
    delay = 300  # seconds
    
    if not file_exists(csv_filenames[MEASUREMENT]):
        write_to_file(csv_filenames[MEASUREMENT], ["temperature 1", "temperature 2", "light", "restart"])
    restart = 1
    # main execution loop
    while True:
        temp1 = 0.
        temp2 = 0.
        light = 0.
        status[0] = YELLOW
        # we want to average over n_samples for temp1, temp2 and light
        # YOUR CODE
        status[0] = OFF
        write_to_file(csv_filenames[MEASUREMENT], [temp1, temp2, light, restart])
        restart = 0
        # sleep for a long time! 
        time.sleep(delay)


def callibration_mode():
    n_samples = 5
    delay = 0.5  # seconds
    
    if not file_exists(csv_filenames[CALLIBRATION]):
        write_to_file(csv_filenames[CALLIBRATION], ["temperature 1", "temperature 2"])
    # main execution loop
    while True:
        temp1 = 0.
        temp2 = 0.
        status[0] = YELLOW
        # we want to average over n_samples for temp1 and temp2
        # YOUR CODE
        status[0] = OFF
        write_to_file(csv_filenames[CALLIBRATION], [temp1, temp2])
        # sleep for a bit 
        time.sleep(delay)



# main program:

if run_mode == CALLIBRATION:
    callibration_mode()
elif run_mode == MEASUREMENT:
    measurement_mode()
else:
    print("Mode %d does not exist\n"%run_mode)


