#!/usr/bin/env python
# imports
from HydroIO import VALVE_CLOSED, VALVE_OPEN
import HydroIO
import time

# general definitions
from schedule import Zone, Pump, Light, Valve

FLOOD_TIME = 0
DRAIN_TIME = 0

# define pin locations
PUMP_PIN = 2
LIGHT1A_PIN = 3
LIGHT1B_PIN = 4
LIGHT2A_PIN = 5
LIGHT2B_PIN = 6
INLET_VALVE_PIN = 7
ZONE1_VALVE_PIN = 8
ZONE2_VALVE_PIN = 11
ZONE3_VALVE_PIN = 11
ZONE4_VALVE_PIN = 11
ZONE5_VALVE_PIN = 11
ZONE6_VALVE_PIN = 11
OUTLET_VALVE_PIN = 9

# initialize appliances
pump = Pump(PUMP_PIN)
light1 = Light(LIGHT1A_PIN, LIGHT1B_PIN)
light2 = Light(LIGHT2A_PIN, LIGHT2B_PIN)
inlet_valve = Valve(INLET_VALVE_PIN)
zone1_valve = Valve(ZONE1_VALVE_PIN)
zone2_valve = Valve(ZONE2_VALVE_PIN)
zone3_valve = Valve(ZONE3_VALVE_PIN)
zone4_valve = Valve(ZONE4_VALVE_PIN)
zone5_valve = Valve(ZONE5_VALVE_PIN)
zone6_valve = Valve(ZONE6_VALVE_PIN)
outlet_valve = Valve(OUTLET_VALVE_PIN)
# initialize zones
zone1 = Zone("ZONE1", zone1_valve, inlet_valve, outlet_valve, pump)
zone2 = Zone("ZONE2", zone2_valve, inlet_valve, outlet_valve, pump)
zone3 = Zone("ZONE3", zone3_valve, inlet_valve, outlet_valve, pump)
zone4 = Zone("ZONE4", zone4_valve, inlet_valve, outlet_valve, pump)
zone5 = Zone("ZONE5", zone5_valve, inlet_valve, outlet_valve, pump)
zone6 = Zone("ZONE6", zone6_valve, inlet_valve, outlet_valve, pump)


def close_all_valves():
    inlet_valve.set_mode(VALVE_CLOSED)
    zone1_valve.set_mode(VALVE_CLOSED)
    zone2_valve.set_mode(VALVE_CLOSED)
    zone3_valve.set_mode(VALVE_CLOSED)
    zone4_valve.set_mode(VALVE_CLOSED)
    zone5_valve.set_mode(VALVE_CLOSED)
    zone6_valve.set_mode(VALVE_CLOSED)
    outlet_valve.set_mode(VALVE_CLOSED)


def open_all_valves():
    inlet_valve.set_mode(VALVE_OPEN)
    zone1_valve.set_mode(VALVE_OPEN)
    zone2_valve.set_mode(VALVE_OPEN)
    zone3_valve.set_mode(VALVE_OPEN)
    zone4_valve.set_mode(VALVE_OPEN)
    zone5_valve.set_mode(VALVE_OPEN)
    zone6_valve.set_mode(VALVE_OPEN)
    outlet_valve.set_mode(VALVE_OPEN)


if __name__ == '__main__':

    time.sleep(5)
    zone1.flood()
    zone1.maintain()
    zone1.drain()
