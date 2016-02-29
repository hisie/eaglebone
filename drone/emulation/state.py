# -*- coding: utf-8 -*-

'''
Created on 03/02/2016

@author: david
'''

class State(object):
    '''
    State of a drone at a time

    IMU's positive angles are counter clockwise (CCW)
    '''

    def __init__(self):

        self._time = None
        self._crashed = False
        self._coords = [0.0]*3
        self._accels = [0.0]*3
        self._speeds = [0.0]*3        
        self._angleSpeeds = [0.0]*3
        self._angles = [0.0]*3
        
        
    def __str__(self):
        
        if not self._crashed:
            coords = "C({0:.3f}, {1:.3f}, {2:.3f})".format(self._coords[0],self._coords[1],self._coords[2])
            speed = "S({0:.3f}, {1:.3f}, {2:.3f})".format(self._speeds[0],self._speeds[1],self._speeds[2])
            accel = "Ac({0:.3f}, {1:.3f}, {2:.3f})".format(self._accels[0],self._accels[1],self._accels[2])            
            angles = "An({0:.3f}, {1:.3f}, {2:.3f}, {3:.3f})".format(self._angles[0],self._angles[1],self._angles[2],self._angleSpeeds[2])
            
            string = "{0}-{1}-{2}-{3}".format(coords, speed, angles, accel)
        else:
            string = "CRASHED!!!"
        
        return string

