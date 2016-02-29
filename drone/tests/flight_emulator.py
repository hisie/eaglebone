# -*- coding: utf-8 -*-
'''
Created on 25 de feb. de 2016

@author: david
'''

from emulation.state import State
from emulation.ui.graphic import Display


class StateProvider(object):
    
    def __init__(self):
        
        self._state = State()
        self._state._coords[2] = 5.0
        self._state._angles = [5.0]*3
    
    def getState(self):
    
        #self._state._coords[2] += 1.0
        #self._state._coords[0] += 1.0
        #self._state._angles[0] += 1.0
        #self._state._angles[1] -= 1.0
        #self._state._angles[2] += 1.0
        
        return self._state
    

def main():

    display = Display.getInstance().setStateProvider(StateProvider())
    display.start()


if __name__ == '__main__':
    
    main()
