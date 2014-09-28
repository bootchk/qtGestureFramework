

from qtGestureFramework.gestureHandler.gestureHandler import GestureHandler


class LoggingGestureHandler(GestureHandler):
  '''
  Override GestureHandler to print every state change.
  
  Useful for learning or debugging.
  
  Accepts every gesture state change (never ignores.)
  '''
  
  def start(self, gesture):
    self._logGestureStateChange("Start", gesture)
    return True
  
  def update(self, gesture):
    self._logGestureStateChange("Update", gesture)
    return True
  
  def finish(self, gesture):
    self._logGestureStateChange("End", gesture)
    return True
  
  def cancel(self, gesture):
    self._logGestureStateChange("Cancel", gesture)
    return True
  
  

  def _logGestureStateChange(self, gesture, state):
    print(state, " gesture: ", gesture.type())
    