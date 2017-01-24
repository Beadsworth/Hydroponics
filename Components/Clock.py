from Components.Component import Component

import datetime


class Clock(Component):

    @property
    def state(self):
        """Return current clock time (datetime object), to the nearest second."""
        now = datetime.datetime.now().replace(microsecond=0)
        return now
