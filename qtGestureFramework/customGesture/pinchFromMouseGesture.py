

from PyQt5.QtWidgets import QGesture

from qtGestureFramework.customGesture.pinchable import Pinchable


class PinchFromMouseGesture(Pinchable, QGesture): 
  '''
  A custom gesture.
  
  This particular one simulates a two-finger pinch from mouse events.
  See Pinchable.
  
  See recognizer for:
  - what mouse motion engenders the gesture state
  - how properties of gesture derived from motion
  
  All methods below are reimplementation of base class.
  '''
  def __init__(self, parent):
    print("init PinchFromMouseGesture", parent)
    Pinchable.initialize(self)
    super().__init__(parent)


  def gestureCancelPolicy(self):
    #print "cancelPolicy"
    return QGesture.CancelNone
  
  """
  def gestureType(self):
    ''' This property is constant: no setter.  But you must implement this getter. '''
    print "gestureType"
    return Qt.CustomGesture
  """
  
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
  """
  