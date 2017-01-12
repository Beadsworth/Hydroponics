#!/usr/bin/env python
# imports
from Elements import Load, Controller, DigitalSensor, Relay

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
red = Relay(ard, LED_RED, 'red')
orange = Relay(ard, LED_ORANGE, 'orange')
yellow = Relay(ard, LED_YELLOW, 'yellow')
green = Relay(ard, LED_GREEN, 'green')
blue = Relay(ard, LED_BLUE, 'blue')
purple = Relay(ard, LED_PURPLE, 'purple')
white1 = Relay(ard, LED_WHITE1, 'white1')
white2 = Relay(ard, LED_WHITE2, 'white2')

level = DigitalSensor(ard, 12, 'level_sensor')

controllers = ard,


if __name__ == '__main__':
    pass
