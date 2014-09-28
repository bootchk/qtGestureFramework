
from PyQt5.QtCore import Qt, QEvent


class GestureManager(object):
  '''
  Know when a gesture is active.
  
  Glorified state, for an app that only subscribes to one gesture!!!
  (TODO make it count active gestures, when many can be active.)
  
  Especially fixes a quirk of Qt on OSX: determine when a scrolling gesture starts on OSX.
  
  !!! isGestureActive() == True does NOT mean the app has accepted the gesture.
  It only means that as best we can tell, the user is gesturing.
  '''
  
  def __init__(self):
    self._isGestureActive = False
  
  def isGestureActive(self):
    '''
    Is a physical gesture started, including a pseudo 'scroll' gesture on OSX.
    '''
    return self._isGestureActive
  
  
  def monitorEventForGesture(self, event):
    '''
    monitor events to more accurately detect the start of a 'scroll' physical gesture, which comes as a QWheelEvent.
    On OSX, a physical 2-finger pinch gesture also generates QWheelEvent (the scrolling component of the physical gesture)
    but often before a QGestureEvent having a QPinchGesture in the started state.
    So Qt is late in saying the gesture has started.
    
    This is called on every event (by GestureAble.monitorGestureEvent(), which your app should call on every event.)
    
    Implementation:
    A TouchBegin event reliably comes when a pinch gesture was started (with two fingers down.)
    But it also comes without a gesture !?! So it is not reliable.
    On OSX, a QWheelEvent having a phase of Qt.ScrollBegin reliably indicates that a two-finger gesture
    (that will later come as a QPinchGesture having only a scrolling component)
    is in fact a 'scroll' gesture.
    
    This doesn't monitor QGestureEvent.
    Your app should be handling those, and calling setGestureActive() when it accepts a gesture in the started state.
    
    This may be fragile: Qt or OSX may change.
    '''
    """
    OLD, not reliable.
    
    # class is QTouchEvent, type is QEvent.TouchBegin
    if event.type() == QEvent.TouchBegin:
      print("setGestureActive")
      self.setGestureActive()
    """
    # class is QWheelEvent, type is Wheel
    if event.type() == QEvent.Wheel and event.phase() == Qt.ScrollBegin :
      # assert this event comes from a touch gesture.  A QWheelEvent from a mouse does not have phases, even on OSX
      print("setGestureActive for scrolling gesture on touchpad")
      self.setGestureActive()
    
    
  def setGestureActive(self):
    '''
    Call this when your app receives a QGestureEvent having a gesture in the started state.
    '''
    self._isGestureActive = True
    
    
  def setGestureCanceledOrFinished(self):
    '''
    Call this when your app receives a QGestureEvent having a gesture in the finished or canceled state.
    '''
    self._isGestureActive = False
    
    
gestureMgr = GestureManager()