#!/usr/bin/env python
# imports
from HydroLoads import Zone, Pump, Light, Valve, Sublight, Controller, Relay

# general definitions
FLOOD_TIME = 0
DRAIN_TIME = 0

# controller info
addr = '/dev/ttyACM0'
uno = Controller(addr)

# define pin locations
RELAY_BOARD_PIN = 2
PUMP_PIN = 9
LIGHT1A_PIN = 10
LIGHT1B_PIN = 11
INLET_VALVE_PIN = 8
ZONE1_VALVE_PIN = 7
ZONE2_VALVE_PIN = 6
ZONE3_VALVE_PIN = 5
OUTLET_VALVE_PIN = 4

# enable relay boards
relay1 = Relay(uno, RELAY_BOARD_PIN)
#  initialize Loads
pump1 = Pump(uno, PUMP_PIN)
# lights
sublight_1A = Sublight(uno, LIGHT1A_PIN)
sublight_1B = Sublight(uno, LIGHT1B_PIN)


light1 = Light(sublight_1A, sublight_1B)
# valves
inlet_valve = Valve(uno, INLET_VALVE_PIN)
zone1_valve = Valve(uno, ZONE1_VALVE_PIN)
zone2_valve = Valve(uno, ZONE2_VALVE_PIN)
zone3_valve = Valve(uno, ZONE3_VALVE_PIN)
outlet_valve = Valve(uno, OUTLET_VALVE_PIN)
# initialize Zones
zone1 = Zone("ZONE1", zone1_valve, inlet_valve, outlet_valve, pump1)
zone2 = Zone("ZONE2", zone2_valve, inlet_valve, outlet_valve, pump1)
zone3 = Zone("ZONE3", zone3_valve, inlet_valve, outlet_valve, pump1)

controllers = uno,
zones = zone1, zone2, zone3,


if __name__ == '__main__':
    pass
