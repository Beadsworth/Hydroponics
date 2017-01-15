#!/usr/bin/env python

from HydroElementList import *
from HydroComponentList import *
from HydroGroupList import *


def quit():
    ard.disconnect()
    print("Done!")
    exit()

if __name__ == '__main__':

    ard.connect()

    print("awaiting input...")
