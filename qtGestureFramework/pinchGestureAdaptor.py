
from PyQt5.QtCore import QPointF


class PinchGestureAdaptor(object):
  '''
  Adapts a pinch gesture: adds 'delta' class methods useful for continual updating of a view.
  
  These are deltas between previous (last) reported total value and current total value.
  In other words, between prior two gesture update events.
  These are not present in the QPinchGesture API.
  
  Methods are simple, but also hide complexity, such as vectors, and division by zero.
  '''
  
  @classmethod
  def deltaCenterPoint(cls, gesture):
    '''
    Vector that center of gesture moved since previous GestureEvent.
    '''
    result = gesture.centerPoint() - gesture.lastCenterPoint()
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
      result = gesture.totalScaleFactor() / gesture.lastScaleFactor()
    else:
      result = 1.0  # No change in scale
      
    # Don't scale by a negative number, it flips view ?
    assert result > 0 and result < 1000
    return result
