from config.HydroGroupList import *
import test_triggers

import time
import queue
import Trigger

exec_queue = queue.Queue()
exec_loop = Trigger.ExeQueue(exec_queue)
poll_loop = Trigger.TriggerList(exec_queue, poll_time=1)

for trigger in test_triggers.triggers:
    poll_loop.add_trigger(trigger)


def main():
    exec_loop.start()
    poll_loop.start()

    while True:
        time.sleep(60)

if __name__ == '__main__':

    try:
        print("starting")
        ard1.state = "CONNECTED"
        main()
        print("end")
    finally:
        ard1.state = "DISCONNECTED"
