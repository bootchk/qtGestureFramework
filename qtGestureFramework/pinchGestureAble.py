
from PyQt5.QtWidgets import QGraphicsView # demo

from qtGestureFramework.pinchGestureAdaptor import PinchGestureAdaptor


class PinchGestureAble(object):
  '''
  Mixin methods for an app.
  
  Methods for handling PinchGesture in various states.
  Gesture can be real QPinchGesture or qtGestureFramework.customGesture.PinchFromMouseGesture
  
  Change this to suit your application.
  Typically, a pinch changes viewing transform, crudely demonstrated below.
  '''
  
  def handlePinchStart(self, gesture):
    print('Start pinch')
    
  
  def handlePinchUpdate(self, gesture):
    print('Update pinch')
    
    '''
    For demonstration, change viewing transform.
    '''
    scaleRatio = PinchGestureAdaptor.deltaScaleFactor(gesture)
    assert isinstance(self, QGraphicsView)
    print("Scaling view", scaleRatio)
    self.scale(scaleRatio, scaleRatio)
    
    center = PinchGestureAdaptor.deltaCenterPoint(gesture)
    self.translate(center.x(), center.y())
    
    
  def handlePinchFinish(self, gesture):
    print('Finish pinch')
  
  def handlePinchCancel(self, gesture):
    print('Cancel pinch')
