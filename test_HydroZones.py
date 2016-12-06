#!/usr/bin/env python
# imports
import unittest
import time
import HydroLoads

from LoadList import zones, controllers, light1


# @unittest.skip("Skipping TestPump Class...")
class TestSanity(unittest.TestCase):

    def test_sanity(self):
        pass


# @unittest.skip("Skipping TestLight Class...")
class TestZones(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        for controller in controllers:
            controller.connect()

    @classmethod
    def tearDownClass(cls):
        for controller in controllers:
            controller.disconnect()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.skip("Skipping test")
    def test_cycle_zones(self):

        time.sleep(3)
        light1.low()
        for zone in zones:
            print('Filling ' + zone.name)
            zone.fill()
            time.sleep(2)

            print('Maintaining ' + zone.name)
            zone.maintain()
            time.sleep(2)

            print('Draining ' + zone.name)
            zone.drain()
            time.sleep(2)

            print('Maintaining ' + zone.name)
            zone.maintain()
            time.sleep(2)

            light1.low()



if __name__ == '__main__':
    unittest.main()
