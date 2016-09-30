import datetime
import copy
from pathlib import Path
from Beep import beep, beep_scale
# TODO remove beep, fix eval


class Task:
    # TODO add repeat flag; some tasks should be repeated daily
    def __init__(self, exe_time, repeat, function, *args):

        if not isinstance(exe_time, datetime.time):
            raise TypeError('Must be datetime.time object')

        # TODO add ability to initiate from string
        # exec_time should be datetime.time object
        # repeat -> True or False
        self.exe_time = exe_time
        self.repeat = repeat
        self.function = function
        self.args = args

    # TODO more tests on __str__ and __repr__
    def __repr__(self):
        arg_str = ''
        for item in self.args:
            if isinstance(item, str):
                arg_str += (', \'' + item + '\'')
            else:
                arg_str += (', ' + str(item))

        return 'Task(%s, %s, %s%s)' \
               % (repr(self.exe_time), repr(self.repeat), self.function.__name__, arg_str)

    def __str__(self):
        return 'exe_time: %s, repeat: %s, function: %s, args: %s' \
               % (str(self.exe_time)[:8], repr(self.repeat), self.function.__name__, [str(item) for item in self.args])

    def task_str(self):
        # return string to write to txt file
        pass

    def do(self):
        """Will do task immediately when called.  Waiting implemented in TaskQueue"""

        status = self.function(*self.args)
        return status


def task_from_str(input_string):
    # TODO fix eval() vulnerability
    # expected format ---> Task(datetime.time(1, 1, 1), True, beep, 'G5', 1)
    return eval(input_string)


class TaskQueue:

    def __init__(self, filename_str='TaskQueue.txt'):
        self.filename_str = filename_str
        self.queue = []
        self.index = -1
        self.length = 0
        self.current_task = None

        if Path('./' + self.filename_str).is_file():  # if file exists
            with open(self.filename_str, 'r') as sched_file:
                for line in sched_file:
                    single_task = task_from_str(line[:-1])
                    self.add_task(single_task)

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

        temp_index = 0

        if self.length > 0:  # if length == 0, just append to empty queue

            for i in range(self.length):
                if task.exe_time.second < self.queue[temp_index].exe_time.second:
                    break
                temp_index += 1

        self.queue.insert(temp_index, task)
        self.length += 1
        # self.refresh()

    def remove_task(self, index):
        del self.queue[index]
        self.length -= 1

    def refresh(self):
        """Sort queue and catch up to current time."""
        self.queue.sort(key=lambda x: x.exe_time)
        self.catch_up()

    def run(self):
        # TODO figure out return status
        # TODO log each action

        status = None

        if self.length == 0:
            return status

        # if queue just initialized, current_task should be None.  catch_up if current_task is None
        if self.current_task is None:
            self.catch_up()

        # by this point, queue has at least one task
        first_task = self.queue[0]
        now = datetime.datetime.now().time().second
        if now >= self.current_task.exe_time.second:

            if (self.index == 0) and (now > first_task.exe_time.second):  # if end of day, skip task
                return status

            # print('Index: ' + str(self.index))
            status = self.current_task.do()

            # TODO remove task from txt file if repeat is False
            if self.current_task.repeat is False:  # if no repeat, remove task and don't change index
                self.remove_task(self.index)
            else:
                self.index += 1

            if self.index >= self.length:
                self.catch_up()
                # print('Done!')
                # return True

            self.current_task = self.queue[self.index]

        return status

    def write_queue(self):

        if self.filename_str is None:
            raise RuntimeError('This TaskQueue has no txt-file!')
        with open(self.filename_str, 'w') as sched_file:
            for task in self.queue:
                sched_file.write(repr(task) + '\n')
