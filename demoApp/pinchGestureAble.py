
from PyQt5.QtWidgets import QGraphicsView # demo

from qtGestureFramework.pinchGestureAdaptor import PinchGestureAdaptor
from qtGestureFramework.gestureable.gestureManager import gestureMgr  # singleton

class PinchGestureAble(object):
  '''
  Mixin methods for an app.
  
  Methods for handling PinchGesture in various states.
  Gesture can be real QPinchGesture or qtGestureFramework.customGesture.PinchFromMouseGesture
  
  Change this to suit your application.
  Typically, a pinch changes viewing transform, crudely demonstrated below.
  
  Here we accept all state changes.
  '''
  
  def handlePinchStart(self, gesture):
    print('Start pinch')
    PinchGestureAdaptor.resetHotSpotBy(gesture)
    gestureMgr.setGestureActive()
    return True #accepted
    
  
  def handlePinchUpdate(self, gesture):
    print('Update pinch')
    
    '''
    Demo: change view transform.
    '''
    scaleRatio = PinchGestureAdaptor.deltaScaleFactor(gesture)
    assert isinstance(self, QGraphicsView)
    print("Scaling view", scaleRatio)
    self.scale(scaleRatio, scaleRatio)
    
    center = PinchGestureAdaptor.deltaCenterPoint(gesture)
    self.translate(center.x(), center.y())
    
    return True #accepted
    
  def handlePinchFinish(self, gesture):
    print('Finish pinch')
    gestureMgr.setGestureCanceledOrFinished()
    return True #accepted
  
  def handlePinchCancel(self, gesture):
    print('Cancel pinch')
    gestureMgr.setGestureCanceledOrFinished()
    # Demo: restore view transform
    # TODO
    
    return True #accepted
