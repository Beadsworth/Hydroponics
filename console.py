#!/usr/bin/env python

from config.HydroSystemList import hydro
from config.HydroGroupList import *
from config.HydroComponentList import *


def quit():

    hydro.stop()
    print("Done!")
    exit()

if __name__ == '__main__':

    print("starting script...")
    hydro.start()
    print("awaiting input...")