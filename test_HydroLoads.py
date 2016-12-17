#!/usr/bin/env python
# imports
import unittest
import time

from pyfirmata import PinAlreadyTakenError
from HydroLoads import light_high_str, light_low_str, light_off_str, relay_on_str, relay_off_str
import HydroLoads
import quick

mega = quick.get_arduino()


# @unittest.skip("Skipping TestPump Class...")
class TestSanity(unittest.TestCase):

    def test_sanity(self):
        pass


# @unittest.skip("Skipping TestLight Class...")
class TestController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        mega.connect()

    def tearDown(self):
        quick.buzz()
        mega.disconnect()

    # @unittest.skip("Skipping test")
    def test_reconnect(self):
        mega.reconnect()

    def test_adding_when_connected(self):

        with self.assertRaises(RuntimeError):
            temp = HydroLoads.Component(mega, 13, 'test1')

        with self.assertRaises(RuntimeError):
            temp = HydroLoads.Valve(mega, 13, 'test3')

        with self.assertRaises(RuntimeError):
            temp = HydroLoads.Relay(mega, 13, 'test4')

        with self.assertRaises(RuntimeError):
            temp = HydroLoads.RelayBoard(mega, 13, 'test5')

        with self.assertRaises(RuntimeError):
            temp = HydroLoads.Light(mega, 12, 13, 'test5')


# @unittest.skip("Skipping TestLight Class...")
class TestLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        mega.connect()

    def tearDown(self):
        quick.buzz()
        mega.disconnect()

    # @unittest.skip("Skipping test")
    def test_add_load(self):
        mega.disconnect()

        with self.assertRaises(PinAlreadyTakenError):
            temp1 = HydroLoads.Component(mega, 30, 'hi')
            temp2 = HydroLoads.Component(mega, 30, 'bye')
            mega.connect()

        mega.components.remove(temp1)
        mega.components.remove(temp2)
        temp1 = None
        temp2 = None
        mega.connect()

    def test_relay(self):

        mega.open_all_valves()
        time.sleep(0.5)
        mega.disable_all_relays()
        time.sleep(0.5)
        mega.enable_all_relays()
        time.sleep(0.5)
        mega.close_all_valves()

    def test_valve(self):
        quick.inlet_valve.open()
        quick.outlet_valve.open()
        quick.light1.high()
        quick.inlet_valve.close()
        quick.outlet_valve.close()
        mega.close_all_valves()

    def test_emer_off(self):
        mega.open_all_valves()
        quick.light1.high()
        quick.pump1.high()
        time.sleep(2)
        mega.emergency_off()


# @unittest.skip("Skipping TestLight Class...")
class TestLight(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        mega.connect()

    def tearDown(self):
        quick.buzz()
        mega.disconnect()

    def test_light1(self):  # high -> low -> low, twice

        pause_time = 0.5

        for i in range(2):

            quick.light1.set_state(light_high_str)
            time.sleep(pause_time)
            self.assertTrue(quick.light1.get_state() == light_high_str)
            self.assertTrue(quick.light1.sublight_a.get_state() == relay_on_str)
            self.assertTrue(quick.light1.sublight_b.get_state() == relay_on_str)

            quick.light1.set_state(light_low_str)
            time.sleep(pause_time)
            self.assertTrue(quick.light1.get_state() == light_low_str)

            quick.light1.set_state(light_off_str)
            time.sleep(pause_time)
            self.assertTrue(quick.light1.get_state() == light_off_str)
            self.assertTrue(quick.light1.sublight_a.get_state() == relay_off_str)
            self.assertTrue(quick.light1.sublight_b.get_state() == relay_off_str)

    def test_low_blink(self):

        pause_time = 0.2

        for i in range(10):

            quick.light1.set_state(light_low_str)
            time.sleep(pause_time)
            self.assertTrue(quick.light1.get_state() == light_low_str)


if __name__ == '__main__':
    unittest.main()
