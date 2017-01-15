#!/usr/bin/env python

from HydroElementList import *
from HydroComponentList import *
from HydroGroupList import *


def quit():
    ard_test.state = "DISCONNECTED"
    print("Done!")
    exit()

if __name__ == '__main__':

    ard_test.state = "CONNECTED"

    print("awaiting input...")
