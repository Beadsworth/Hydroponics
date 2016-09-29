#!/usr/bin/env python
# imports
import unittest
import time

from HydroLoads import light_high_str, sublight_off_str, sublight_on_str, light_low_str, light_off_str, pump_off_str, pump_on_str, \
    valve_closed_str, valve_open_str

from LoadList import pump1, inlet_valve, zone1_valve, zone2_valve, zone3_valve, zone4_valve, zone5_valve, \
    zone6_valve, outlet_valve, sublight_1A, sublight_1B, sublight_2A, sublight_2B, light1, light2, \
    zone1, zone2, zone3,zone4, zone5, zone6, close_all_valves, open_all_valves


def flicker_all():
    pump1.set_mode(pump_on_str)
    open_all_valves()
    light1.set_mode(light_high_str)

    pump1.set_mode(pump_off_str)
    close_all_valves()
    light1.set_mode(light_off_str)


# @unittest.skip("Skipping TestPump Class...")
class TestSanity(unittest.TestCase):

    def test_sanity(self):

        time.sleep(3)


class TestHydroLoad:

    def __init__(self):

        self.load = None

    def test_load(self):

        all_modes = {
            pump_off_str: 0,
            pump_on_str: 0,
            valve_closed_str: 0,
            valve_open_str: 0,
            sublight_off_str: 0,
            sublight_on_str: 0,
            '0': 0,
            '1': 1,
            '229': 229,
            'ON': 1,
            'OFF': 0,
            'hello': 0
        }

        good_modes = self.load.mode_dict
        bad_modes = all_modes.copy()

        for mode in good_modes:
            del bad_modes[mode]

        status0 = self.load.get_mode()
        status0 = self.load.get_mode()
        self.assertTrue(self.load.mode_dict[status0] is 0 or self.load.mode_dict[status0] is 1)

        for mode in bad_modes:
            with self.assertRaises(ValueError):
                self.load.set_mode(mode)
                self.load.set_mode(mode)

        for mode in good_modes:
            status1 = self.load.set_mode(mode)
            status2 = self.load.set_mode(mode)
            self.assertIsNone(status1)
            self.assertIsNone(status2)
            status3 = self.load.get_mode()
            self.assertEqual(self.load.mode_dict[status3], self.load.mode_dict[mode])


class TestHydroZone:

    def __init__(self):

        self.zone = None

    def test_zone(self):

        pause_sec = 0

        # flicker_all()
        time.sleep(pause_sec)
        # fill check
        self.zone.fill()
        time.sleep(pause_sec)
        self.assertTrue(self.zone.control_valve.get_mode() == valve_open_str)
        self.assertTrue(self.zone.inlet_valve.get_mode() == valve_open_str)
        self.assertTrue(self.zone.outlet_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.pump.get_mode() == pump_on_str)
        # maintain check
        self.zone.maintain()
        time.sleep(pause_sec)
        self.assertTrue(self.zone.control_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.inlet_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.outlet_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.pump.get_mode() == pump_off_str)
        # drain check
        self.zone.drain()
        time.sleep(pause_sec)
        self.assertTrue(self.zone.control_valve.get_mode() == valve_open_str)
        self.assertTrue(self.zone.inlet_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.outlet_valve.get_mode() == valve_open_str)
        self.assertTrue(self.zone.pump.get_mode() == pump_off_str)
        # maintain check
        self.zone.maintain()
        time.sleep(pause_sec)
        self.assertTrue(self.zone.control_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.inlet_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.outlet_valve.get_mode() == valve_closed_str)
        self.assertTrue(self.zone.pump.get_mode() == pump_off_str)


# @unittest.skip("Skipping TestPump Class...")
class TestPump(unittest.TestCase, TestHydroLoad):

    load = pump1


# @unittest.skip("Skipping TestInletValve Class...")
class TestInletValve(unittest.TestCase, TestHydroLoad):

    load = inlet_valve


# @unittest.skip("Skipping TestZone1Valve Class...")
class TestZone1Valve(unittest.TestCase, TestHydroLoad):

    load = zone1_valve


# @unittest.skip("Skipping TestZone2Valve  Class...")
class TestZone2Valve(unittest.TestCase, TestHydroLoad):
    load = zone2_valve


# @unittest.skip("Skipping TestZone3Valve  Class...")
class TestZone3Valve(unittest.TestCase, TestHydroLoad):
    load = zone3_valve


# @unittest.skip("Skipping TestZone4Valve  Class...")
class TestZone4Valve(unittest.TestCase, TestHydroLoad):
    load = zone4_valve


# @unittest.skip("Skipping TestZone5Valve  Class...")
class TestZone5Valve(unittest.TestCase, TestHydroLoad):
    load = zone5_valve


# @unittest.skip("Skipping TestZone6Valve  Class...")
class TestZone6Valve(unittest.TestCase, TestHydroLoad):
    load = zone6_valve


# @unittest.skip("Skipping TestOutletValve  Class...")
class TestOutletValve(unittest.TestCase, TestHydroLoad):

    load = outlet_valve


# @unittest.skip("Skipping TestSublight1A  Class...")
class TestSublight1A(unittest.TestCase, TestHydroLoad):

    load = sublight_1A


