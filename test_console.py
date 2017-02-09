#!/usr/bin/env python
from config.test_HydroSystemList import test_hydro
from config.test_HydroGroupList import *
from config.test_HydroComponentList import *


def quit():

    test_hydro.stop()
    print("Done!")
    exit()

if __name__ == '__main__':

    print("starting script...")
    test_hydro.start()
    print("awaiting input...")





