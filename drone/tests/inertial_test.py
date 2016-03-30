# -*- coding: utf-8 -*-
'''
Created on 9 de mar. de 2016

@author: david
'''

import rpyc
import time

from emulation.state import State
from emulation.ui.graphic import Display
from copy import deepcopy


class StateProvider(object):
    
    ACCEL_LPF = 0.001
    
    def __init__(self, address="192.168.1.130"):
        
        self._state = State()
        self._state._coords = [0.0, 0.0, 1.0]
        
        self._connection = rpyc.classic.connect(address)
        
        self._imu = self._connection.modules["sensors.imu6050dmp"].Imu6050Dmp()
        self._imu.start()
    

    def getState(self):
        
        self._imu.refreshState()
        
        '''
        currentTime = time.time()
        if self._state._time != None:

            dt2 = (currentTime - self._state._time)/2.0
        
            #self._state._crashed = False
            
            previousAccels = deepcopy(self._state._accels)
            previousSpeeds = deepcopy(self._state._speeds)
            
            rawAccels = self._imu.readAccels()
            for index in range(3):
                self._state._accels[index] = previousAccels[index] + \
                    StateProvider.ACCEL_LPF * (rawAccels[index] - previousAccels[index])
                    
                self._state._speeds[index] += (self._state._accels[index] + previousAccels[index])*dt2
                self._state._coords[index] += (self._state._speeds[index] + previousSpeeds[index])*dt2

            self._state._angleSpeeds = self._imu.readAngleSpeeds()
            self._state._angles = self._imu.readDeviceAngles()

        self._state._time = currentTime
        '''
        self._state._angles = self._imu.readDeviceAngles()
        
        return self._state
    
    
    def close(self):
        
        self._imu.stop()
        self._connection.close()
        

def main():

    provider = StateProvider()
    display = Display.getInstance().setStateProvider(provider).setRefreshTime(0.02)
    display.start()
    provider.close()


if __name__ == '__main__':
    
    main()
