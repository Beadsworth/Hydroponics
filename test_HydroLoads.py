#!/usr/bin/env python
# imports
import unittest
import time

from HydroLoads import *

addr = '/dev/ttyACM0'
uno = Controller(addr)
led_red = Sublight(uno, 2)
led_yellow = Sublight(uno, 3)
led_green = Sublight(uno, 4)
led_blue = Sublight(uno, 5)
led_white1 = Sublight(uno, 6)
led_white2 = Sublight(uno, 7)

led_list = [led_red, led_yellow, led_green, led_blue, led_white1, led_white2]

buzzer = Load(uno, 8)

sublight_1A = led_white1
sublight_1B = led_white2
sublight_2A = led_green
sublight_2B = led_blue
light1 = Light(sublight_1A, sublight_1B)
light2 = Light(sublight_2A, sublight_2B)


def buzz(Hz, sec):

    start = time.time()
    now = time.time()
    try:
        while now - start < sec:
            buzzer.high()
            time.sleep(1 / Hz)
            buzzer.low()
            time.sleep(1 / Hz)
            now = time.time()
    finally:
        buzzer.low()


# @unittest.skip("Skipping TestPump Class...")
class TestSanity(unittest.TestCase):

    def test_sanity(self):
        pass


# @unittest.skip("Skipping TestLight Class...")
class TestController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        uno.connect()

    @classmethod
    def tearDownClass(cls):
        uno.disconnect()

    def setUp(self):
        uno.all_loads_off()

    def tearDown(self):
        buzz(100, 0.5)

    # @unittest.skip("Skipping test")
    def test_reconnect(self):
        uno.reconnect()

    def test_adding_when_connected(self):
        with self.assertRaises(RuntimeError):
            temp = Component(uno, 13)

        with self.assertRaises(RuntimeError):
            temp = Load(uno, 13)

        with self.assertRaises(RuntimeError):
            temp = Valve(uno, 13)

        with self.assertRaises(RuntimeError):
            temp = Pump(uno, 13)

        with self.assertRaises(RuntimeError):
            temp = Sublight(uno, 13)


# @unittest.skip("Skipping TestLight Class...")
class TestLight(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        uno.connect()

    @classmethod
    def tearDownClass(cls):
        uno.disconnect()

    def setUp(self):
        uno.all_loads_off()

    def tearDown(self):
        buzz(100, 0.5)

    def test_light1(self):  # high -> low -> off, twice

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

    # @unittest.skip("Skipping test_light2: light2 not yet implemented")
    def test_light2(self):  # high -> low -> off, twice

        pause_time = 0.5

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

        pause_time = 0.2
        previous_switch = None

        for i in range(10):

            light1.set_mode(light_low_str)
            time.sleep(pause_time)
            self.assertTrue(light1.get_mode() == light_low_str)
            self.assertIsNot(light1.sublight_switch, previous_switch)

    def test_sublight_validity(self):

        uno.disconnect()

        good_light1 = led_red
        good_light2 = led_blue
        bad_light1 = 'hello'
        bad_light2 = Valve(uno, 5)

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

        uno.connect()

        lightc.high()


if __name__ == '__main__':
    unittest.main()
