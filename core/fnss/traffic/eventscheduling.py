"""Functions and classes for creating and manipulating event schedules.

An event schedule is simply a list of events each labelled with a time and a
number of properties.

An event schedule can be read and written from/to an XML files with provided
functions.
"""
import random
import bisect
import copy
import xml.etree.cElementTree as ET

import fnss.util as util
from fnss.units import time_units

__all__ = [
    'EventSchedule',
    'deterministic_process_event_schedule',
    'poisson_process_event_schedule',
    'write_event_schedule',
    'read_event_schedule'
           ]

class EventSchedule(object):
    """Class representing an event schedule. This class is simply a wrapper for
    a list of events.
    """

    # NOTE: This class doesn't have a __setitem__ method because the insertion
    # of an event is done so that the schedule remains chronologically sorted.
    # Therefore, users cannot be allowed to insert events in an arbitrary
    # position of the schedule.

    def __init__(self, t_start=0, t_unit='ms'):
        """Initialize the event schedule

        Parameters
        ----------
        t_start : float, optional
            Time at which the event schedule starts
        t_unit : str, optional
            The unit of time
        """
        if not t_unit in time_units:
            raise ValueError("The t_unit argument is not valid")
        self.attrib = {}
        self.attrib['t_start'] = t_start
        self.attrib['t_end'] = t_start
        self.attrib['t_unit'] = t_unit
        # Implement event schedule as list of (time, event) tuple
        # Couldn't use dict because can have several events with same timestamp
        self.event = []

    def __len__(self):
        """Return the number of events in the schedule. Use the expression
        'len(schedule)'
        """
        return len(self.event)

    def __iter__(self):
        """Iterates over the events of the schedule. Use the expression
        'for event in event_schedule'
        """
        return iter(self.event)

    def __getitem__(self, key):
        """Return the event in a specific position of the schedule. Use the
        expression 'event_schedule[i]'
        """
        return self.event[key]

    def __delitem__(self, key):
        """Remove the event in a specific position of the schedule. Use the
        expression 'del event_schedule[i]'
        """
        self.event.pop(key)

    def __add__(self, other):
        """Merge two events schedules.

        This method takes all the events of the schedule passed as argument,
        add them to the event schedule it belongs to and returned the merged
        schedule. The events of the schedule after the merging are still
        chronologically sorted.

        Parameters
        ----------
        other : EventSchedule
            The event schedule whose events are added to this one.
        """
        es = copy.copy(self)
        es.add_schedule(other)  # merge with shallow copy
        return es

    def __radd__(self, other):
        """Merge two events schedules.

        This method takes all the events of the schedule passed as argument,
        add them to the event schedule it belongs to and returned the merged
        schedule. The events of the schedule after the merging are still
        chronologically sorted.

        Parameters
        ----------
        other : EventSchedule
            The event schedule whose events are added to this one.
        """
        return self.__add__(other)

    def add(self, time, event, absolute_time=False):
        """Adds an event to the schedule.

        Events are inserted so that the schedule is always chronologically
        sorted.

        Parameters
        ----------
        time : float
            The time at which the event takes place
        event : dict
            The properties of the event
        absolute_time : bool, optional
            Specifies whether the time is expressed as absolute time or as
            interval from the latest event of the schedule
        """
        # When a new event is inserted, make sure it is inserted in
        # chronological order
        if absolute_time and time < 0:
            raise ValueError('Time must be a positive value')
        if absolute_time:
            if time < self.attrib['t_end']:
                bisect.insort(self.event, (time, event))  # maintain list sorted
                return
            self.attrib['t_end'] = time
        else:
            self.attrib['t_end'] += time
            time = self.attrib['t_end']
        self.event.append((time, event))

    def pop(self, i):
        """
        Remove from the schedule the event in a specific position

        Parameters
        ----------
        i : int
            The index of the event to pop

        Returns
        -------
        event : tuple (time, event)
            The event popped from the schedule
        """
        return self.event.pop(i)

    def number_of_events(self):
        """Return the number of events in the schedule

        Returns
        -------
        number_of_events : int
            The number of events of the schedule
        """
        return len(self.event)

    def add_schedule(self, event_schedule):
        """Merge with another event schedule.

        This method takes all the events of the schedule passed as argument
        and add them to the event schedule it belongs to. The events of the
        schedule after the merging are still chronologically sorted.

        Parameters
        ----------
        event_schedule : EventSchedule
            The event schedule whose events are added to this one.

        Notes
        -----
        All the events are sorted
        """
        this_t_unit = time_units[self.attrib['t_unit']]
        other_t_unit = time_units[event_schedule.attrib['t_unit']]
        conv_factor = float(other_t_unit) / float(this_t_unit)
        for time, event_props in event_schedule:
            self.add(time * conv_factor, event_props, absolute_time=True)

    def events_between(self, t_start, t_end):
        """Return an event schedule comprising all events scheduled between a
        start time (included) and an end time (excluded).

        Parameters
        ----------
        t_start : float
            The start time
        t_end : float
            The end time

        Returns
        -------
        event_schedule : EventSchedule
            An EventSchedule object
        """
        if t_end <= t_start:
            raise ValueError('end_time must be greater than start_time')
        event_schedule = EventSchedule()
        event_schedule.attrib['t_start'] = t_start
        event_schedule.attrib['t_end'] = t_end
        event_schedule.attrib['t_unit'] = self.attrib['t_unit']
        event_schedule.event = [(time, event) for (time, event) in self.event
                                if time >= t_start and time < t_end]
        return event_schedule


