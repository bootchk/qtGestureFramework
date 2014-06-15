
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer

from qtGestureFramework.customGesture.pinchFromMouseGesture import PinchFromMouseGesture

from qtGestureFramework.eventDumper import eventDumper


class PinchFromMouseRecognizer(QGestureRecognizer):
  '''
  Simulates a QPinchGesture, but reads mouse events.
  In a primitive way, see below.
  '''
  
  def __init__(self):
    print("Init MyGestureRecognizer")
    self.isRecognizing = False  # internal state
    super().__init__()
    
  
  
  def recognize(self, gesture, watched, event):
    '''
    Reimplement ( Qt requires )
    
    Note we use middle mouse button for gestures,
    and other mouse buttons can still be used in your app.
    '''
    
    result = QGestureRecognizer.Ignore  # default result
    if event.type() == QEvent.MouseButtonPress and event.button() == Qt.MiddleButton:
      self.isRecognizing = True
      self.startPos = event.pos()   # copy ?
      result = QGestureRecognizer.MayBeGesture
    elif event.type() == QEvent.MouseMove and self.isRecognizing:
      result = self._updateGesture(gesture, event)
      # result is Triggered or Maybe: not canceled until mouseButtonRelease
    elif event.type() == QEvent.MouseButtonRelease and self.isRecognizing:
      result = self.finalGestureResult(gesture, event)
      self.isRecognizing = False
      
    # The result is a single flag
    assert result in (QGestureRecognizer.FinishGesture, 
                      QGestureRecognizer.MayBeGesture, 
                      QGestureRecognizer.Ignore,
                      QGestureRecognizer.CancelGesture,
                      QGestureRecognizer.TriggerGesture,
                      )
    print("Recognize result {}".format(eventDumper.gestureRecognizerResultFlagMap[result]))
    
    # Consume input event, so it doesn't propagate to other event handlers
    # result = result | QGestureRecognizer.ConsumeEventHint
    
    return result # 
  
  
  
  def create(self, targetWidgetOrQGraphicsObj):
    '''
    Called by recognizer to create custom gesture.
    Optional to reimplement: only if gesture type is specialized subclass of QGesture.
    '''
    gesture = PinchFromMouseGesture(parent=targetWidgetOrQGraphicsObj) # MyGesture(parent=targetWidgetOrQGraphicsObj)
    print("create", gesture)
    # gesture is owned by Qt
    return gesture
  
  
  def reset(self, gesture):
    '''
    Reimplement
    '''
    print("Gesture reset")
    self.isRecognizing = False
    super().reset(gesture)


  def _updateGesture(self, gesture, event):
    '''
    State machine for gesture.
    
    In a minimal way:
    - mouse button press is start of state machine
    - changes to begun (triggered) state with a little movement
    - changes to state canceled if mouse button release without enough movement
    - changes to finished state with mouse button release and enough movement
    (That is, you really don't make a shape, just the distance moved determines state.)
    '''
    assert event.type() == QEvent.MouseMove
    assert gesture.gestureType() == 257
    # assert mouse button was pressed recently (and probably still down.)
    if self._manhattanDistanceToOrigin(event.pos()) > 3:
      result = QGestureRecognizer.TriggerGesture
    else:
      result = QGestureRecognizer.MayBeGesture
    
    '''
    update gesture properties only if triggered?
    It could still be canceled, so if client is using properties to change app,
    client must be ready to rollback.
    '''
    self.updateGestureProperties(gesture, event)
    
    assert result in (QGestureRecognizer.TriggerGesture, QGestureRecognizer.MayBeGesture)
    return result
  
  
  def finalGestureResult(self, gesture, event):
    '''
    This knows that for emulation, a short mouse move means cancel
    while a long one means finish.
    '''
    assert self.isRecognizing
    if self._manhattanDistanceToOrigin(event.pos()) < 20 :
      result = QGestureRecognizer.CancelGesture
    else:
      result = QGestureRecognizer.FinishGesture
    return result
  
  
  def updateGestureProperties(self, gesture, event):
    '''
    fabricated in a simple way: always in relation to current pos and starting pos.
    '''
    gesture.setCenterPoint(event.pos())
    
    # !!! TODO, the real angle of mouse vector
    gesture.setTotalRotationAngle(0.0)
    
    scaleFactor = self._manhattanDistanceToOrigin(event.pos()) / 20.0
    assert scaleFactor > 0 and scaleFactor < 1000
    gesture.setTotalScaleFactor(scaleFactor)
      

  
  def _manhattanDistanceToOrigin(self, pos1):
    '''
    Simple measure of distance between two points in same frame.
    '''
    pos2 = self.startPos
    result = abs(pos1.x() - pos2.x()) + abs(pos1.y() - pos2.y())
    assert result > 0
    return result