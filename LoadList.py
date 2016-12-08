#!/usr/bin/env python
# imports
from HydroLoads import Zone, Light, Valve, Controller, RelayBoard, Relay

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
relayboard1 = RelayBoard(mega, RELAY_BOARD_PIN, 'relayboard1')
relay1 = Relay(mega, 26, 'relay1')
#  initialize Loads
pump1 = Relay(mega, PUMP_PIN, 'pump1')
# lights
light1 = Light(mega, LIGHT1A_PIN, LIGHT1B_PIN, 'light1')
# valves
inlet_valve = Valve(mega, INLET_VALVE_PIN, 'inlet_valve')
zone1_valve = Valve(mega, ZONE1_VALVE_PIN, 'zone1_valve')
zone2_valve = Valve(mega, ZONE2_VALVE_PIN, 'zone2_valve')
zone3_valve = Valve(mega, ZONE3_VALVE_PIN, 'zone3_valve')
outlet_valve = Valve(mega, OUTLET_VALVE_PIN, 'outlet_valve')
# initialize Zones
zone1 = Zone("ZONE1", zone1_valve, inlet_valve, outlet_valve, pump1)
zone2 = Zone("ZONE2", zone2_valve, inlet_valve, outlet_valve, pump1)
zone3 = Zone("ZONE3", zone3_valve, inlet_valve, outlet_valve, pump1)

controllers = mega,
zones = zone1, zone2, zone3,


if __name__ == '__main__':
    pass
