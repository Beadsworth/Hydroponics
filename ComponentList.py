import ElementList
import time

from ElementList import ard

from Components import Component, Pump, Valve, WaterLevelSensor

red1 = Component(ElementList.red, 'red1')
green1 = Valve(ElementList.green, 'green1')
blue1 = Pump(ElementList.blue, 'blue1')
level1 = WaterLevelSensor(ElementList.level, 'level1')

if __name__ == '__main__':

    try:
        ElementList.ard.connect()

        print('red1 in state: ' + str(red1.state))
        print('blue1 in state: ' + str(blue1.state))
        red1.state = 'HIGH'
        blue1.state = 'OPEN'
        print('red1 in state: ' + str(red1.state))
        print('blue1 in state: ' + str(blue1.state))
        print('red1 name: ' + str(red1.name))
        print('blue1 name: ' + str(blue1.name))
        blue1.state = 'CLOSED'
        red1.state = 'LOW'
        time.sleep(5)
    finally:
        ElementList.ard.disconnect()
        print("Done!")
