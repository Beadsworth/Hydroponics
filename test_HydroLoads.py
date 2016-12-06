#!/usr/bin/env python
# imports
import unittest
import time

from pyfirmata import PinAlreadyTakenError
from HydroLoads import *

addr = '/dev/ttyACM0'
mega = Controller(addr)
led_red = Valve(mega, 4)
led_orange = Valve(mega, 5)
led_yellow = Valve(mega, 6)
led_green = Valve(mega, 7)
led_blue = Valve(mega, 8)
led_purple = Valve(mega, 9)
led_white1 = Sublight(mega, 10)
led_white2 = Sublight(mega, 11)

relay1 = RelayBoard(mega, 2)
buzzer = Load(mega, 3)

sublight_1A = led_white1
sublight_1B = led_white2

light1 = Light(sublight_1A, sublight_1B)


def buzz(Hz, sec):

    start = time.time()
    now = time.time()
    try:
        while now - start < sec:
            buzzer.on()
            time.sleep(1 / Hz)
            buzzer.off()
            time.sleep(1 / Hz)
            now = time.time()
    finally:
        buzzer.off()


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
        mega.clear_pins()

    def tearDown(self):
        buzz(100, 0.5)
        mega.disconnect()

    # @unittest.skip("Skipping test")
    def test_reconnect(self):
        mega.reconnect()

    def test_all_pins_low(self):
        mega.clear_pins()

    def test_adding_when_connected(self):
        with self.assertRaises(RuntimeError):
            temp = Component(mega, 13)

        with self.assertRaises(RuntimeError):
            temp = Load(mega, 13)

        with self.assertRaises(RuntimeError):
            temp = Valve(mega, 13)

        with self.assertRaises(RuntimeError):
            temp = Pump(mega, 13)

        with self.assertRaises(RuntimeError):
            temp = Sublight(mega, 13)


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
        mega.clear_pins()

    def tearDown(self):
        buzz(100, 0.5)
        mega.disconnect()

    # @unittest.skip("Skipping test")
    def test_add_load(self):
        mega.disconnect()

        with self.assertRaises(PinAlreadyTakenError):
            temp1 = Component(mega, 13)
            temp2 = Component(mega, 13)
            mega.connect()

        mega.components.remove(temp1)
        mega.components.remove(temp2)
        temp1 = None
        temp2 = None
        mega.connect()

    def test_relay(self):

        time.sleep(0.5)
        relay1.disable()
        time.sleep(0.5)
        mega.enable_all_relays()
        time.sleep(0.5)

    def test_valve(self):
        led_red.open()
        led_purple.open()
        led_white1.on()
        led_purple.open()
        # purple should close as white1 goes on
        led_purple.close()
        mega.close_all_valves()
        led_blue.open()

    def test_emer_off(self):
        led_blue.open()
        led_yellow.open()
        led_red.open()
        light1.high()
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
        mega.clear_pins()

    def tearDown(self):
        buzz(100, 0.5)
        mega.disconnect()

    def test_light1(self):  # on -> off -> off, twice

        pause_time = 0.5

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

    def test_low_blink(self):

        pause_time = 0.2
        previous_switch = None

        for i in range(10):

            light1.set_mode(light_low_str)
            time.sleep(pause_time)
            self.assertTrue(light1.get_mode() == light_low_str)
            self.assertIsNot(light1.sublight_switch, previous_switch)

    def test_sublight_validity(self):

        mega.disconnect()

        good_light1 = led_white1
        good_light2 = led_white2
        bad_light1 = 'hello'
        bad_light2 = Valve(mega, 13)

        with self.assertRaises(TypeError):
            Light(good_light1, bad_light1)

        with self.assertRaises(TypeError):
            Light(bad_light2, good_light2)

        with self.assertRaises(TypeError):
            Light(bad_light1, bad_light2)

        with self.assertRaises(RuntimeError):
            Light(good_light1, good_light1)

        # next one should pass
        lightc = Light(good_light1, good_light2)

        mega.connect()

        lightc.high()


if __name__ == '__main__':
    unittest.main()
