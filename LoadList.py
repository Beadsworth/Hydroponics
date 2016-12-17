#!/usr/bin/env python
# imports
from HydroLoads import Load, Controller

# controller info
addr = '/dev/ttyACM0'
ard = Controller(addr)

# define pin locations
LED_RED = 2
LED_ORANGE = 3
LED_YELLOW = 4
LED_GREEN = 5
LED_BLUE = 6
LED_PURPLE = 7
LED_WHITE1 = 8
LED_WHITE2 = 9

# leds
red = Load(ard, LED_RED, 'red')
orange = Load(ard, LED_ORANGE, 'orange')
yellow = Load(ard, LED_YELLOW, 'yellow')
green = Load(ard, LED_GREEN, 'green')
blue = Load(ard, LED_BLUE, 'blue')
purple = Load(ard, LED_PURPLE, 'purple')
white1 = Load(ard, LED_WHITE1, 'white1')
white2 = Load(ard, LED_WHITE2, 'white2')

controllers = ard,


if __name__ == '__main__':
    pass
