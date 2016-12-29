#!/usr/bin/env python

from LoadList_2 import *


def quit():
    ard.disconnect()
    print("Done!")
    exit()

if __name__ == '__main__':

    ard.connect()

    print("awaiting input...")
