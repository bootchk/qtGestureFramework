

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer


class GestureAble(object):
  '''
  Mixin class for QGraphicsView
  '''
  subscribedGestures = {}
  

  def subscribeBuiltinGesture(self, gestureType,
                              startHandler,
                              updateHandler,
                              finishHandler,
                              cancelHandler):
    self._subscribeTouchEvents()
    # assert gestureType in ...
    self.grabGesture(gestureType)  # method of QWidget or QGraphicsObject
    self._registerGestureSubscription(gestureType, startHandler, updateHandler, finishHandler, cancelHandler)

  
  def subscribeCustomGesture(self, recognizerFactory,
                              startHandler=None,
                              updateHandler=None,
                              finishHandler=None,
                              cancelHandler=None):
    
    # Assume Widget subscribes to events that are input to custom recognizer
    gestureTypeID = self._grabCustomGesture(recognizerFactory)
    self._registerGestureSubscription(gestureTypeID, startHandler, updateHandler, finishHandler, cancelHandler)
    
    
  def _registerGestureSubscription(self, gestureType,
                              startHandler,
                              updateHandler,
                              finishHandler,
                              cancelHandler):
    # Create dictionary key is gesture state, value is handler
    gestureHandlerDictionary = {Qt.GestureStarted : startHandler,
                         Qt.GestureUpdated : updateHandler,
                         Qt.GestureFinished : finishHandler,
                         Qt.GestureCanceled : cancelHandler }
    
    GestureAble.subscribedGestures[gestureType] = gestureHandlerDictionary 
    

  def unsubscribeGestures(self):
    '''
    Not sure this is necessary.
    It might prevent crash on exit.
    '''
    print("unsubscribeGestures")
    # TODO more general, iterate over subscribed
    QGestureRecognizer.unregisterRecognizer(257)
    
  
  def _subscribeTouchEvents(self):
    '''
    Boilerplate to subscribe to touch events, needed for built-in Qt gestures.
    '''
    # Tell Qt to deliver touch events instead of default, which is translating to mouse events (friendly)
    self.setAttribute(Qt.WA_AcceptTouchEvents)
    
    # !!! Obscure: set the attribute on viewport()
    self.viewport().setAttribute(Qt.WA_AcceptTouchEvents)
    
    
  def _grabCustomGesture(self, recognizerFactory):
    '''
    Create instance of gesture recognizer,
    register it,
    and subscribe self to custom gesture of recognizer.
    Return gestureTypeID
    
    This assumes app gets events that are input to the recognizer
    (e.g. mouse events for recognizer that uses mouse events.)
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
    
    return gestureTypeID
    
    '''
    !!! Note that we don't keep a reference to recognizer, since now Qt owns it ???
    '''


  def dispatchGestureEventByState(self, event):
    '''
    This understands how to get gestures and their state out of a QGestureEvent
    '''
    if event.type() == QEvent.Gesture:
      # Should not be getting gestures not subscribed.  KeyError if we do.
      
      activeGestures = event.activeGestures()
      for gesture in activeGestures:
        self._dispatchGestureByState(gesture)

      canceledGestures = event.canceledGestures()
      for gesture in canceledGestures:
        self._dispatchGestureByState(gesture)
        print('Cancel gesture')
  
  
  def _dispatchGestureByState(self, gesture):
    '''
    This understands our our internal dictionary of handlers for states.
    '''
    handlerSet = GestureAble.subscribedGestures[gesture.gestureType()]
    handler = handlerSet[gesture.state()]
    if handler is not None:
      # call handler
      handler(gesture)
    else:
      print('No handler for gesture type {} in state {}'.format(gesture.gestureType(), gesture.state()))
      
    """
      if gesture.state() == Qt.GestureStarted:
        print('Starting gesture')
      elif gesture.state() == Qt.GestureUpdated:
        print('Update gesture')
      elif gesture.state() == Qt.GestureFinished:
        print('Finish gesture')
    """
    
  def checkGestureIsSubscribed(self, gesture):
    if not gesture.gestureType() in GestureAble.subscribedGestures:
      raise RuntimeError("Can't dispatch unsubscribed gesture")
    
    