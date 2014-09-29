

from qtGestureFramework.gestureHandler.gestureHandler import GestureHandler


class LoggingStartGestureHandler(GestureHandler):
  '''
  Override GestureHandler to print only the start of a gesture.
  
  Ignores every gesture state change, but logs start so you know gesture is being ignored.
  '''
  
  def start(self, gesture):
    self._logGestureStateChange(gesture, state="Start")
    return False
  
  '''
  Other methods are inherited.
  '''
    