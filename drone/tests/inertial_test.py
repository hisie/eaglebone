# -*- coding: utf-8 -*-
'''
Created on 9 de mar. de 2016

@author: david
'''

import rpyc
import time

from emulation.state import State
from emulation.ui.graphic import Display


class StateProvider(object):
    
    def __init__(self):
        
        self._state = State()
        self._state._coords = [0.0, 0.0, 1.0]
        
        self._connection = rpyc.classic.connect("192.168.1.130")
        
        self._imu = self._connection.modules["sensors.imu6050dmp"].Imu6050Dmp()
        self._imu.start()
    

    def getState(self):
        
        self._imu.refreshState()
        
        #self._state._time = time.time()
        
        #self._state._crashed = False
        #self._state._coords = [0.0]*3
        self._state._accels = self._imu.readAccels()
        #self._state._speeds = [0.0]*3        
        self._state._angleSpeeds = self._imu.readAngleSpeeds()
        self._state._angles = self._imu.readDeviceAngles()
        
        return self._state
    
    
    def close(self):
        
        self._imu.stop()
        self._connection.close()
        

def main():

    provider = StateProvider()
    display = Display.getInstance().setStateProvider(provider)
    display.start()
    provider.close()


if __name__ == '__main__':
    
    main()
