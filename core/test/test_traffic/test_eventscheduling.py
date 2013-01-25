import unittest
from os import environ, path
from fnss.traffic.eventscheduling import *
from nose.tools import *
from random import random

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
        r = random()
        event_props['action'] = action[0] if r > threshold else action[1]
        return event_props


    def test_event_schedule_add(self):
        es = EventSchedule()
        es.add(8, {'add_order': 1}, absolute_time=True)
        es.add(5, {'add_order': 2}, absolute_time=True)
        assert_equal(2, es.number_of_events())
        assert_equal(5, es[0][0])
        assert_equal({'add_order': 2}, es[0][1])
        assert_equal(8, es[1][0])
        assert_equal({'add_order': 1}, es[1][1])
        
    
    def test_event_schedule_pop(self):
        es = EventSchedule()
        es.add(8, {'add_order': 1}, absolute_time=True)
        es.add(5, {'add_order': 2}, absolute_time=True)
        t0, e0 = es.pop(0)
        t1, e1 = es.pop(0)
        assert_equal(5, t0)
        assert_equal(8, t1)
        assert_equal({'add_order': 2}, e0)
        assert_equal({'add_order': 1}, e1)
        assert_equal(0, es.number_of_events())
    
    
    def test_event_schedule_events_between(self):
        es = EventSchedule()
        es.add(5, {'event_order': 3}, absolute_time=True)
        es.add(4, {'event_order': 2}, absolute_time=True)
        es.add(3, {'event_order': 1}, absolute_time=True)
        es.add(7, {'event_order': 5}, absolute_time=True)
        es.add(6, {'event_order': 4}, absolute_time=True)
        es.add(8, {'event_order': 6}, absolute_time=True)
        events = es.events_between(5, 7)
        assert_equal(2, events.number_of_events())
        assert_equal(5, events[0][0])
        assert_equal({'event_order': 3}, events[0][1])
        assert_equal(6, events[1][0])
        assert_equal({'event_order': 4}, events[1][1])


    def test_event_schedule_merge_with(self):
        es1 = EventSchedule(t_unit='s')
        es1.add(3, {'event_order': 1}, absolute_time=True)
        es1.add(5, {'event_order': 3}, absolute_time=True)
        es2 = EventSchedule(t_unit='ms')
        es2.add(4000, {'event_order': 2}, absolute_time=True)
        es2.add(7000, {'event_order': 5}, absolute_time=True)
        es1.merge_with(es2)
        assert_equal(4, len(es1))
        assert_equal('s', es1.attrib['t_unit'])
        assert_equal(3, es1[0][0])
        assert_equal(4, es1[1][0])
        assert_equal(5, es1[2][0])
        assert_equal(7, es1[3][0])


    def test_event_schedule_operators(self):
        es = EventSchedule()
        es.add(5, {'event_order': 3}, absolute_time=True)
        es.add(4, {'event_order': 2}, absolute_time=True)
        es.add(3, {'event_order': 1}, absolute_time=True)
        es.add(7, {'event_order': 5}, absolute_time=True)
        es.add(6, {'event_order': 4}, absolute_time=True)
        es.add(8, {'event_order': 6}, absolute_time=True)
        assert_equal(6, len(es))
        assert_equal(2, len(es[3:5]))
        del es[0]
        assert_equal(5, len(es))
        for ev in es:
            t, _ = ev
            assert_greater_equal(t, es.attrib['t_start'])
            assert_less_equal(t, es.attrib['t_end'])
            
    
    def test_deterministic_process_event_schedule(self):
        action = ['read_email', 'watch_video']
        schedule = deterministic_process_event_schedule(20, 0, 80001, 'ms', 
                                                        self.event_gen, 
                                                        0.5, action=action)
        assert_is_not_none(schedule)
        assert_equal(4000, len(schedule))
        for time, event in schedule: 
            assert_true(event['action'] in action)
            assert_true(time >= 0)
            assert_true(time <= 80001)
    
    
    def test_poisson_process_event_schedule(self):
        action = ['read_email', 'watch_video']
        schedule = poisson_process_event_schedule(15, 0, 8000, 'ms', 
                                                  self.event_gen,
                                                  0.5, action=action)
        assert_is_not_none(schedule)
        for time, event in schedule: 
            assert_true(event['action'] in action)
            assert_true(time >= 0)
            assert_true(time <= 8000)
            
    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_read_write_event_schedule(self):
        action = ['read_email', 'watch_video']
        schedule = deterministic_process_event_schedule(20, 0, 801, 'ms', 
                                                        self.event_gen,
                                                        0.5, action=action)
        time, event = schedule[2]
        tmp_es_file = path.join(TMP_DIR, 'event-schedule.xml')
        write_event_schedule(schedule, tmp_es_file)
        read_schedule = read_event_schedule(tmp_es_file)
        assert_equal(len(schedule), len(read_schedule))
        read_time, read_event = read_schedule[2]
        assert_equal(time, read_time)
        assert_equal(event, read_event)
        
    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_read_write_event_schedule_special_type(self):
        schedule = EventSchedule()
        event = {'tuple_param': (1,2,3),
                 'dict_param': {'a': 1, 'b': 2},
                 'list_param':[1, 'hello', 0.3]}
        schedule.add(1, event)
        tmp_es_file = path.join(TMP_DIR, 'event-schedule-special.xml')
        write_event_schedule(schedule, tmp_es_file)
        read_schedule = read_event_schedule(tmp_es_file)
        assert_equal(len(schedule), len(read_schedule))
        _, read_event = read_schedule[0]
        assert_equal(event, read_event)
        assert_equal(tuple, type(read_event['tuple_param']))
        assert_equal(list, type(read_event['list_param']))
        assert_equal(dict, type(read_event['dict_param']))
        assert_equal(event['dict_param'], read_event['dict_param'])    
        assert_equal(event['list_param'], read_event['list_param'])  
        assert_equal(event['tuple_param'], read_event['tuple_param'])  
