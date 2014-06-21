#!/usr/bin/env python

from distutils.core import setup

setup(name='qtGestureFramework',
      version='1.0.0',
      description='Classes supporting Qt gestures',
      author='Lloyd Konneker',
      author_email='bootch@nc.rr.com',
      url='https://github.com/bootchk/qtGestureFramework',
      packages=['qtGestureFramework',
                'qtGestureFramework.gestureable',
                'qtGestureFramework.customGesture',
                'demoApp',
                ],
     )
