#!/usr/bin/env python

from LoadList import *

if __name__ == '__main__':

    ard.connect()

    try:
        while True:
            task = input('>>>')
            if task is None or task.lower() == "exit()":
                break
            elif task == '':
                pass
            else:
                eval(task)
    finally:
        ard.disconnect()

    print("Done!")