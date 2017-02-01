from Components import Pump, Valve, Light, WaterLevelSensor, Clock, TwitterAccount

from config.HydroElementList import *

outlet1 = Valve.Valve(red, 'red1')
control3 = Valve.Valve(orange, 'orange1')
control2 = Valve.Valve(yellow, 'yellow1')
control1 = Valve.Valve(green, 'green1')
inlet1 = Valve.Valve(blue, 'blue1')
pump1 = Pump.Pump(purple, 'purple1')
white1 = Light.Light(white1, 'white1')
white2 = Light.Light(white2, 'white2')
level1 = WaterLevelSensor.WaterLevelSensor(level, 'level1')

clock1 = Clock.Clock("clock1")
twitter_account = TwitterAccount.TwitterAccount("twitter")


if __name__ == '__main__':
    pass
