import Groups
import config.test_HydroComponentList as test_HydroComponents

zone1 = Groups.FloodZone.FloodZone(test_HydroComponents.control1,
                                   test_HydroComponents.inlet1,
                                   test_HydroComponents.outlet1,
                                   test_HydroComponents.pump1,
                                   test_HydroComponents.level1,
                                   'zone1')

zone2 = Groups.FloodZone.FloodZone(test_HydroComponents.control2,
                                   test_HydroComponents.inlet1,
                                   test_HydroComponents.outlet1,
                                   test_HydroComponents.pump1,
                                   test_HydroComponents.level1,
                                   'zone2')

zone3 = Groups.FloodZone.FloodZone(test_HydroComponents.control3,
                                   test_HydroComponents.inlet1,
                                   test_HydroComponents.outlet1,
                                   test_HydroComponents.pump1,
                                   test_HydroComponents.level1,
                                   'zone3')

light1 = Groups.SuperLight.SuperLight(test_HydroComponents.white1, test_HydroComponents.white2, 'light1')

uno = Groups.Arduino.Arduino([zone1, zone2, zone3, light1], 'test_uno')

if __name__ == '__main__':
    pass
