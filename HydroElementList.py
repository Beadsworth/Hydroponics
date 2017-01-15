import Elements


# controller info
addr = '/dev/ttyACM0'
ard = Elements.Controller(addr)

# define pin locations
LED_RED = 2
LED_ORANGE = 3
LED_YELLOW = 4
LED_GREEN = 5
LED_BLUE = 6
LED_PURPLE = 7
LED_WHITE1 = 8
LED_WHITE2 = 9

# LEDs
red = Elements.Relay(ard, LED_RED, 'red')
orange = Elements.Relay(ard, LED_ORANGE, 'orange')
yellow = Elements.Relay(ard, LED_YELLOW, 'yellow')
green = Elements.Relay(ard, LED_GREEN, 'green')
blue = Elements.Relay(ard, LED_BLUE, 'blue')
purple = Elements.Relay(ard, LED_PURPLE, 'purple')
white1 = Elements.Relay(ard, LED_WHITE1, 'white1')
white2 = Elements.Relay(ard, LED_WHITE2, 'white2')

level = Elements.DigitalSensor(ard, 12, 'level_sensor')


if __name__ == '__main__':
    pass