def deterministic_process_event_schedule(interval, t_start, duration, t_unit,
                                         event_generator, *args, **kwargs):
    """Return a schedule of events separated by a fixed time interval

    Parameters
    ----------
    interval : float
        The fixed time interval between subsequent events

    t_start : float
        The time at which the schedule starts
    duration : float
        The duration of the event schedule
    t_unit: string
        The unit in which time values are expressed (e.g. 'ms', 's')
    event_generator : function
        A function that when called returns an event, i.e. a dictionary of
        event properties
    *args : argument list
        List of non-keyworded arguments for event_generator function
    **kwargs : keyworded argument list
        List of keyworded arguments for event_generator function

    Returns
    -------
    event_schedule : EventSchedule
        An EventSchedule object
    """
    t_end = t_start + duration
    t_last_event = t_start
    event_schedule = EventSchedule(t_start=t_start, t_unit=t_unit)
    while True:
        t_last_event += interval
        if t_last_event < t_end:
            event = event_generator(*args, **kwargs)
            event_schedule.add(t_last_event, event, absolute_time=True)
        else:
            break
    return event_schedule


def poisson_process_event_schedule(avg_interval, t_start, duration, t_unit,
                                   event_generator, *args, **kwargs):
    """Return a schedule of Poisson-distributed events

    Parameters
    ----------
    avg_interval : float
        The average time interval between subsequent events

    t_start : float
        The time at which the schedule starts
    duration : float
        The duration of the event schedule
    t_unit : string
        The unit in which time values are expressed (e.g. 'ms', 's')
    seed : int, long or hashable type, optional
        The seed to be used by the random generator.
    event_generator : callable
        A function that when called returns an event, i.e. a dictionary of
        event properties
    *args : argument list
        List of non-keyworded arguments for event_generator function
    **kwargs : keyworded argument list
        List of keyworded arguments for event_generator function

    Returns
    -------
    event_schedule : EventSchedule
        An EventSchedule object

    Example
    -------
    >>> import random, fnss
    >>> def my_event_gen(p):
    ...     event_props = {}
    ...     r = random.random()
    ...     if r > p:
    ...         event_props['action']='send_email'
    ...     else:
    ...         event_props['action']='watch_video'
    ...     return event_props
    ...
    >>> schedule = fnss.schedule_dynamic_poisson_events(15, 0, 8000, 'ms',
    ... my_event_gen, p=0.5)
    """
    t_end = t_start + duration
    t_last_event = t_start
    event_schedule = EventSchedule(t_start=t_start, t_unit=t_unit)
    while True:
        t_last_event += (random.expovariate(1.0 / avg_interval))
        if t_last_event < t_end:
            event = event_generator(*args, **kwargs)
            event_schedule.add(t_last_event, event, absolute_time=True)
        else:
            break
    return event_schedule


def read_event_schedule(path):
    """Read event schedule from an XML file

    Parameters
    ----------
    path : str
        The path to the event schedule XML file

    Returns
    -------
    event_schedule : EventSchedule
        The parsed event schedule
    """
    event_schedule = EventSchedule()
    tree = ET.parse(path)
    head = tree.getroot()
    for prop in head.findall('property'):
        name = prop.attrib['name']
        value = util.xml_cast_type(prop.attrib['type'], prop.text)
        event_schedule.attrib[name] = value
    # this is needed for not messing up the automatic sorting of the event list
    event_schedule.attrib['t_end'] = 0
    for event in head.findall('event'):
        time = float(event.attrib['time'])
        event_prop = {}
        for prop in event.findall('property'):
            name = prop.attrib['name']
            value = util.xml_cast_type(prop.attrib['type'], prop.text)
            event_prop[name] = value
        event_schedule.add(time, event_prop, absolute_time=True)
    return event_schedule


def write_event_schedule(event_schedule, path,
                         encoding='utf-8', prettyprint=True):
    """Write an event schedule object to an XML file.

    Parameters
    ----------
    event_schedule : EventSchedule
        The event schedule to write
    path : str
        The path of the output XML file
    encoding : str, optional
        The desired encoding of the output file
    prettyprint : bool, optional
        Specify whether the XML file should be written with indentation for
        improved human readability
    """
    head = ET.Element("event-schedule")
    for name, value in event_schedule.attrib.items():
        prop = ET.SubElement(head, "property")
        prop.attrib['name'] = str(name)
        prop.attrib['type'] = util.xml_type(value)
        prop.text = str(value)
    for time, event_props in event_schedule:
        event = ET.SubElement(head, "event")
        event.attrib['time'] = str(time)
        for name, value in event_props.items():
            prop = ET.SubElement(event, "property")
            prop.attrib['name'] = str(name)
            prop.attrib['type'] = util.xml_type(value)
            prop.text = str(value)
    if prettyprint:
        util.xml_indent(head)
    ET.ElementTree(head).write(path, encoding=encoding)
