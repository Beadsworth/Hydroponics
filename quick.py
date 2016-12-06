from test_HydroLoads import *

"""DOES NOT EXIT CLEANLY!"""

addr1 = '/dev/ttyACM0'
mega1 = Controller(addr1)
load1 = Valve(mega1, 52)
load2 = Valve(mega1, 50)
load3 = Valve(mega1, 48)
load4 = Valve(mega1, 46)
load5 = Valve(mega1, 44)
load6 = Valve(mega1, 42)
load7 = Valve(mega1, 40)
load8 = Valve(mega1, 38)
relay1 = RelayBoard(mega1, 36)
buzzer = Load(mega1, 34)


def buzz():
    Hz = 200
    buzz_time = 0.5
    start = time.time()
    now = time.time()
    try:
        while now - start < buzz_time:
            buzzer.on()
            time.sleep(1 / Hz)
            buzzer.off()
            time.sleep(1 / Hz)
            now = time.time()
    finally:
        buzzer.off()


def get_mega():

    mega1.connect()
    return mega1
