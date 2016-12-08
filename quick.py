import time

from LoadList import *

"""DOES NOT EXIT CLEANLY!"""



def buzz():
    Hz = 200
    buzz_time = 0.5
    start = time.time()
    now = time.time()
    try:
        while now - start < buzz_time:
            buzzer.high()
            time.sleep(1 / Hz)
            buzzer.low()
            time.sleep(1 / Hz)
            now = time.time()
    finally:
        buzzer.low()


def get_mega():

    mega.connect()
    return mega


buzzer = Relay(mega, 34, 'buzzer')
mega = get_mega()

