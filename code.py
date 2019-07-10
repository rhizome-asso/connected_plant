from analogio import AnalogIn
import board
import digitalio
import errno
import math
import neopixel
import time

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
n_samples = 10
sample_delay = 0.1  # seconds
delay = 300  # seconds

# files
temp_sensor_calibration = 'temp_sensor_calibration.csv'
plant_envdata = 'plant_envdata.csv'

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


def write_to_file(filename, row):
    try:
        with open(filename, "a") as f:
            f.write(", ".join([str(e) for e in row]) + "\n")
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


write_to_file(plant_envdata,["temperature 1", "temperature 2", "light"])
# main execution loop
while True:
    temp1 = 0.
    temp2 = 0.
    light = 0.
    for i in range(nb_samples):
        temp1 += get_temperature(sensor_temp_pin1)
        temp2 += get_temperature(sensor_temp_pin2)
        light += get_light(sensor_light_pin)
        time.sleep(sample_delay)
    # averaging the samples 
    temp1 /= nb_samples
    temp2 /= nb_samples
    light /= nb_samples
    write_to_file(plant_envdata,[temp1, temp2, light])
    # sleep for a long time! 
    time.sleep(delay)

