#! /usr/bin/python3

'''
Test custom gesture.
'''

import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsTextItem, QGraphicsView

from qtGestureFramework.gestureAble import GestureAble
from qtGestureFramework.eventDumper import eventDumper  # singleton



class DiagramScene(QGraphicsScene):
  def __init__(self, *args):
    QGraphicsScene.__init__(self, *args)
    text = QGraphicsTextItem("My events on item not triggered if mouse button pressed")
    text.setTextInteractionFlags(Qt.TextEditorInteraction)
    self.addItem(text)
    
  
  """
  def event(self, event):
    eventDumper.dump(event, "Scene")
    return super().event(event)
  """
    
    
class DiagramView(GestureAble, QGraphicsView):
  def __init__(self, *args):
    super().__init__(*args)
    self.setAttribute(Qt.WA_AcceptTouchEvents)
    # !!! Obscure: set the attribute on viewport()
    self.viewport().setAttribute(Qt.WA_AcceptTouchEvents)
    self.subscribeGestures()
    #self.grabGesture(Qt.PanGesture)
    # self.startGestureSimulation()
  
  
  def viewportEvent(self, event):
    eventDumper.dump(event, "View")
    return super().viewportEvent(event)
  
  



class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.scene = DiagramScene()
        self.view = DiagramView(self.scene)
        #self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        #self.subscribeGestures()
        self.setWindowTitle("Gesture example");
      
    def event(self, event):
      #eventDumper.dump(event, "Window")
      
      eventType = event.type()
      
      # dump touch events
      if eventType in (QEvent.TouchBegin, QEvent.TouchUpdate, QEvent.TouchEnd, QEvent.TouchCancel):
        eventDumper.dump(event, "Window.event")
        event.accept()
      
      # dump gesture events
      if eventType in (QEvent.Gesture, ):
        eventDumper.dumpGestureEvent(event)
        event.accept()
        
      
      # TODO accept?  super ? eventFilter ?
      
      #return QMainWindow.event(self, event)
      return True # meaning: did process
    
         
    def touchEvent(self, event):
      " Reimplemented to dump "
      eventDumper.dump(event, "Window.touchEvent")
         

      

def main(args):
    app = QApplication(args)
    #app = QApplication(['testgesture', '-plugin evdevtouch:/dev/input/wacom-touch',])  # args in a list of strings
    #app = QApplication(['testgesture', '-plugin qevdevtouchplugin'])
    # -plugin evdevtouch:/dev/input/event[i
    
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 500, 400)
    mainWindow.show()
    
    
    """
    ''' Without MainWindow. '''
    scene = DiagramScene()
    view = DiagramView(scene)
    view.showMaximized()
    view.fitInView(scene.sceneRect().adjusted(-20, -20, 20, 20), Qt.KeepAspectRatio)
    """
    
    # Qt Main loop
    sys.exit(app.exec_())

"""
Linux stuff

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