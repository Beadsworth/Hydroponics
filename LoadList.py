#!/usr/bin/env python
# imports
from HydroLoads import Zone, Pump, Light, Valve, Sublight

# general definitions
FLOOD_TIME = 0
DRAIN_TIME = 0

# define pin locations
PUMP_PIN = 2
LIGHT1A_PIN = 11
LIGHT1B_PIN = 12
LIGHT2A_PIN = 13
LIGHT2B_PIN = 13
INLET_VALVE_PIN = 3
ZONE1_VALVE_PIN = 4
ZONE2_VALVE_PIN = 5
ZONE3_VALVE_PIN = 6
ZONE4_VALVE_PIN = 7
ZONE5_VALVE_PIN = 8
ZONE6_VALVE_PIN = 9
OUTLET_VALVE_PIN = 10

# initialize Loads
pump1 = Pump(PUMP_PIN)
# lights
sublight_1A = Sublight(LIGHT1A_PIN)
sublight_1B = Sublight(LIGHT1B_PIN)
sublight_2A = Sublight(LIGHT2A_PIN)
sublight_2B = Sublight(LIGHT2B_PIN)

light1 = Light(sublight_1A, sublight_1B)
light2 = Light(sublight_2A, sublight_2B)
# valves
inlet_valve = Valve(INLET_VALVE_PIN)
zone1_valve = Valve(ZONE1_VALVE_PIN)
zone2_valve = Valve(ZONE2_VALVE_PIN)
zone3_valve = Valve(ZONE3_VALVE_PIN)
zone4_valve = Valve(ZONE4_VALVE_PIN)
zone5_valve = Valve(ZONE5_VALVE_PIN)
zone6_valve = Valve(ZONE6_VALVE_PIN)
outlet_valve = Valve(OUTLET_VALVE_PIN)
# initialize Zones
zone1 = Zone("ZONE1", zone1_valve, inlet_valve, outlet_valve, pump1)
zone2 = Zone("ZONE2", zone2_valve, inlet_valve, outlet_valve, pump1)
zone3 = Zone("ZONE3", zone3_valve, inlet_valve, outlet_valve, pump1)
zone4 = Zone("ZONE4", zone4_valve, inlet_valve, outlet_valve, pump1)
zone5 = Zone("ZONE5", zone5_valve, inlet_valve, outlet_valve, pump1)
zone6 = Zone("ZONE6", zone6_valve, inlet_valve, outlet_valve, pump1)


pump_tuple = (
    pump1,
)

light_tuple = (
    light1,
    # light2,
)

valve_tuple = (
    inlet_valve,
    zone1_valve,
    zone2_valve,
    zone3_valve,
    zone4_valve,
    zone5_valve,
    zone6_valve,
    outlet_valve,
)

load_tuple = pump_tuple + light_tuple + valve_tuple


zone_tuple = (
    zone1,
    zone2,
    zone3,
    zone4,
    zone5,
    zone6,
)


def close_all_valves():

    for valve in valve_tuple:
        valve.close()


def open_all_valves():

    for valve in valve_tuple:
        valve.open()


def shutdown_all():

    close_all_valves()

    for pump in pump_tuple:
        pump.off()

    for light in light_tuple:
        light.off()


if __name__ == '__main__':

    pass
