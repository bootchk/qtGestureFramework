

from PyQt5.QtWidgets import QGesture


class pinchFromMouseGesture(QGesture): 
  '''
  A custom gesture.
  
  This particular one simulates a two-finger pinch from mouse events.
  In a minimal way:
  - mouse button press creates gesture
  - changes to begun state with a little movement
  - changes to state canceled if mouse button release without enough movement
  - changes to finished state with mouse button release and enough movement
  (That is, you really don't make a shape, just the distance moved determines the state.)
  
  It has all the properties of a two-finger pinch gesture: 
  -rotation, 
  -center, and
  -scale factor.
  Again, fabricated in a simple way: proportional to the distance moved.
  
  All methods below are reimplementation of base class.
  '''
  def __init__(self, parent):
    #print "initting MyGesture", parent
    super().__init__()  # parent?
    #print self.gestureType()
    #print "returning init"

  def gestureCancelPolicy(self):
    #print "cancelPolicy"
    return QGesture.CancelNone
  
  """
  def gestureType(self):
    ''' This property is constant: no setter.  But you must implement this getter. '''
    print "gestureType"
    return Qt.CustomGesture
  """
  
  def hasHotSpot(self):
    ''' This property is constant: no setter.  But you must implement this getter. '''
    #print "hasHotSpot"
    return False
  
  def hotSpot(self):
    ''' '''
    #print "hotSpot"
    return False
  
  def setHotSpot(self, value):
    #print "sethotSpot"
    pass
    
  def unsetHotSpot(self, value):
    #print "unsethotSpot"
    pass
    
  def state(self):
    #print "state"
    return super().state()
  
  