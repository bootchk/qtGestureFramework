
from PyQt5.QtCore import QPointF, QPoint


class Pinchable(object):
  '''
  Mixin methods for a custom gesture, to emulate a two-finger QPinchGesture.
  In other words, gesture is pinchable, i.e. has API of QPinchGesture.
  
  Names match QPinchGesture.
  
  A subset, only the totals for:
  -rotation, 
  -center,
  -scale factor.
  
  The recognizer also may be implementing a further subset or degradation (i.e. rotation always 0)
  '''
  
  '''
  Getters
  '''
  def centerPoint(self):
    return self._centerPoint
  
  def totalRotationAngle(self):
    return self._totalRotationAngle
  
  def totalScaleFactor(self):
    return self._totalScaleFactor
  
  '''
  Setters, called by recognizer.
  '''
  def setCenterPoint(self, value):
    assert isinstance(value, (QPointF, QPoint))
    '''
    Coerce to QPointF.
    Since all mouse events to the recognizer are QPoint in the frame (coordinate system) of a widget,
    it doesn't make design sense that this is float,
    but that's what QPinchGesture does.
    '''
    self._centerPoint = QPointF(value)
    
  def setTotalRotationAngle(self, value):
    assert isinstance(value, float)
    self._totalRotationAngle = value
    
  def setTotalScaleFactor(self, value):
    assert isinstance(value, float)
    self._totalScaleFactor = value
    
    
    
    