from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer


class EventDumper(object):
  '''
  Print events and class that received them
  '''
  def __init__(self):
    self.eventTypeMap = self._buildEnumMap(QEvent, QEvent.Type) # _buildEventTypeMap()
    self.gestureTypeMap = self._buildEnumMap(Qt, Qt.GestureType)
    self.gestureStateMap = self._buildEnumMap(Qt, Qt.GestureState)
    #self.gestureTypeMap = self._buildGestureTypeMap()
    
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
    print(enumMap)
    return enumMap
       
  def dump(self, event, receiverName):
    '''
    '''
    # General for any event, but brief.
    print(receiverName, "event", self.eventTypeMap[event.type()])
    
    if event.type() in (QEvent.Gesture, ):
        self.dumpGestureEvent(event)
        
  
  def dumpGestureEvent(self, event):
    '''
    Special for QGestureEvent, but detailed.
    '''
    assert event.type() == QEvent.Gesture
    print('Gesture event {}'.format(event.isAccepted()))
    activeGestures = event.activeGestures()
    if len(activeGestures) > 0:
      for gesture in activeGestures:
        print("   Active gesture {} {}".format(self.gestureTypeMap[gesture.gestureType()],
                                      self.gestureStateMap[gesture.state()]))
    else:
      print("    active gestures in event")

#global
eventDumper = EventDumper()
