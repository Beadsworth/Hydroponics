from config.HydroGroupList import *
from Trigger import ClockTrigger, InstantTrigger, OverflowTrigger, Switch

import datetime

time0 = datetime.datetime.now().replace(second=0)
time1 = datetime.datetime.now().replace(second=10)
time2 = datetime.datetime.now().replace(second=20)
time3 = datetime.datetime.now().replace(second=30)
time35 = datetime.datetime.now().replace(second=35)
time4 = datetime.datetime.now().replace(second=40)
time5 = datetime.datetime.now().replace(second=50)

time_hourly = datetime.datetime.now().replace(minute=30, second=0)

sec_10 = datetime.timedelta(seconds=10)
sec_30 = datetime.timedelta(seconds=30)

task0 = ClockTrigger(light1, "LOW", clock1, time0, sec_10, 'minute')
task1 = ClockTrigger(light1, "LOW", clock1, time1, sec_10, 'minute')
task2 = ClockTrigger(light1, "LOW", clock1, time2, sec_10, 'minute')
task3 = ClockTrigger(light1, "LOW", clock1, time3, sec_10, 'minute')
task4 = ClockTrigger(light1, "LOW", clock1, time4, sec_10, 'minute')
task5 = ClockTrigger(light1, "LOW", clock1, time5, sec_10, 'minute')
task6 = ClockTrigger(outlet1, "OPEN", clock1, time3, sec_10, 'minute')
task6b = ClockTrigger(outlet1, "CLOSED", clock1, time5, sec_10, 'minute')
task7 = Switch(level1, 'FULL', pump1, 'OFF')
task7b = Switch(level1, 'EMPTY', pump1, 'ON')
task8 = ClockTrigger(control2, "OPEN", clock1, time2, sec_10, 'hour')
task9 = ClockTrigger(control2, "CLOSED", clock1, time5, sec_10, 'hour')
task11 = ClockTrigger(control3, "OPEN", clock1, time0, sec_10, 'minute')
task12 = ClockTrigger(control3, "CLOSED", clock1, time35, sec_10, 'minute')
task_hourly = ClockTrigger(twitter_account, "TEST MESSAGE", clock1, time_hourly, sec_30, 'hour')


triggers = [
    task0,
    task1,
    task2,
    task3,
    task4,
    task5,
    task6,
    task6b,
    task7,
    task7b,
    task8,
    task9,
    task_hourly,
    task11,
    task12
]


