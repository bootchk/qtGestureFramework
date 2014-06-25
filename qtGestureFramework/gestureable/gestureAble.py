

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGestureRecognizer

from qtGestureFramework.gestureable.gestureManager import gestureMgr


class GestureAble(object):
  '''
  Mixin class for QGraphicsView
  
  Subscribing registers handlers for individual gestures (not QGestureEvents).
  !!! Handlers return False to ignore a gesture,
  especially when the gesture is in the started state.
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
  

  def subscribeBuiltinGesture(self, 
                              subscribingWidget,
                              gestureType,
                              startHandler,
                              updateHandler,
                              finishHandler,
                              cancelHandler):
    '''
    Subscribe the subscribingWidget to gesture type built into Qt (valid across platforms, but not necessarily implemented on all platforms.)
    
    subscribingWidget may be self, or a child (i.e. the viewport of a QGraphicsView.)
    '''
    assert GestureAble.isGestureTypeBuiltin(gestureType)
    
    # Qt built-in gestures use touch events, must enable them on widget
    # Qt built-in widgets DO NOT use mouse events
    self._subscribeTouchEvents(subscribingWidget)
    
    subscribingWidget.grabGesture(gestureType)  # method of QWidget or QGraphicsObject
    
    self._registerGestureSubscription(gestureType, startHandler, updateHandler, finishHandler, cancelHandler)
    # assert this widget will receive touch events and gestureType is grabbed

  
  def subscribeCustomGesture(self, 
                             subscribingWidget,
                             recognizerFactory,
                             startHandler=None,
                             updateHandler=None,
                             finishHandler=None,
                             cancelHandler=None):
    
    # Assume Widget subscribes to events that are input to custom recognizer
    gestureTypeID = self._grabCustomGesture(subscribingWidget, recognizerFactory)
    self._registerGestureSubscription(gestureTypeID, startHandler, updateHandler, finishHandler, cancelHandler)
    
    
  def _registerGestureSubscription(self, 
                              gestureType,
                              startHandler,
                              updateHandler,
                              finishHandler,
                              cancelHandler):
    '''
    Remember handlers by gestureStates for this subscription.
    '''
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
    
  
  def _subscribeTouchEvents(self, subscribingWidget):
    '''
    Boilerplate to subscribe to touch events, needed for built-in Qt gestures.
    '''
    # Tell Qt to deliver touch events instead of default, which is translating to mouse events (friendly)
    self.setAttribute(Qt.WA_AcceptTouchEvents)
    
    # !!! Obscure: set the attribute on child receiving events, e.g. viewport()
    subscribingWidget.setAttribute(Qt.WA_AcceptTouchEvents)
    
    
  def _grabCustomGesture(self, subscribingWidget, recognizerFactory):
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
    subscribingWidget.grabGesture(gestureTypeID)
    
    return gestureTypeID
    
    '''
    !!! Note that we don't keep a reference to recognizer, since now Qt owns it ???
    '''

  def monitorGestureEvent(self, event):
    '''
    If event has any signficance to gestures, handle it.
    
    - events whose type is well known to be gesture related
    - events that ARE subtly gesture related, but you wouldn't know it from their type.
    '''
    if GestureAble.isEventGestureRelated(event):
      self._dispatchGestureEventByState(event)
      # dispatchGestureEventByState does not ignore events, only individual gestures inside the event
      # if this is a gesture event, it is still accepted.
      # TODO will it still propagate to parent widgets?
      
    
    #Watch for start of a PinchGesture in the form of a QWheelEvent of phase BeginScroll
    gestureMgr.monitorEventForGesture(event)
    
    '''
    Assert that if event is QGestureEvent, it is accepted unless
    a gesture inside is in the start state and a handler ignored the gesture (rejected future events for the gesture.)
    '''
    
    
  def _dispatchGestureEventByState(self, event):
    '''
    This understands how to get gestures and their state out of a QGestureEvent
    
    Raises KeyError if get gestures not subscribed to.
    How would Qt let that happen?
    '''
    assert GestureAble.isEventGestureRelated(event)
    
    '''
    Temporary hack.
    MacOS is raising attribute error on QEvent of type GestureOverride.
    I found that GestureOverride comes e.g. when you subscribe gestures on a view instead of its viewport.
    That is, when gestures are made in a child of a subscriber.
    If you want that, you should properly design how to handle GestureOverride.
    This might not be a correct design.
    '''
    if event.type() == QEvent.GestureOverride:
      print("Accepting gesture override event.")
      event.accept()
      return
    
    assert event.type() == QEvent.Gesture
    activeGestures = event.activeGestures()
    for gesture in activeGestures:
      self._dispatchGestureByState(event, gesture)
      if self._gestureIsIgnoredStart(gesture):
        '''
        To properly ignore a gesture in start state, (so your app does not receive future events for gesture)
        the owning gesture eventy must also be ignored.
        Other gestures in the gestureEvent may be starting and not ignored.
        '''
        print("Ignoring gestureEvent having ignored gesture in start state")
        event.ignore()

    canceledGestures = event.canceledGestures()
    for gesture in canceledGestures:
      self._dispatchGestureByState(event, gesture)
      print('Cancel gesture')
      
    '''
    Handlers accept individual gestures inside event, and not the event itself.
    Handlers may ignore individual gestures inside gesture events (gestures that they are not subscribed)
    but they do not ignore the gesture event itself.
    
    It is not true stmt that (subtype is Gesture => accepted) and (subtype is GestureOverride => ignored)
    # assert (not event.isAccepted() or event.type() == QEvent.Gesture) and (event.isAccepted() or event.type() == QEvent.GestureOverride)
    
    I don't think Qt alters gestureEvent.accepted when its gestures are accepted.
    '''
  
  def _gestureIsIgnoredStart(self, gesture):
    '''
    Return True if gesture is in started state and was ignored.
    '''
    return gesture.state() == Qt.GestureStarted and not gesture.isAccepted()

  
  
  def _dispatchGestureByState(self, event, gesture):
    '''
    This understands our our internal dictionary of handlers for states.
    
    !!! This does NOT return a value indicating acceptance of any individual gesture.
    Handlers may (and should) accept or ignore individual gesture in particular life-states,
    but that is an acceptance-state of the individual gesture, and not returned here.
    
    However, a quirk of Qt is that a QGesture has no method setAccepted.
    Only a QGestureEvent.accept(QGesture) exists to accept and individual gesture,
    I suppose because the event wants involved so it can cache state of gestures?
    '''
    handlerSet = GestureAble.subscribedGestures[gesture.gestureType()]
    handler = handlerSet[gesture.state()]
    if handler is not None:
      # call handler
      handlerAccepted = handler(gesture)
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
      handlerAccepted = False
      
    '''
    Tell event to accept or ignore gesture.
    That is, a handler only returns an acceptance value, and doesn't know how to set it on the gesture.
    This method knows how to set acceptance on a gesture.
    
    By default, gestures are accepted, so setAccepted( , True) is superfluous, but do it the simple way.
    
    !!! This is NOT the acceptance of the QGestureEvent.
    See the caller, _dispatchGestureEventByState.
    '''
    event.setAccepted(gesture, handlerAccepted)
    if not handlerAccepted:
      print("handler ignored gesture")
      
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
    
    
