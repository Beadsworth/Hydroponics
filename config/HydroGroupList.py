from Groups import Arduino, FloodZone, SuperLight
from config.HydroComponentList import *

zone1 = FloodZone.FloodZone(control1, inlet1, outlet1, pump1, level1, 'zone1')
zone2 = FloodZone.FloodZone(control2, inlet1, outlet1, pump1, level1, 'zone2')
zone3 = FloodZone.FloodZone(control3, inlet1, outlet1, pump1, level1, 'zone3')
light1 = SuperLight.SuperLight(white1, white2, 'light1')

ard1 = Arduino.Arduino([zone1, zone2, zone3, light1], 'ard1')

if __name__ == '__main__':
    pass
