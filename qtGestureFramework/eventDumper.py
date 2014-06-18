
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer

from qtGestureFramework.gestureAble import GestureAble


class EventDumper(object):
  '''
  Print events and class that received them
  
  Know maps from enum value to keys
  '''
  def __init__(self):
    self.eventTypeMap = self._buildEnumMap(QEvent, QEvent.Type) # _buildEventTypeMap()
    self.gestureTypeMap = self._buildEnumMap(Qt, Qt.GestureType)
    self.gestureStateMap = self._buildEnumMap(Qt, Qt.GestureState)
    self.gestureRecognizerResultFlagMap = self._buildEnumMap(QGestureRecognizer, QGestureRecognizer.ResultFlag)
    
    # Add item for one custom gesture
    self.gestureTypeMap[257] = 'PinchFromMouseGesture'

    
  def _buildEnumMap(self, className, typeName):
    ''' 
    Map from class having className to name of enum having typeName. 
    PyQt only
    '''
    enumMap = {}
    for key, value in vars(className).items():
      if isinstance(value, typeName):
        #print(key, value)
        enumMap[value] = key
    # print(enumMap)
    assert len(enumMap)>0
    return enumMap
       
  def dump(self, event, receiverName):
    '''
    '''
    # General for any event, but brief.
    print(receiverName, "event", self.eventTypeMap[event.type()])
    
    if GestureAble.isEventGestureRelated(event):
        self.dumpGestureRelatedEvent(event)
        
  
  def dumpGestureRelatedEvent(self, event):
    '''
    Special for QGestureEvent, detailed.
    '''
    assert GestureAble.isEventGestureRelated(event)
    print('Gesture event accepted? {}'.format(event.isAccepted()))
    if event.type() == QEvent.GestureOverride:
      print("Gesture is OVERRIDE")
    try:
      self._dumpGestureEvent(event)
    except:
      print("Failed to dump event") # .format(dir(event)))
      # GestureOverride events are missing gestures() method, etc.
    
      
  def _dumpGestureEvent(self, event):
    '''
    Separate method because OSX raises AttributeError on event.activeGestures ????
    '''
    activeGestures = event.activeGestures()
    if len(activeGestures) > 0:
      for gesture in activeGestures:
        print("   Active gesture {} {}".format(self.gestureTypeMap[gesture.gestureType()],
                                      self.gestureStateMap[gesture.state()]))
    else:
      print("   No active gestures in event")
    
    '''
    !!! Canceled gestures are separate, are not active.
    '''
    canceledGestures = event.canceledGestures()
    if len(canceledGestures) > 0:
      for gesture in canceledGestures:
        print("   Canceled gesture {} {}".format(self.gestureTypeMap[gesture.gestureType()],
                                      self.gestureStateMap[gesture.state()]))

#global
eventDumper = EventDumper()
