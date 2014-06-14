

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer

from qtGestureFramework.customGesture.pinchFromMouseRecognizer import PinchFromMouseRecognizer


class GestureAble(object):
  '''
  Mixin class for QGraphicsView
  '''
  # grabbedGestureIDSet = []
  
  def subscribeGestures(self):
    '''
    Boilerplate to subscribe to Qt gestures.
    '''
    # Tell Qt to deliver touch events instead of default, which is translating to mouse events (friendly)
    self.setAttribute(Qt.WA_AcceptTouchEvents)
    
    # !!! Obscure: set the attribute on viewport()
    self.viewport().setAttribute(Qt.WA_AcceptTouchEvents)
    
    self.grabGestureSet()


  def unsubscribeGestures(self):
    '''
    Not sure this is necessary.
    It might prevent crash on exit.
    '''
    print("unsubscribeGestures")
    QGestureRecognizer.unregisterRecognizer(257)
    
    

  def grabGestureSet(self):
    '''
    Defines gestures relevant to this app.
    
    !!! For simulation, grab same gesture type as simulator is emitting (pinch)
    '''
    print("grabGestureSet")
    self.grabCustomGesture(PinchFromMouseRecognizer)
    
    
  def grabCustomGesture(self, recognizerFactory):
    '''
    Create instance of gesture recognizer,
    register it,
    and subscribe self to custom gesture of recognizer.
    '''
    myRecognizer = recognizerFactory()
    
    # Call class method to let app take ownership of recognizer
    gestureTypeID = QGestureRecognizer.registerRecognizer(myRecognizer)
    '''
    ID is Qt::CustomGesture 0x100 plus 1, e.g. 257
    '''
    #print("gesture type id is ", gestureTypeID)
    
    print("{} grabbing gesture type {}".format(self, gestureTypeID))
    self.grabGesture(gestureTypeID)
    
    '''
    !!! Note that we don't keep a reference to recognizer, since now Qt owns it ???
    '''


  def processGestures(self, event):
    if event.type() == QEvent.Gesture:
      pass