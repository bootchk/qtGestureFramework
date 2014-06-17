
import sys

from PyQt5.QtCore import QPointF


"""
def isMacOS():
  return sys.platform == 'darwin'
"""


class PinchGestureAdaptor(object):
  '''
  Adapts a pinch gesture: 
  - adds 'delta' class methods useful for continual updating of a view.
  - palliates design flaw on MacOS platform
  
  Implements deltas between previous (last) reported total value and current total value.
  In other words, between prior two gesture events when gesture is in state 'updated'.
  These are not present in the QPinchGesture API.
  QPanGesture.delta() is similar.
  So this helps make both continuous gestures (pinch and pan) have similar delta methods.
  Swipe is a discrete gesture (never comes in the Updated state) and needs no delta method.
  
  Methods hide complexity:
  - vector result for deltaCenterPoint()
  - possible division by zero on deltaScaleFactor()
  - bugs on Mac platform (see qmacgesturerecognizer.cpp in Qt source)
  '''
  
  _lastHotSpot = None
  
  
  @classmethod
  def resetHotSpotBy(cls, gesture):
    cls._lastHotSpot = gesture.hotSpot()

    
  @classmethod
  def deltaCenterPoint(cls, gesture):
    '''
    Vector that center of gesture moved since previous GestureEvent.
    
    !!! MacOS extraordinary
    '''
    if sys.platform == 'darwin':
      result = PinchGestureAdaptor._osxDeltaCenterPoint(gesture)
    else:
      result = PinchGestureAdaptor._usualDeltaCenterPoint(gesture)
    return result
    
    
  @classmethod
  def _usualDeltaCenterPoint(cls, gesture):
    # TODO robustness: check that we received some update i.e. is a continuous gesture.
    result = gesture.centerPoint() - gesture.lastCenterPoint()
    # subtracting two points yields a vector
      
    # !!! Result is a point, but to be interpreted as a vector
    assert isinstance(result, QPointF)
    # Result may be a zero vector
    return result
  
  
  @classmethod
  def _osxDeltaCenterPoint(cls, gesture):
    '''
    On OSX, centerPoint (current, last) are never updated.
    On OSX centerPoint is set by Qt's qmacgesturerecognizer only at begin.
    And hotSpot is a screenPos().
    '''
    result = gesture.hotSpot() - cls._lastHotSpot
    cls._lastHotSpot = gesture.hotSpot()
    # subtracting two points yields a vector
      
    # !!! Result is a point, but to be interpreted as a vector
    assert isinstance(result, QPointF)
    # Result may be a zero vector
    return result
  
  
  @classmethod
  def deltaRotationAngle(cls, gesture):
    '''
    Angle that gesture moved since previous GestureEvent
    '''
    result = gesture.totalRotationAngle() - gesture.lastRotationAngle()
    return result
  
  
  @classmethod
  def deltaScaleFactor(cls, gesture):
    '''
    Ratio of previous scale factor to current scale factor.
    
    That is, you can use the result to scale() an object repeatedly (on every GestureEvent).
    '''
    if gesture.lastScaleFactor() > 0:
      # !!! Should be equivalent to total/last, but total is not updated on OSX
      result = gesture.scaleFactor() / gesture.lastScaleFactor()
    else:
      result = 1.0  # No change in scale
      
    # Don't scale by a negative number, it flips view ?
    assert result > 0 and result < 1000
    return result
