import datetime
import copy
from LoadList import pump_tuple, light_tuple, valve_tuple, load_tuple, zone_tuple


def close_all_valves():

    for valve in valve_tuple:
        valve.close()


def open_all_valves():

    for valve in valve_tuple:
        valve.open()


def shutdown_all():

    close_all_valves()

    for pump in pump_tuple:
        pump.off()

    for light in light_tuple:
        light.off()


class Task:
    # TODO add repeat flag; some tasks should be repeated daily
    def __init__(self, exe_time, function, *args):

        # TODO add ability to initiate from string
        self.exe_time = exe_time
        self.function = function
        self.args = args

    def write_task(self):
        # return string to write to txt file
        pass

    def do(self):
        """Will do task immediately when called.  Waiting implemented in TaskQueue"""

        status = self.function(*self.args)


class TaskQueue:

    def __init__(self):
        self.queue = []
        self.index = -1
        self.length = 0
        self.current_task = None

        # for task in schedule.txt:
            # self.queue.append(task)

        self.refresh()

    def catch_up(self):
        """Find index of next task and start queue there.  If current time greater than all tasks,
        index = 0 and current_task is first task in queue (i.e., prepare for next day)"""
        # TODO change minute refresh to day refresh
        if len(self.queue) == 0:
            return copy.copy(self.index)

        self.index = -1
        self.current_task = self.queue[0]

        current_time = datetime.datetime.now()
        deltat = datetime.timedelta(milliseconds=-1)
        temp_time = current_time - deltat
        # remove these later
        current_time = current_time.time().second
        temp_time = temp_time.time().second

        while temp_time <= current_time:

            self.index += 1
            if self.index >= len(self.queue):  # end of day
                self.index = 0
                self.current_task = self.queue[self.index]
                return copy.copy(self.index)

            self.current_task = self.queue[self.index]
            temp_time = self.current_task.exe_time.second

        return copy.copy(self.index)

    def add_task(self, task):

        self.queue.append(task)
        self.length += 1
        self.refresh()

    def remove_task(self):
        pass

    def refresh(self):
        """Sort queue and create new iterator.  Catch up to current time."""
        self.queue.sort(key=lambda x: x.exe_time)
        self.catch_up()

    def run(self):

        # self.catch_up()
        if self.length == 0:
            return False

        first_task = self.queue[0]
        now = datetime.datetime.now().time().second
        if now >= self.current_task.exe_time.second:

            if (self.index == 0) and (now > first_task.exe_time.second):  # if end of day, skip task
                return False

            print('Index: ' + str(self.index))
            self.current_task.do()
            self.index += 1

            if self.index >= self.length:
                self.catch_up()
                # print('Done!')
                # return True

            self.current_task = self.queue[self.index]

        return False
