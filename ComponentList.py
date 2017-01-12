import ElementList
import time

from Components import Component, Pump, Valve, WaterLevelSensor, Light
from ElementList import ard

outlet1 = Valve(ElementList.red, 'red1')
control3 = Valve(ElementList.orange, 'orange1')
control2 = Valve(ElementList.yellow, 'yellow1')
control1 = Valve(ElementList.green, 'green1')
inlet1 = Valve(ElementList.blue, 'blue1')
pump1 = Pump(ElementList.purple, 'purple1')
white1 = Light(ElementList.white1, 'white1')
white2 = Light(ElementList.white2, 'white2')
level1 = WaterLevelSensor(ElementList.level, 'level1')

if __name__ == '__main__':

    try:
        ElementList.ard.connect()
        time.sleep(5)
    finally:
        ElementList.ard.disconnect()
        print("Done!")
