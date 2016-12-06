#!/usr/bin/env python
# imports
from HydroLoads import Zone, Pump, Light, Valve, Sublight, Controller, RelayBoard

# general definitions
FLOOD_TIME = 0
DRAIN_TIME = 0

# controller info
addr = '/dev/ttyACM0'
mega = Controller(addr)

# define pin locations
RELAY_BOARD_PIN = 36
PUMP_PIN = 48
LIGHT1A_PIN = 52
LIGHT1B_PIN = 50
INLET_VALVE_PIN = 46
ZONE1_VALVE_PIN = 44
ZONE2_VALVE_PIN = 42
ZONE3_VALVE_PIN = 40
OUTLET_VALVE_PIN = 38

# enable relay boards
relay1 = RelayBoard(mega, RELAY_BOARD_PIN)
#  initialize Loads
pump1 = Pump(mega, PUMP_PIN)
# lights
sublight_1A = Sublight(mega, LIGHT1A_PIN)
sublight_1B = Sublight(mega, LIGHT1B_PIN)


light1 = Light(sublight_1A, sublight_1B)
# valves
inlet_valve = Valve(mega, INLET_VALVE_PIN)
zone1_valve = Valve(mega, ZONE1_VALVE_PIN)
zone2_valve = Valve(mega, ZONE2_VALVE_PIN)
zone3_valve = Valve(mega, ZONE3_VALVE_PIN)
outlet_valve = Valve(mega, OUTLET_VALVE_PIN)
# initialize Zones
zone1 = Zone("ZONE1", zone1_valve, inlet_valve, outlet_valve, pump1)
zone2 = Zone("ZONE2", zone2_valve, inlet_valve, outlet_valve, pump1)
zone3 = Zone("ZONE3", zone3_valve, inlet_valve, outlet_valve, pump1)

controllers = mega,
zones = zone1, zone2, zone3,


if __name__ == '__main__':
    pass
