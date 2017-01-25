from config.HydroGroupList import *
from Trigger import ClockTrigger, InstantTrigger, OverflowTrigger, LightTrigger

import datetime

time0 = datetime.datetime.now().replace(second=0)
time1 = datetime.datetime.now().replace(second=10)
time2 = datetime.datetime.now().replace(second=20)
time3 = datetime.datetime.now().replace(second=30)
time4 = datetime.datetime.now().replace(second=40)
time5 = datetime.datetime.now().replace(second=50)

sec_10 = datetime.timedelta(seconds=10)

task0 = ClockTrigger(light1, "LOW", clock1, time0, sec_10, 'minute')
task1 = ClockTrigger(light1, "LOW", clock1, time1, sec_10, 'minute')
task2 = ClockTrigger(light1, "LOW", clock1, time2, sec_10, 'minute')
task3 = ClockTrigger(light1, "LOW", clock1, time3, sec_10, 'minute')
task4 = ClockTrigger(light1, "LOW", clock1, time4, sec_10, 'minute')
task5 = ClockTrigger(light1, "LOW", clock1, time5, sec_10, 'minute')
task6 = OverflowTrigger(zone1)
task7 = LightTrigger(zone1, light1)
task8 = ClockTrigger(pump1, "ON", clock1, time2, sec_10, 'hour')
task9 = ClockTrigger(pump1, "OFF", clock1, time5, sec_10, 'hour')
task10 = ClockTrigger(zone1, "FILL", clock1, time5, sec_10, 'hour')

triggers = [
    task0,
    task1,
    task2,
    task3,
    task4,
    task5,
    task6,
    task7,
    task8,
    task9,
    task10
]


