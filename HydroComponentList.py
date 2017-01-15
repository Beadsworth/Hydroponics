import HydroComponents

from HydroElementList import *

outlet1 = HydroComponents.Valve(red, 'red1')
control3 = HydroComponents.Valve(orange, 'orange1')
control2 = HydroComponents.Valve(yellow, 'yellow1')
control1 = HydroComponents.Valve(green, 'green1')
inlet1 = HydroComponents.Valve(blue, 'blue1')
pump1 = HydroComponents.Pump(purple, 'purple1')
white1 = HydroComponents.Light(white1, 'white1')
white2 = HydroComponents.Light(white2, 'white2')
level1 = HydroComponents.WaterLevelSensor(level, 'level1')


if __name__ == '__main__':
    pass
