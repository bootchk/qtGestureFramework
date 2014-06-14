qtGestureFramework
==================

Copyright 2014 Lloyd Konneker
Licensed GPLv3

Classes supporting gestures for Python3, PyQt5

Useful for learning, experimentation, testing when you don't actually have a trackpad or touchscreen.

Includes
========

The main class GestureAble, a mixin for QGraphicsView that hides the details of subscribing to gestures and handling gesture events.

A custom gesture and recognizer simulating a two-finger pinch from the mouse.
The pinch gesture is important to recognize since many laptop trackpads recognize it.
Apple HIG suggest that your app handle it: users expect it to work in all apps.

A simple app/test program that uses framework

Other classes such as EventDumper






