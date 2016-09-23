import unittest
import time
import datetime

from TaskScheduler import open_all_valves, close_all_valves, shutdown_all, zone_tuple, Task, TaskQueue, light_tuple, valve_tuple


class TestTaskScheduler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(3)
        shutdown_all()

    def setUp(self):
        pass

    def tearDown(self):
        shutdown_all()

    def test_sanity(self):
        self.assertTrue(True)

    @staticmethod
    def test_open_close_all_valves():
        open_all_valves()
        time.sleep(1)
        close_all_valves()

    def test_task_queue(self):

        time1 = datetime.time(hour=12, minute=00, second=0)
        time2 = datetime.time(hour=12, minute=00, second=1)
        time3 = datetime.time(hour=12, minute=00, second=2)
        time4 = datetime.time(hour=12, minute=00, second=3)
        time5 = datetime.time(hour=12, minute=00, second=4)
        time6 = datetime.time(hour=12, minute=00, second=5)

        light = light_tuple[0]

        task1 = Task(time1, light.high)
        task2 = Task(time1, zone_tuple[0].fill)
        task3 = Task(time2, zone_tuple[0].maintain)
        task4 = Task(time3, zone_tuple[0].drain)
        task5 = Task(time4, zone_tuple[0].maintain)
        task6 = Task(time5, light.low)
        task7 = Task(time6, light.off)

        sched = TaskQueue()
        sched.add_task(task7)
        sched.add_task(task6)
        sched.add_task(task5)
        sched.add_task(task4)
        sched.add_task(task3)
        sched.add_task(task2)
        sched.add_task(task1)

        done = False

        start_time = time.time()

        while not done:
            # TODO fix NoneType error that happens occasionally
            print('Seconds: ' + str(datetime.datetime.now().time().second))
            done = sched.run()

            #if datetime.datetime.now().time() < time1:
             #   self.assertEqual(light.get_mode(), 'LIGHT_OFF')
            #else:
             #   self.assertEqual(light.get_mode(), 'LIGHT_HIGH')

            time.sleep(0.1)

        while True:
            print('Seconds: ' + str(datetime.datetime.now().time().second))
            print('Index: ' + str(sched.catch_up()))
            time.sleep(1)

        print('sched finished')
        #self.assertEqual(light.get_mode(), 'LIGHT_HIGH')
        time.sleep(5)
        light.off()


if __name__ == '__main__':
    unittest.main()
