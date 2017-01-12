#!/usr/bin/env python

from ComponentList import ard
from GroupList import zone1, zone2, zone3, light1


def quit():
    ard.disconnect()
    print("Done!")
    exit()

if __name__ == '__main__':

    ard.connect()

    print("awaiting input...")
