#!/usr/bin/env python
# imports
import unittest

import time

from HydroIO import getPin
from schedule import Light, Pump, Valve, Zone, LightMode
from schedule_run import PUMP_PIN, LIGHT1A_PIN, LIGHT2A_PIN, LIGHT1B_PIN, LIGHT2B_PIN, INLET_VALVE_PIN, ZONE1_VALVE_PIN, \
    ZONE2_VALVE_PIN, ZONE3_VALVE_PIN, ZONE4_VALVE_PIN, ZONE5_VALVE_PIN, ZONE6_VALVE_PIN, OUTLET_VALVE_PIN


class ScheduleTest(unittest.TestCase):
    def test_sanity(self):
        pass

    def setUp(self):
        # initialize appliances
        pump = Pump(PUMP_PIN)
        # light1 = Light(LIGHT1A_PIN, LIGHT1B_PIN)
        # light2 = Light(LIGHT2A_PIN, LIGHT2B_PIN)
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

        time.sleep(3)


    def test_light(self):
        light1 = Light(LIGHT1A_PIN, LIGHT1B_PIN)
        light1.set_mode(LightMode.HIGH)
        self.assertTrue("Light Mode is not high!!!", light1.is_high())
        # self.assertEqual(LightMode.HIGH, getPin(LIGHT1B_PIN))