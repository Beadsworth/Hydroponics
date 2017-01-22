from Components.Component import Component

import datetime


class Clock(Component):

    @staticmethod
    def by_year(datetime_obj):
        return datetime_obj.replace(year=2000)

    @staticmethod
    def by_month(datetime_obj):
        return Clock.by_year(datetime_obj).replace(month=1)

    @staticmethod
    def by_week(datetime_obj):
        return Clock.by_month(datetime_obj).replace(year=2000)

    @staticmethod
    def by_day(datetime_obj):
        return Clock.by_year(datetime_obj).replace(year=2000)

    @staticmethod
    def by_month(datetime_obj):
        return Clock.by_year(datetime_obj).replace(year=2000)

    @property
    def state(self):
        """Return current clock time (datetime object), to the nearest second."""
        now = datetime.datetime.now().replace(microsecond=0)
        return now
