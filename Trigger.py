from Groups.FloodZone import FloodZone
from config.HydroGroupList import *
from config.HydroComponentList import *

import datetime
import time


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

    def __init__(self, item, target_state, clock, start_time, window, repeat_by='none'):
        # window must be datetime.timedelta object
        super().__init__(persistent=True)

        if repeat_by not in ('none', 'day', 'hour', 'minute'):
            raise RuntimeError("repeat_by argument invalid")

        if repeat_by == 'none':
            self._persistent = False

        self._item = item
        self._target_state = target_state
        self._clock = clock
        self._start_time = start_time
        self._end_time = start_time + window
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
