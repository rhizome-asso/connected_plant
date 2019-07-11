from analogio import AnalogIn
import board
import digitalio
import errno
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
Vout = 3.3  # Volts
B = 3470

# files
csv_filenames = ['temp_sensor_calibration.csv',
                 'plant_envdata.csv']

# colors
nocolor = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [0, 255, 255]

# neopixel
status = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
status[0] = blue
time.sleep(0.3)
status[0] = nocolor


error_codes = {
    0: (red, 0.3),  # default
    errno.ENOSPC: (red, 0.5),
    errno.EROFS: (red, 0.1),
}

def file_exists(filename):
    try:
        f = open(filename)
        f.close()
    except IOError as e:
        if e.args[0] == errno.ENOENT):
            return False
        else:
            raise e
    return True

def write_to_file(filename, row):
    try:
        with open(filename, "a") as f:
            f.write(", ".join([str(e) for e in row]) + "\n")
        status[0] = green
        time.sleep(0.1)
        status[0] = nocolor
    except IOError as e:
        print("Error opening file:", fname)
        response = error_codes.get(e.args[0], error_codes[0])
        while True:
            status[0] = response[0]
            time.sleep(respone[1])
            status[0] = nocolor
            time.sleep(respone[1])


def get_temperature(temp_pin):
    sensor_voltage = temp_pin.value * Vout / MAX_VAL
    sensor_resistance = R1 * (Vout / sensor_voltage - 1)
    temperature_kelvin = 1.0 / (
        1.0 / 298.15 + 1.0 / B * math.log(sensor_resistance / 10000)
    )
    return temperature_kelvin - 273.15


def get_light(temp_pin):
    return sensor_light_pin.value * Vout / MAX_VAL


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
        status[0] = yellow
        for i in range(nb_samples):
            temp1 = temp1 + get_temperature(sensor_temp_pin1)
            temp2 = temp2 + get_temperature(sensor_temp_pin2)
            light = light + get_light(sensor_light_pin)
            time.sleep(sample_delay)
        status[0] = nocolor
        # averaging the samples 
        temp1 = temp1 / nb_samples
        temp2 = temp2 / nb_samples
        light = light / nb_samples
        write_to_file(csv_filenames[MEASUREMENT], [temp1, temp2, light, restart])
        restart = 0
        # sleep for a long time! 
        time.sleep(delay)


def callibration_mode():
    n_samples = 3
    delay = 0.1  # seconds
    
    if not file_exists(csv_filenames[CALLIBRATION]):
        write_to_file(csv_filenames[CALLIBRATION], ["temperature 1", "temperature 2"])
    # main execution loop
    while True:
        temp1 = 0.
        temp2 = 0.
        status[0] = yellow
        for i in range(nb_samples):
            temp1 = temp1 + get_temperature(sensor_temp_pin1)
            temp2 = temp2 + get_temperature(sensor_temp_pin2)
        status[0] = nocolor
        # averaging the samples 
        temp1 = temp1 / nb_samples
        temp2 = temp2 / nb_samples
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


