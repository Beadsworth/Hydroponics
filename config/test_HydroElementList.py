import ArduinoElements


# controller info
addr = '/dev/ttyACM0'
test_uno = ArduinoElements.Controller(addr)

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
red = ArduinoElements.Relay(test_uno, LED_RED, 'red')
orange = ArduinoElements.Relay(test_uno, LED_ORANGE, 'orange')
yellow = ArduinoElements.Relay(test_uno, LED_YELLOW, 'yellow')
green = ArduinoElements.Relay(test_uno, LED_GREEN, 'green')
blue = ArduinoElements.Relay(test_uno, LED_BLUE, 'blue')
purple = ArduinoElements.Relay(test_uno, LED_PURPLE, 'purple')
white1 = ArduinoElements.Relay(test_uno, LED_WHITE1, 'white1')
white2 = ArduinoElements.Relay(test_uno, LED_WHITE2, 'white2')

level = ArduinoElements.DigitalSensor(test_uno, 12, 'level_sensor')


if __name__ == '__main__':
    pass