# @unittest.skip("Skipping TestSublight1B  Class...")
class TestSublight1B(unittest.TestCase, TestHydroLoad):

    load = sublight_1B


# @unittest.skip("Skipping TestZone1 Class...")
class TestZone1(unittest.TestCase, TestHydroZone):

    zone = zone1


# @unittest.skip("Skipping TestZone2 Class...")
class TestZone2(unittest.TestCase, TestHydroZone):

    zone = zone2


# @unittest.skip("Skipping TestZone3 Class...")
class TestZone3(unittest.TestCase, TestHydroZone):

    zone = zone3


# @unittest.skip("Skipping TestZone4 Class...")
class TestZone4(unittest.TestCase, TestHydroZone):

    zone = zone4


# @unittest.skip("Skipping TestZone5 Class...")
class TestZone5(unittest.TestCase, TestHydroZone):

    zone = zone5


# @unittest.skip("Skipping TestZone6 Class...")
class TestZone6(unittest.TestCase, TestHydroZone):

    zone = zone6


# @unittest.skip("Skipping TestZone6 Class...")
class TestLight(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        time.sleep(5)

    def setUp(self):

        flicker_all()

    def test_light1(self):  # high -> low -> off, twice

        pause_time = 0

        for i in range(2):

            light1.set_mode(light_high_str)
            time.sleep(pause_time)
            self.assertTrue(light1.get_mode() == light_high_str)
            self.assertTrue(light1.sublight_a.get_mode() == sublight_on_str)
            self.assertTrue(light1.sublight_b.get_mode() == sublight_on_str)

            light1.set_mode(light_low_str)
            time.sleep(pause_time)
            self.assertTrue(light1.get_mode() == light_low_str)

            light1.set_mode(light_off_str)
            time.sleep(pause_time)
            self.assertTrue(light1.get_mode() == light_off_str)
            self.assertTrue(light1.sublight_a.get_mode() == sublight_off_str)
            self.assertTrue(light1.sublight_b.get_mode() == sublight_off_str)

    @unittest.skip("Skipping test_light2: light2 not yet implemented")
    def test_light2(self):  # high -> low -> off, twice

        pause_time = 0

        for i in range(2):
            light2.set_mode(light_high_str)
            time.sleep(pause_time)
            self.assertTrue(light2.get_mode() == light_high_str)
            self.assertTrue(light2.sublight_a.get_mode() == sublight_on_str)
            self.assertTrue(light2.sublight_b.get_mode() == sublight_on_str)

            light2.set_mode(light_low_str)
            time.sleep(pause_time)
            self.assertTrue(light2.get_mode() == light_low_str)

            light2.set_mode(light_off_str)
            time.sleep(pause_time)
            self.assertTrue(light2.get_mode() == light_off_str)
            self.assertTrue(light2.sublight_a.get_mode() == sublight_off_str)
            self.assertTrue(light2.sublight_b.get_mode() == sublight_off_str)

    def test_low_blink(self):

        pause_time = 0
        previous_switch = None

        for i in range(10):

            light1.set_mode(light_low_str)
            time.sleep(pause_time)
            self.assertTrue(light1.get_mode() == light_low_str)
            self.assertIsNot(light1.sublight_switch, previous_switch)


# @unittest.skip("Skipping TestSimplifiedMethods Class...")
class TestSimplifiedMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        time.sleep(3)

    def setUp(self):

        pass

    def test_sublight_simplified_methods(self):

        sublight_1A.on()
        sublight_1A.on()
        sublight_1A.off()
        sublight_1A.off()
        sublight_1A.on()
        sublight_1A.off()
        sublight_1A.on()
        sublight_1A.off()

        sublight_1B.on()
        sublight_1B.on()
        sublight_1B.off()
        sublight_1B.off()
        sublight_1B.on()
        sublight_1B.off()
        sublight_1B.on()
        sublight_1B.off()

    def test_pump_simplified_methods(self):

        pump1.on()
        pump1.on()
        pump1.off()
        pump1.off()
        pump1.on()
        pump1.off()

    def test_valve_simplified_methods(self):

        valve_list = [
            inlet_valve,
            zone1_valve,
            zone2_valve,
            zone3_valve,
            zone4_valve,
            zone5_valve,
            zone6_valve,
            outlet_valve
            ]
        for valve in valve_list:

            valve.open()
            valve.open()
            valve.close()
            valve.close()
            valve.open()
            valve.close()

    def test_light_simplified_methods(self):

        light1.off()
        light1.low()
        light1.high()
        light1.low()
        light1.off()
        light1.high()
        light1.off()
        light1.low()
        light1.low()
        light1.off()

    def test_typical_use(self):

        flood_drain_time = 2

        zone_list = [
            zone1,
            zone2,
            zone3,
            zone4,
            zone5,
            zone6
        ]

        light1.high()

        for zone in zone_list:

            zone.fill()
            zone.maintain()
            zone.drain()
            zone.maintain()

        light1.low()

        for zone in zone_list:
            zone.fill()
            time.sleep(flood_drain_time)
            zone.maintain()
            zone.drain()
            time.sleep(flood_drain_time)
            zone.maintain()

        light1.off()


if __name__ == '__main__':
    unittest.main()
