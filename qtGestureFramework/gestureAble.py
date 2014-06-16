

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer


class GestureAble(object):
  '''
  Mixin class for QGraphicsView
  '''
  subscribedGestures = {}
  
  
  @classmethod
  def isEventGestureRelated(self, event):
    '''
    Does event contain gestures?
    
    The Qt documentation is obscure re event having type() == GestureOverride.
    The class of such and event is QGestureEvent,
    but the reported type() is one of two values
    '''
    return event.type() in (QEvent.Gesture, QEvent.GestureOverride)
  
  
  @classmethod
  def isGestureTypeBuiltin(cls, gestureType):
    # Not a custom gesture
    return gestureType in (Qt.TapGesture, Qt.TapAndHoldGesture, Qt.PanGesture, Qt.PinchGesture, Qt.SwipeGesture)
  

  def subscribeBuiltinGesture(self, gestureType,
                              startHandler,
                              updateHandler,
                              finishHandler,
                              cancelHandler):
    '''
    Subscribe to gesture type built into Qt (valid across platforms, but not necessarily implemented on all platforms.)
    '''
    assert GestureAble.isGestureTypeBuiltin(gestureType)
    
    # Qt built-in gestures use touch events, must enable them on widget
    # Qt built-in widgets DO NOT use mouse events
    self._subscribeTouchEvents()
    
    self.grabGesture(gestureType)  # method of QWidget or QGraphicsObject
    
    self._registerGestureSubscription(gestureType, startHandler, updateHandler, finishHandler, cancelHandler)
    # assert this widget will receive touch events and gestureType is grabbed

  
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
    # Create dictionary {gesture state: handler}
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
    ID is Qt.CustomGesture 0x100 plus 1, e.g. 257
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
    
    Raises KeyError if get gestures not subscribed to.
    How would Qt let that happen?
    '''
    assert GestureAble.isEventGestureRelated(event)
    
    activeGestures = event.activeGestures()
    for gesture in activeGestures:
      self._dispatchGestureByState(gesture)

    canceledGestures = event.canceledGestures()
    for gesture in canceledGestures:
      self._dispatchGestureByState(gesture)
      print('Cancel gesture')
      
    '''
    Handlers accept individual gestures inside event, and not the event itself.
    But an event isAccepted() by default.
    
    Handlers may ignore individual gestures inside gesture events (gestures that they are not subscribed)
    but they do not ignore the gesture event itself.
    '''
    assert event.isAccepted()
  
  
  def _dispatchGestureByState(self, gesture):
    '''
    This understands our our internal dictionary of handlers for states.
    
    !!! This does NOT return a value indicating acceptance of any individual gesture.
    Handlers may (and should) accept or ignore individual gesture in particular life-states,
    but that is an acceptance-state of the individual gesture, and not passed here.
    '''
    handlerSet = GestureAble.subscribedGestures[gesture.gestureType()]
    handler = handlerSet[gesture.state()]
    if handler is not None:
      # call handler
      handler(gesture)
    else:
      '''
      App programmer error.
      Should be a not None handler for every state.
      E.g. you designed gesture to be discrete (never in GestureUpdate state)
      but the gesture arrives in GestureUpdate state.
      '''
      print('No handler for gesture type {} in state {}'.format(gesture.gestureType(), gesture.state()))
      # TODO should we ignore the gesture so that this widget does not get it again?
      # Especially if it is in the GestureStart life-state?
      
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
    
    