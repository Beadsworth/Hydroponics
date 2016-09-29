import unittest
import time
import datetime

from TaskScheduler import Task, TaskQueue
from Beep import beep, beep_scale


class TestTaskScheduler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sanity(self):
        self.assertTrue(True)

    def test_task_queue(self):

        time1 = datetime.time(hour=12, minute=00, second=0)
        time2 = datetime.time(hour=12, minute=00, second=10)
        time3 = datetime.time(hour=12, minute=00, second=20)
        time4 = datetime.time(hour=12, minute=00, second=30)
        time5 = datetime.time(hour=12, minute=00, second=40)
        time6 = datetime.time(hour=12, minute=00, second=50)

        task1 = Task(time1, True, beep, 'C5')
        task2 = Task(time1, True, beep, 'D5')
        task3 = Task(time2, True, beep, 'E5')
        task4 = Task(time3, True, beep, 'F5')
        task5 = Task(time4, True, beep, 'G5')
        task6 = Task(time5, True, beep, 'A5')
        task7 = Task(time6, False, beep_scale)

        sched = TaskQueue()
        sched.add_task(task7)
        sched.add_task(task6)
        sched.add_task(task5)
        sched.add_task(task4)
        sched.add_task(task3)
        sched.add_task(task2)
        sched.add_task(task1)

        secs_left = 125

        start_time = time.time()

        temp_sec = datetime.datetime.now().time().second
        while secs_left > 0:
            # TODO fix NoneType error that happens occasionally
            current_sec = datetime.datetime.now().time().second
            sched.run()
            if temp_sec != current_sec:
                print('Seconds: ' + str(current_sec))
                temp_sec = current_sec
                secs_left -= 1

        print('First loop complete')
        secs_left = 125
        sched.add_task(task7)

        while secs_left > 0:
            current_sec = datetime.datetime.now().time().second
            sched.run()
            if temp_sec != current_sec:
                print('Seconds: ' + str(current_sec))
                temp_sec = current_sec
                secs_left -= 1


if __name__ == '__main__':
    unittest.main()






