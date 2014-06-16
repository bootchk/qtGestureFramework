#! /usr/bin/python3

'''
Test qtGestureFramework
'''

import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsTextItem, QGraphicsView

from qtGestureFramework.gestureAble import GestureAble
from qtGestureFramework.pinchGestureAble import PinchGestureAble
from qtGestureFramework.eventDumper import eventDumper  # singleton
from qtGestureFramework.customGesture.pinchFromMouseRecognizer import PinchFromMouseRecognizer



class DiagramScene(QGraphicsScene):
  def __init__(self, parent):
    QGraphicsScene.__init__(self, parent)
    text = QGraphicsTextItem("Simulate pinch with middle mouse button pressed")
    #text.setTextInteractionFlags(Qt.TextEditorInteraction)
    self.addItem(text)
  
  """
  def event(self, event):
    eventDumper.dump(event, "Scene")
    return super().event(event)
  """
    
    
class DiagramView(GestureAble, PinchGestureAble, QGraphicsView):
  def __init__(self, scene, parent):
    super().__init__(scene, parent)
    
    '''
    Here we subscribe to both the builtin pinch gesture and a custom pinch gesture simulated with mouse.
    If you don't have a touch device, you won't get touch events and thus not the built-in one.
    If you do have a touch device, this might not work,
    since touch events not handled are translated by Qt into mouse events,
    and you might have multiple pinch gestures active,
    calling the same handlers.
    '''
    self.subscribeBuiltinGesture(Qt.PinchGesture, startHandler=self.handlePinchStart,
                                updateHandler=self.handlePinchUpdate,
                                finishHandler=self.handlePinchFinish,
                                cancelHandler=self.handlePinchCancel)
    
    self.subscribeCustomGesture(PinchFromMouseRecognizer,
                                startHandler=self.handlePinchStart,
                                updateHandler=self.handlePinchUpdate,
                                finishHandler=self.handlePinchFinish,
                                cancelHandler=self.handlePinchCancel)

  
  def event(self, event):
    eventDumper.dump(event, "View")
    
    if GestureAble.isEventGestureRelated(event):
      self.dispatchGestureEventByState(event)
      # dispatchGestureEventByState does not ignore events, only individual gestures inside the event
      # if this is a gesture event, it is still accepted.
      # TODO will it still propagate to parent widgets?
      
    return super().event(event)
  
  
  def viewportEvent(self, event):
    '''
    viewport is area inside scrollbars?
    '''
    eventDumper.dump(event, "Viewport")
    return super().viewportEvent(event)
  
  
    


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        scene = DiagramScene(parent=self) # !!! parent is important for clean exit
        self.view = DiagramView(scene=scene, parent=self)
        self.setCentralWidget(self.view)
        self.setWindowTitle("Gesture example");
        
        '''
        MainWindow does not subscribe gestures,
        since then user could make gestures in other children such as menubar and statusbar
        '''
      
    def event(self, event):
      #eventDumper.dump(event, "Window")
      
      eventType = event.type()
      
      # dump touch events
      if eventType in (QEvent.Gesture, QEvent.TouchBegin, QEvent.TouchUpdate, QEvent.TouchEnd, QEvent.TouchCancel):
        eventDumper.dump(event, "Window.event")
      
      # Call super, so propagate to children
      return super().event(event)
    
         
    def touchEvent(self, event):
      " Reimplemented to dump "
      eventDumper.dump(event, "Window.touchEvent")
      super().touchEvent(event)
      

def main(args):
    app = QApplication(args)
    #app = QApplication(['testgesture', '-plugin evdevtouch:/dev/input/wacom-touch',])  # args in a list of strings
    #app = QApplication(['testgesture', '-plugin qevdevtouchplugin'])
    # -plugin evdevtouch:/dev/input/event[i
    
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 500, 400)
    app.setActiveWindow(mainWindow)  # necessary for clean exit?
    mainWindow.show()
    
    # Qt Main loop
    sys.exit(app.exec_())

"""
Linux stuff for using certain touch devices

def loadEvdevPlugin():
  #plugin = QPluginLoader("libqevdevtouchplugin.so")
  #plugin = QPluginLoader("qevdevtouchplugin")
  plugin = QPluginLoader("evdevtouchplugin")
  result = plugin.load()
  if not result:
    print("PLUGIN LOAD FAIL")
"""

if __name__ == "__main__":
    main(sys.argv)