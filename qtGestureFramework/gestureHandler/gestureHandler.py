


class GestureHandler(object):
  '''
  Handle state changes for a gesture.
  'state' includes attributes; we get multiple events with gesture in state:update, meaning attributes changed.
  I.e. our definition of state is not just gesture.state() but also gesture attributes.
  
  Base class.
  
  Certain other classes depend on this API.
  '''
  
  " No __init__, subclasses may override. "
  
  
  def start(self, gesture):
    '''
    Default is to ignore, so no further state changes should be received.
    '''
    return False
  
  '''
  If you ignore start, we should not receive further state changes.
  But we return False, which will cause qtPrintFramework to mark the gesture ignored again.
  '''
  def update(self, gesture):
    return False
  
  def finish(self, gesture):
    return False
  
  def cancel(self, gesture):
    return False
