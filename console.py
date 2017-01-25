#!/usr/bin/env python
import System
import test_triggers
import time
import threading

from config.HydroGroupList import *

system1 = System.ArduinoSystem(ard1, 'system1')

for trigger in test_triggers.triggers:
    system1.add_trigger(trigger)


def quit():

    system1.stop()
    print("end")

    print("active thread count:", threading.active_count())
    thread_list = threading.enumerate()
    print("active threads:")
    for thread in thread_list:
        print(thread.name)

    print("Done!")
    exit()

if __name__ == '__main__':

    print("starting script...")

    print("active thread count:", threading.active_count())
    thread_list = threading.enumerate()
    print("active threads:")
    for thread in thread_list:
        print(thread.name)

    system1.start()

    print("active thread count:", threading.active_count())
    thread_list = threading.enumerate()
    print("active threads:")
    for thread in thread_list:
        print(thread.name)

    print('')
    print("awaiting input...")