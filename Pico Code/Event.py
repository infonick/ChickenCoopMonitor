from ucollections import deque
from ujson import dumps

from utime import localtime
from utime import mktime

class Event():
    """
    An Event class for communicating AI events.

    ≡≡≡ Attributes ≡≡≡
    eventQueue: A deque of length 100 to hold events
    eventTypes: A list of valid event types
    
    ≡≡≡ Methods ≡≡≡
    __init__(eventType, eventDetails, time=None):
        Initializes an Event Object and adds it to the event Queue
    
    getEventType():
        Returns a string representation of the event type.
    
    def getEventDetails():
        Returns the 'eventDetails' dictionary.
    
    def getEventTime(asInt = False):
        Returns the time as an integer of seconds since Jan 1st 1970, or a
        localtime tuple of (year, month, day, hour, minute, second, DOTW, DOTY).
    
    getJson():
        Returns a json string of a dictionary of event details in the format 
        {'eventType': e, 'time': t, 'details': d}
    """
    eventQueue = deque((), 100, 1)
    eventTypes = ['Agent Action',
                  'IRQ Triggered']
    
    def __init__(self, eventType, eventDetails, time=None):
        """
        Validates the parameter inputs for, and instantiates, an Event Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        eventType:    one of the official types of events in the list of
                      event.eventTypes 
        eventDetails: a dictionary object of event details

        ≡≡≡ Optional Parameters ≡≡≡
        time: an integer representing the number of seconds from Jan 1st 1970
              at midnight. If time is None, the time is automatically included.
              
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not correct
        ValueError: if the supplied parameter value is incorrect
        
        ≡≡≡ Returns ≡≡≡
        Event Object
        """
        if str(eventType) not in Event.eventTypes:
            raise ValueError ("\'eventType\' must be one of " +
                                  str(self.eventTypes) +
                                  ".")
        if not isinstance(eventDetails, dict):
            raise ValueError ("\'eventDetails\' must be of type \'dict\'.")

        if not isinstance(time, int) and time is not None:
            raise TypeError ("\'time\' must be of type \'int\' or \'None\'.")
        
        self.eventType = self.eventTypes.index(str(eventType))
        self.eventDetails = eventDetails
        if isinstance(time, int):
            self.time = time
        else:
            self.time = mktime(localtime())
        
        try:
            Event.eventQueue.append(self)
        except IndexError:
            pass
            # Log Error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    def getEventType(self):
        """Returns a string representation of the event type."""
        return self.eventTypes[self.eventType]

    def getEventDetails(self):
        """Returns the 'eventDetails' dictionary."""
        return self.eventDetails
    
    def getEventTime(self, asInt = False):
        """
        Returns the time as an integer of seconds since Jan 1st 1970, or a
        localtime tuple of (year, month, day, hour, minute, second, DOTW, DOTY).
        """
        if asInt:
            return self.time
        else:
            return localtime(self.time)

    def getJson(self):
        """
        Returns a json string of a dictionary of event details in the format 
        {'eventType': e, 'time': t, 'details': d}
        """
        out = {'eventType': self.getEventType(), 
               'time':self.getEventTime(asInt=True), 
               'details':self.getEventDetails()}
        return dumps(out)
