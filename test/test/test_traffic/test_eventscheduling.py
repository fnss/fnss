from os import environ, path
import unittest
import random

import fnss

TMP_DIR = environ['test.tmp.dir'] if 'test.tmp.dir' in environ else None

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def event_gen(self, threshold, action):
        event_props = {}
        r = random.random()
        event_props['action'] = action[0] if r > threshold else action[1]
        return event_props

    def test_event_schedule_add(self):
        es = fnss.EventSchedule()
        es.add(8, {'add_order': 1}, absolute_time=True)
        es.add(5, {'add_order': 2}, absolute_time=True)
        self.assertEqual(2, es.number_of_events())
        self.assertEqual(5, es[0][0])
        self.assertEqual({'add_order': 2}, es[0][1])
        self.assertEqual(8, es[1][0])
        self.assertEqual({'add_order': 1}, es[1][1])


    def test_event_schedule_pop(self):
        es = fnss.EventSchedule()
        es.add(8, {'add_order': 1}, absolute_time=True)
        es.add(5, {'add_order': 2}, absolute_time=True)
        t0, e0 = es.pop(0)
        t1, e1 = es.pop(0)
        self.assertEqual(5, t0)
        self.assertEqual(8, t1)
        self.assertEqual({'add_order': 2}, e0)
        self.assertEqual({'add_order': 1}, e1)
        self.assertEqual(0, es.number_of_events())


    def test_event_schedule_events_between(self):
        es = fnss.EventSchedule()
        es.add(5, {'event_order': 3}, absolute_time=True)
        es.add(4, {'event_order': 2}, absolute_time=True)
        es.add(3, {'event_order': 1}, absolute_time=True)
        es.add(7, {'event_order': 5}, absolute_time=True)
        es.add(6, {'event_order': 4}, absolute_time=True)
        es.add(8, {'event_order': 6}, absolute_time=True)
        events = es.events_between(5, 7)
        self.assertEqual(2, events.number_of_events())
        self.assertEqual(5, events[0][0])
        self.assertEqual({'event_order': 3}, events[0][1])
        self.assertEqual(6, events[1][0])
        self.assertEqual({'event_order': 4}, events[1][1])


    def test_event_schedule_add_schedule(self):
        es1 = fnss.EventSchedule(t_unit='s')
        es1.add(3, {'event_order': 1}, absolute_time=True)
        es1.add(5, {'event_order': 3}, absolute_time=True)
        es2 = fnss.EventSchedule(t_unit='ms')
        es2.add(4000, {'event_order': 2}, absolute_time=True)
        es2.add(7000, {'event_order': 5}, absolute_time=True)
        es1.add_schedule(es2)
        self.assertEqual(4, len(es1))
        self.assertEqual('s', es1.attrib['t_unit'])
        self.assertEqual(3, es1[0][0])
        self.assertEqual(4, es1[1][0])
        self.assertEqual(5, es1[2][0])
        self.assertEqual(7, es1[3][0])

    def test_event_schedule_add_operator(self):
        es1 = fnss.EventSchedule(t_unit='s')
        es1.add(3, {'event_order': 1}, absolute_time=True)
        es1.add(5, {'event_order': 3}, absolute_time=True)
        es2 = fnss.EventSchedule(t_unit='ms')
        es2.add(4000, {'event_order': 2}, absolute_time=True)
        es2.add(7000, {'event_order': 5}, absolute_time=True)
        es3 = es1 + es2
        self.assertEqual(4, len(es3))
        self.assertEqual('s', es3.attrib['t_unit'])
        self.assertEqual(3, es3[0][0])
        self.assertEqual(4, es3[1][0])
        self.assertEqual(5, es3[2][0])
        self.assertEqual(7, es3[3][0])

    def test_event_schedule_operators(self):
        es = fnss.EventSchedule()
        es.add(5, {'event_order': 3}, absolute_time=True)
        es.add(4, {'event_order': 2}, absolute_time=True)
        es.add(3, {'event_order': 1}, absolute_time=True)
        es.add(7, {'event_order': 5}, absolute_time=True)
        es.add(6, {'event_order': 4}, absolute_time=True)
        es.add(8, {'event_order': 6}, absolute_time=True)
        self.assertEqual(6, len(es))
        self.assertEqual(2, len(es[3:5]))
        del es[0]
        self.assertEqual(5, len(es))
        for ev in es:
            t, _ = ev
            self.assertGreaterEqual(t, es.attrib['t_start'])
            self.assertLessEqual(t, es.attrib['t_end'])


    def test_deterministic_process_event_schedule(self):
        action = ['read_email', 'watch_video']
        schedule = fnss.deterministic_process_event_schedule(20, 0, 80001, 'ms',
                                                             self.event_gen,
                                                             0.5, action=action)
        self.assertIsNotNone(schedule)
        self.assertEqual(4000, len(schedule))
        for time, event in schedule:
            self.assertTrue(event['action'] in action)
            self.assertTrue(time >= 0)
            self.assertTrue(time <= 80001)


    def test_poisson_process_event_schedule(self):
        action = ['read_email', 'watch_video']
        schedule = fnss.poisson_process_event_schedule(15, 0, 8000, 'ms',
                                                       self.event_gen,
                                                       0.5, action=action)
        self.assertIsNotNone(schedule)
        for time, event in schedule:
            self.assertTrue(event['action'] in action)
            self.assertTrue(time >= 0)
            self.assertTrue(time <= 8000)

    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_read_write_event_schedule(self):
        action = ['read_email', 'watch_video']
        schedule = fnss.deterministic_process_event_schedule(20, 0, 801, 'ms',
                                                             self.event_gen,
                                                             0.5, action=action)
        time, event = schedule[2]
        tmp_es_file = path.join(TMP_DIR, 'event-schedule.xml')
        fnss.write_event_schedule(schedule, tmp_es_file)
        read_schedule = fnss.read_event_schedule(tmp_es_file)
        self.assertEqual(len(schedule), len(read_schedule))
        read_time, read_event = read_schedule[2]
        self.assertEqual(time, read_time)
        self.assertEqual(event, read_event)

    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_read_write_event_schedule_special_type(self):
        schedule = fnss.EventSchedule()
        event = {'tuple_param': (1, 2, 3),
                 'dict_param': {'a': 1, 'b': 2},
                 'list_param':[1, 'hello', 0.3]}
        schedule.add(1, event)
        tmp_es_file = path.join(TMP_DIR, 'event-schedule-special.xml')
        fnss.write_event_schedule(schedule, tmp_es_file)
        read_schedule = fnss.read_event_schedule(tmp_es_file)
        self.assertEqual(len(schedule), len(read_schedule))
        _, read_event = read_schedule[0]
        self.assertEqual(event, read_event)
        self.assertEqual(tuple, type(read_event['tuple_param']))
        self.assertEqual(list, type(read_event['list_param']))
        self.assertEqual(dict, type(read_event['dict_param']))
        self.assertEqual(event['dict_param'], read_event['dict_param'])
        self.assertEqual(event['list_param'], read_event['list_param'])
        self.assertEqual(event['tuple_param'], read_event['tuple_param'])
