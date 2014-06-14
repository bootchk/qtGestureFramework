


class PinchGestureAble(object):
  '''
  Mixin methods for an app.
  
  Methods for handling PinchGesture in various states.
  
  Change this to suit your application.
  Typically, a pinch changes viewing transform.
  '''
  
  def handlePinchStart(self, gesture):
    print('Start pinch')
  
  def handlePinchUpdate(self, gesture):
    print('Update pinch')
    
  def handlePinchFinish(self, gesture):
    print('Finish pinch')
  
  def handlePinchCancel(self, gesture):
    print('Cancel pinch')
