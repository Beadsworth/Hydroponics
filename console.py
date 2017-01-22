#!/usr/bin/env python

from config.HydroGroupList import *


def quit():
    ard1.state = "DISCONNECTED"
    print("Done!")
    exit()

if __name__ == '__main__':

    ard1.state = "CONNECTED"
    print("awaiting input...")
