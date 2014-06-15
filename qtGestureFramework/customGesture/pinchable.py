
from PyQt5.QtCore import QPointF, QPoint


class Pinchable(object):
  '''
  Mixin methods for a custom gesture, to emulate a two-finger QPinchGesture.
  In other words, gesture is pinchable, i.e. has API of QPinchGesture.
  
  Names match QPinchGesture.
  
  A subset, (omitting some methods) for:
  -rotation, 
  -center,
  -scale factor.

  See pinchGestureAdaptor for augmented methods for delta
  
  The recognizer also may be implementing a further subset or degradation (i.e. rotation always 0)
  '''
  
  '''
  Initial values.
  This method is not present in QPinchGesture, only needed for PinchGestureFromMouse.
  But values are the same as QPinchGesture returns in case there is no last.
  '''
  def initialize(self):
    self._centerPoint = self._lastCenterPoint = QPointF(0,0)
    self._totalRotationAngle = self._lastRotationAngleNone = 0.0
    self._totalScaleFactor = self._lastScaleFactor = 0.0
  
  '''
  Getters
  '''
  '''
  Total
  '''
  def centerPoint(self):
    return self._centerPoint
  
  def totalRotationAngle(self):
    return self._totalRotationAngle
  
  def totalScaleFactor(self):
    return self._totalScaleFactor
  
  '''
  Last
  '''
  
  def lastCenterPoint(self):
    return self._lastCenterPoint
  
  def lastRotationAngle(self):
    return self._lastRotationAngle
  
  def lastScaleFactor(self):
    return self._lastScaleFactor
  
  '''
  Current
  
  centerPoint() above is also the current center point (as well as the total center point)
  
  Omitted:
  -scaleFactor()
  -rotationAngle()
  
  These are wierd in QPinchGesture API.
  They usually are the same as total,
  but they allow for stages of the gesture, i.e. user lifting a finger during the physical gesture.
  '''
  
  
  '''
  Setters, called by recognizer.
  '''
  
  '''
  Total
  '''
  def setCenterPoint(self, value):
    assert isinstance(value, (QPointF, QPoint))
    '''
    Coerce to QPointF.
    Since all mouse events to the recognizer are QPoint in the frame (coordinate system) of a widget,
    it doesn't make design sense that this is float,
    but that's what QPinchGesture does.
    '''
    self._lastCenterPoint = self._centerPoint #roll
    self._centerPoint = QPointF(value)
    
  def setTotalRotationAngle(self, value):
    assert isinstance(value, float)
    self._lastRotationAngle = self._totalRotationAngle #roll
    self._totalRotationAngle = value
    
  def setTotalScaleFactor(self, value):
    assert isinstance(value, float)
    assert value > 0  # Used as divisor elsewhere
    self._lastScaleFactor = self._totalScaleFactor #roll
    self._totalScaleFactor = value
    
  '''
  Omitting setters for last (present in the real QPinchGesture.)
  '''
    
    
    