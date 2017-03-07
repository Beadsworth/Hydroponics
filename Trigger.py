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
    # TODO block triggers until start time, then repeat?
    def __init__(self, item, target_state, clock, start_str, window_str='00:01:00', repeat_by='none'):
        # window must be datetime.timedelta object
        super().__init__(persistent=True)

        if repeat_by not in ('none', 'day', 'hour', 'minute'):
            raise RuntimeError("repeat_by argument invalid")

        if repeat_by == 'none':
            self._persistent = False

        # create datetime object for start time
        start_time = datetime.datetime.strptime(start_str, '%H:%M:%S')

        # create timedelta object for window
        t = datetime.datetime.strptime(window_str, '%H:%M:%S')
        window = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        if window > datetime.timedelta(hours=24):
            raise RuntimeError("window must be less than 24 hours")

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
        now = self._clock.state
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

            if self._repeat_by == 'none':
                self._end_time += datetime.timedelta(days=1)
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

        new_time = datetime.datetime.min.replace(second=datetime_obj.second)

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

    # wrappers for convenience
    @staticmethod
    def once(item, target_state, clock, start_str, window_str='00:01:00'):
        return ClockTrigger(item, target_state, clock, start_str, window_str, repeat_by='none')

    @staticmethod
    def every_day(item, target_state, clock, start_str, window_str='00:01:00'):
        return ClockTrigger(item, target_state, clock, start_str, window_str, repeat_by='day')

    @staticmethod
    def every_hour(item, target_state, clock, start_str, window_str='00:01:00'):
        return ClockTrigger(item, target_state, clock, start_str, window_str, repeat_by='hour')

    @staticmethod
    def every_minute(item, target_state, clock, start_str, window_str='00:01:00'):
        return ClockTrigger(item, target_state, clock, start_str, window_str, repeat_by='minute')


class OverflowTrigger(Trigger):

    def __init__(self, zone):

        super().__init__(persistent=True)
        self._zone = zone

    @property
    def conditions_met(self):
        # return True if trigger should be executed
        if self._zone.state == 'FULL':
            return True
        else:
            return False

    def execute(self):
        # TODO stop blocking
        # sleep for 10 seconds to prevent float from falling
        self._zone.state = "IDLE"


class Switch(Trigger):

    _item_type = None

    def __init__(self, switch, switch_state, item, item_state):

        super().__init__(persistent=True)

        self._switch = switch
        self._switch_state = switch_state
        self._item = item
        self._item_state = item_state

    @property
    def conditions_met(self):
        # return True if trigger should be executed
        if self._switch.state == self._switch_state:
            return True
        else:
            return False

    def execute(self):
        self._item.state = self._item_state


if __name__ == '__main__':
    pass
