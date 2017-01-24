from Groups.FloodZone import FloodZone
from config.HydroGroupList import *
from config.HydroComponentList import *

import datetime
import time
import threading

import queue


class ExeQueue(threading.Thread):
    def __init__(self, exec_queue):
        threading.Thread.__init__(self)
        self._exec_queue = exec_queue

    def run(self):
        print("exec loop running...")
        while True:
            # get action when it becomes available
            action = self._exec_queue.get(block=True)
            print('Executing action...')
            action()
            self._exec_queue.task_done()


class TriggerList(threading.Thread):

    def __init__(self, exec_queue, poll_time=1):
        threading.Thread.__init__(self)
        self._exec_queue = exec_queue
        self._poll_time = poll_time
        self._trigger_list = []
        self._add_cache = []
        self._remove_cache = []

    def run(self):
        print("Poll loop running...")
        while True:
            # queue put method inside _handle_triggers
            self._handle_triggers()
            print("logging...")
            self._clean_trigger_list()
            self._use_caches()
            time.sleep(self._poll_time)

    def add_trigger(self, trigger):
        self._add_cache.append(trigger)

    def remove_trigger(self, trigger):
        self._remove_cache.append(trigger)

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


class Trigger:
    # default trigger is immediate execution
    def __init__(self, persistent=False):
        # self._item = item
        # self._target_state = target_state
        self._persistent = persistent  # False -> execute once only
        self.latched = False  # True -> skip trigger.  Must reset latch appropriately

    @property
    def should_not_remain(self):
        # if already triggered and should not remain
        return not self._persistent and self.latched

    # property must be calculated every loop, otherwise conditions are static
    # override in child
    @property
    def conditions_met(self):
        return True

    def execute(self):
        pass


















class InstantTrigger(Trigger):

    def __init__(self, item, target_state):

        super().__init__(persistent=False)
        self._item = item
        self._target_state = target_state

    @property
    def conditions_met(self):
        return True

    def execute(self):
        self._item.state = self._target_state


class ClockTrigger(Trigger):

    def __init__(self, item, target_state, clock, start_time, end_time, repeat_by='none'):

        super().__init__(persistent=True)

        if repeat_by not in ('none', 'day', 'hour', 'minute'):
            raise RuntimeError("repeat_by argument invalid")

        if repeat_by == 'none':
            self._persistent = False

        self._item = item
        self._target_state = target_state
        self._clock = clock
        self._start_time = start_time
        self._end_time = end_time
        self._repeat_by = repeat_by
        # adjust times to standard values for repetition
        self.fix_times()

    @property
    def _now(self):
        now = datetime.datetime.now()
        now = ClockTrigger.adj_time(now, self._repeat_by)
        # print("Current time:", now.time())
        return now

    @property
    def conditions_met(self):
        # return True if trigger should be executed
        # now = self._clock.state

        return self._start_time <= self._now <= self._end_time

    def execute(self):
        self._item.state = self._target_state

    def fix_times(self):
        self._start_time = ClockTrigger.adj_time(self._start_time, self._repeat_by)
        self._end_time = ClockTrigger.adj_time(self._end_time, self._repeat_by)

        # if start happens after end -- illogical
        if self._start_time > self._end_time:

            # if one time event, but times out of order, raise exception
            if self._repeat_by == 'none':
                raise RuntimeError("One time event: start time occurs after end time")

            elif self._repeat_by == 'day':
                self._end_time += datetime.timedelta(days=1)
            elif self._repeat_by == 'hour':
                self._end_time += datetime.timedelta(hours=1)
            elif self._repeat_by == 'minute':
                self._end_time += datetime.timedelta(minutes=1)

    @staticmethod
    def adj_time(datetime_obj, period):

        # continue to alter time, return value to break out of alterations
        # default time is datetime.datetime.min()

        new_time = datetime.datetime.min

        new_time = new_time.replace(second=datetime_obj.second)

        if period == 'minute':
            # repeat every minute
            return new_time
        new_time = new_time.replace(minute=datetime_obj.minute)

        if period == 'hour':
            # repeat hourly
            return new_time
        new_time = new_time.replace(hour=datetime_obj.hour)

        if period == 'day':
            # repeat daily
            return new_time
        new_time = new_time.replace(day=datetime_obj.day)
        new_time = new_time.replace(month=datetime_obj.month)
        new_time = new_time.replace(year=datetime_obj.year)

        if period == 'none':
            # execute once at specified time period
            # basically no alterations
            return new_time


class OverflowTrigger(Trigger):

    _item_type = FloodZone.FloodZone

    def __init__(self, zone):

        super().__init__(persistent=True)

        if isinstance(zone, OverflowTrigger._item_type) is False:
            raise RuntimeError("This is a trigger for zones only")
        self._zone = zone

    @property
    def conditions_met(self):
        # return True if trigger should be executed
        if self._zone.state == 'FULL':
            return True
        else:
            return False

    def execute(self):
        self._zone.state = "IDLE"


class LightTrigger(Trigger):

    _item_type = SuperLight.SuperLight

    def __init__(self, zone, light):

        super().__init__(persistent=True)

        if isinstance(light, LightTrigger._item_type) is False:
            raise RuntimeError("This is a trigger for zones only")
        self._zone = zone
        self._light = light

    @property
    def conditions_met(self):
        # return True if trigger should be executed
        if self._zone.state == 'FULL':
            return True
        else:
            return False

    def execute(self):
        self._light.state = "LOW"


if __name__ == '__main__':
    pass
