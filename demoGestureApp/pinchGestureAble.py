
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QGraphicsView # demo

from qtGestureFramework.pinchGestureAdaptor import PinchGestureAdaptor
from qtGestureFramework.gestureable.gestureManager import gestureMgr  # singleton
from qtGestureFramework.gestureHandler.gestureHandler import GestureHandler


def isControlKeyDown():
  keyModifiers = QCoreApplication.instance().keyboardModifiers()
  return keyModifiers & Qt.ControlModifier
  
  
class PinchGestureHandler(GestureHandler):
  '''
  Mixin methods for an app.
  
  Methods for handling PinchGesture in various states.
  Gesture can be real QPinchGesture or qtGestureFramework.customGesture.PinchFromMouseGesture
  
  Change this to suit your application.
  Typically, a pinch changes viewing transform, crudely demonstrated below.
  
  Note we don't accept all state changes, but ignoring the start doesn't prevent future gesture events.
  So we use GestureManager to keep our own state.
  '''
  
  def __init__(self, view):
    assert isinstance(view, QGraphicsView)
    self.view = view
    
  
  def start(self, gesture):
    print('Start pinch')
    ## PinchGestureAdaptor.resetHotSpotBy(gesture)
    # Allow Ctl key to reject gestures
    if isControlKeyDown():
      return False
    else:
      gestureMgr.setGestureActive()
      return True #accepted
    
  
  def update(self, gesture):
    print('Update pinch')
    # Only if we accepted gesture start earlier
    if gestureMgr.isGestureActive():
      self._changeViewTransform(gesture)
      return True #accepted
    else:
      return False
    
  def finish(self, gesture):
    print('Finish pinch')
    gestureMgr.setGestureCanceledOrFinished()
    return True #accepted
  
  def cancel(self, gesture):
    print('Cancel pinch')
    gestureMgr.setGestureCanceledOrFinished()
    # Demo: restore view transform
    # TODO
    return True #accepted
  
  
  def _changeViewTransform(self, gesture):
    '''
    Demo: change view transform.
    '''
    scaleRatio = PinchGestureAdaptor.deltaScaleFactor(gesture)
    
    print("Scaling view", scaleRatio)
    self.view.scale(scaleRatio, scaleRatio)
    
    center = PinchGestureAdaptor.deltaCenterPoint(gesture)
    self.view.translate(center.x(), center.y())
