# NOT WORKING, crashes
class GestureSimulator(object):
  '''
  Mixin class e.g. for QGraphicsView.
  
  Simulate gestures by mouse with button down.
  
  Specifically: a QPinchGesture when any mouse button is down.
  
  The rotation, scale, and position of the simulated gesture
  derive from the starting mouse button press and current position.
  
  '''
  def startGestureSimulation(self):
    self.simulatedGesture = None
    
  def mouseMoveEvent(self, event):
      print("mouseMoveEvent")
      if self.simulatedGesture:
        self.updateSimulatedGesture(event)
      
  def mousePressEvent(self, event):
    print("mousePressEvent")
    self.createSimulatedGesture()
  
  def mouseRelease(self, event):
    self.isSimulatedGesture = None
    
  
  def createSimulatedGesture(self):
    self.simulatedGesture = QPinchGesture() # also tried (parent=self, state = Qt.GestureStarted)
    self.simulatedGesture.pyqtConfigure(state=1)
    # !!! state does not default to a valid value
    #self.simulatedGesture.state = Qt.GestureStarted
    self.postSimulatedGesture()
    
    
  def updateSimulatedGesture(self, mouseEvent):
    self.simulatedGesture
    self.postSimulatedGesture()
    
    
  def postSimulatedGesture(self):
    # event is a list of gestures
    event = QGestureEvent([self.simulatedGesture,])
    # post gesture event to main window
    QCoreApplication.instance().postEvent(self.parent(), event)
  
