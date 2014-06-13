
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QGestureRecognizer, QGesture


class PinchFromMouseRecognizer(QGestureRecognizer):
  
  def __init__(self):
    print("Init MyGestureRecognizer")
    self.isGesture = False  # internal state
    super().__init__()
    
  
  
  def recognize(self, state, watched, event):
    '''
    Reimplement ( Qt requires )
    '''
    print("Recognize")
    result = QGestureRecognizer.Ignore
    if event.type() == QEvent.MouseButtonPress:
      self.isGesture = True
      self.startPos = event.pos()
      result = QGestureRecognizer.MayBeGesture
    elif event.type() == QEvent.MouseMove and self.isGesture:
      result = self._updateGesture(event)
      # maybe canceled
    elif event.type() == QEvent.MouseButtonRelease and self.isGesture:
      self.isGesture = False
      result = QGestureRecognizer.FinishGesture
    #print "recognize"
    return result # 
  
  
  # Optional to reimplement: only if gesture type is  custom
  def create(self, targetWidgetOrQGraphicsObj):
    '''
    Called at registerRecognizer() time.
    '''
    print("create")
    gesture = QGesture(parent=targetWidgetOrQGraphicsObj) # MyGesture(parent=targetWidgetOrQGraphicsObj)
    print(gesture)
    return gesture
  
  
  def reset(self, gesture):
    '''
    Reimplement
    '''
    print("reset")
    self.isGesture = False
    super().reset(gesture)

  def _updateGesture(self, event):
    # TODO change state based on distance
    
    return QGestureRecognizer.MayBeGesture
  
  