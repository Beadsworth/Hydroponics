import HydroGroups
from HydroComponentList import *

zone1 = HydroGroups.FloodZone(control1, inlet1, outlet1, pump1, level1, 'zone1')
zone2 = HydroGroups.FloodZone(control2, inlet1, outlet1, pump1, level1, 'zone2')
zone3 = HydroGroups.FloodZone(control3, inlet1, outlet1, pump1, level1, 'zone3')
light1 = HydroGroups.SuperLight(white1, white2, 'light1')

ard_test = HydroGroups.Arduino([zone1, zone2, zone3], 'test')

if __name__ == '__main__':
    pass
