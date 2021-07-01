# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Events Class Tests
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
# 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

import unittest
import Event

from ucollections import deque
from utime import localtime
from utime import mktime
from ujson import loads

class Test_Event_TypeAndValueErrors(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        Event.Event.eventQueue = deque((), 100, 1)

    def testEvent_init_NoErrorRaised_1(self):
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = None)
        self.assertIsInstance(a, Event.Event)

    def testEvent_init_NoErrorRaised_2(self):
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = 0)
        self.assertIsInstance(a, Event.Event)

    def testEvent_init_NoErrorRaised_3(self):
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = None)
        b = Event.Event.eventQueue.popleft()
        self.assertIs(a, b)


    def testEvent_initFail_ValueError_agent(self):
        with self.assertRaises(ValueError):
            Event.Event('Invalid String',  # String is not in the list of valid event types
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = 0)

    def testEvent_initFail_TypeError_agent(self):
        with self.assertRaises(ValueError):
            Event.Event('Agent Action',
                        ['detail1', 'detail2'], # not a dictionary
                        time = 0)

    def testEvent_initFail_TypeError_agent(self):
        with self.assertRaises(TypeError):
            Event.Event('Agent Action',
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = (2020, 1, 1, 00, 00, 00, 0, 0)) # not a valid time option

    def testEvent_initFail_TypeError_agent(self):
        with self.assertRaises(TypeError):
            Event.Event('Agent Action',
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = 'test') # not a valid time option


class Test_Event_Functions(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        Event.Event.eventQueue = deque((), 100, 1)

    def testEvent_init_Time_1(self):
        t = mktime(localtime())
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = None)
        self.assertAlmostEqual(t, a.getEventTime(asInt=True), delta=1)

    def testEvent_init_Time_2(self):
        t = mktime(localtime())
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = t)
        self.assertEqual(t, a.getEventTime(asInt=True))


    def testEvent_getEventType(self):
        et = 'Agent Action'
        a = Event.Event(et, 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = 0)
        self.assertEqual(et, a.getEventType())

    def testEvent_getEventDetails(self):
        ed = {'detail1': 'test', 'detail2': 'test'}
        a = Event.Event('Agent Action', 
                        ed, 
                        time = 0)
        self.assertIsInstance(a.getEventDetails(), dict)
        self.assertEqual(list(ed.keys()), list(a.getEventDetails().keys()))
        for key in ed:
            self.assertEqual(ed[key], a.getEventDetails()[key])
    
    def testEvent_getEventTime_1(self):
        t = 0 
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = t)
        self.assertIsInstance(a.getEventTime(), tuple)
        self.assertIsInstance(a.getEventTime(asInt=True), int)

    def testEvent_getEventTime_2(self):
        t = 0 
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = t)
        self.assertEqual(a.getEventTime(), localtime(t))
        self.assertEqual(a.getEventTime(asInt=True), t)

    def testEvent_getJson_1(self):
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = None)
        self.assertIsInstance(a.getJson(), str)

    def testEvent_getJson_2(self):
        a = Event.Event('Agent Action', 
                        {'detail1': 'test', 'detail2': 'test'}, 
                        time = None)
        j = loads(a.getJson())
        self.assertIsInstance(j, dict)