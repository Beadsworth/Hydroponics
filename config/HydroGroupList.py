from Groups import FloodZone, Arduino
import config.HydroComponentList as HydroComponents

zone1 = FloodZone.FloodZone(HydroComponents.control1, HydroComponents.inlet_valve, HydroComponents.outlet_valve,
                                   HydroComponents.pump, HydroComponents.level1, 'zone1')

mega_controller = Arduino.Arduino([zone1, ], 'arduino_mega_controller')

if __name__ == '__main__':
    pass
