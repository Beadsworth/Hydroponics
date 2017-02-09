import threading
import queue
import time
import Trigger


class System:

    def __init__(self, name, poll_time=1):
        self._name = name
        self._exec_queue = queue.Queue()
        self._exec_loop = ExeQueue(self._exec_queue, name=(self._name + ' exec loop'))
        self._poll_loop = PollLoop(self._exec_queue, name=(self._name + ' poll loop'), poll_time=poll_time)

    def start(self):
        self._exec_loop.start()
        self._poll_loop.start()

    def stop(self):
        self._poll_loop.stop()
        self._poll_loop.join()
        self._exec_loop.stop()
        self._exec_loop.join()

    def add_trigger(self, trigger):
        self._poll_loop.add_trigger(trigger)

    def do(self, item, state):
        temp_trigger = Trigger.InstantTrigger(item, state)
        self.add_trigger(temp_trigger)


class PollLoop(threading.Thread):

    def __init__(self, exec_queue, name, poll_time=1):
        threading.Thread.__init__(self, name=name)
        self._exec_queue = exec_queue
        self._poll_time = poll_time
        self._trigger_list = []
        self._add_cache = []
        self._remove_cache = []
        self._running = True

    def run(self):
        """Poll for triggers, send commands to exec_loop, clean trigger list.  If running is False, quit"""
        print("Poll loop running...")
        while self._running:
            # queue put method inside _handle_triggers
            self._handle_triggers()
            # print("logging...")
            self._clean_trigger_list()
            self._use_caches()
            time.sleep(self._poll_time)

    def add_trigger(self, trigger):
        self._add_cache.append(trigger)

    def remove_trigger(self, trigger):
        self._remove_cache.append(trigger)

    def _handle_triggers(self):
        """Determines if a trigger has occurred, and sends actions to ExeQueue"""
        for trigger in self._trigger_list:
            if trigger.conditions_met:
                if not trigger.latched:
                    # TODO try execute, handle exceptions
                    print(trigger, "was added to the queue!")
                    # add execute method to execution queue
                    self._exec_queue.put(trigger.execute)
                # latch to prevent multiple executions
                trigger.latched = True
            else:
                # unlatch after trigger is over
                trigger.latched = False

    def _clean_trigger_list(self):
        """prune away used, non-persistent triggers"""
        for trigger in self._trigger_list:
            if trigger.should_not_remain:
                self.remove_trigger(trigger)

    def _use_caches(self):
        """Looks at caches and adds/removes triggers at a convenient time.  Place near end of loop"""
        # remove triggers
        for trigger in self._remove_cache:
            # if trigger exists
            if trigger in self._trigger_list:
                self._trigger_list.remove(trigger)
            else:
                # no such trigger found
                raise RuntimeError("Tried to remove a trigger that did not exist!")
        self._remove_cache = []
        # add triggers
        for trigger in self._add_cache:
            # if trigger already in list
            if trigger in self._trigger_list:
                raise RuntimeError("Trigger added to list more than once!")
            else:
                self._trigger_list.append(trigger)
        self._add_cache = []

    def stop(self):
        # should do finish current cycle
        self._running = False


class ExeQueue(threading.Thread):
    def __init__(self, exec_queue, name):
        threading.Thread.__init__(self, name=name)
        self._exec_queue = exec_queue
        self._running = True

    def run(self):
        print("exec loop running...")
        while self._running:
            # get action when it becomes available
            action = self._exec_queue.get(block=True)
            print('Executing action:', action)
            action()
            self._exec_queue.task_done()

    def stop(self):
        print("stopping...")
        self._running = False
        # send blank function to queue to finish final loop
        self._exec_queue.put(lambda: None)


class ArduinoSystem(System):

    def __init__(self, arduino, name, poll_time=1):
        super().__init__(name, poll_time=poll_time)
        self._arduino = arduino

    def start(self):
        self._arduino.state = "CONNECTED"
        super().start()

    def stop(self):
        super().stop()
        self._arduino.state = "DISCONNECTED"

if __name__ == '__main__':
    pass
