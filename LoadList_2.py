#!/usr/bin/env python
# imports
from HydroLoads import Zone, Light, Valve, Controller, RelayBoard, Relay

# general definitions
FLOOD_TIME = 0
DRAIN_TIME = 0

# controller info
addr = '/dev/ttyACM0'
ard = Controller(addr)

# define pin locations
RELAY_BOARD_PIN = 36
PUMP_PIN = 42
LIGHT1A_PIN = 40
LIGHT1B_PIN = 38
INLET_VALVE_PIN = 52
ZONE1_VALVE_PIN = 50
ZONE2_VALVE_PIN = 48
ZONE3_VALVE_PIN = 46
OUTLET_VALVE_PIN = 44

# enable relay boards
relayboard1 = RelayBoard(ard, RELAY_BOARD_PIN, 'relayboard1')

#  initialize Loads
pump1 = Relay(ard, PUMP_PIN, 'pump1')
# lights
light1 = Light(ard, LIGHT1A_PIN, LIGHT1B_PIN, 'light1')
# valves
inlet_valve = Valve(ard, INLET_VALVE_PIN, 'inlet_valve')
zone1_valve = Valve(ard, ZONE1_VALVE_PIN, 'zone1_valve')
zone2_valve = Valve(ard, ZONE2_VALVE_PIN, 'zone2_valve')
zone3_valve = Valve(ard, ZONE3_VALVE_PIN, 'zone3_valve')
outlet_valve = Valve(ard, OUTLET_VALVE_PIN, 'outlet_valve')
# initialize Zones
zone1 = Zone("ZONE1", zone1_valve, inlet_valve, outlet_valve, pump1)
zone2 = Zone("ZONE2", zone2_valve, inlet_valve, outlet_valve, pump1)
zone3 = Zone("ZONE3", zone3_valve, inlet_valve, outlet_valve, pump1)

controllers = ard,
zones = zone1, zone2, zone3,


if __name__ == '__main__':
    pass
