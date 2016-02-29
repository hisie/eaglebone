'''
Created on 28/02/2016

@author: david
'''
from emulation.ui.graphic import Display
from emulation.drone import EmulatedDrone
import remote_control.start as RemoteControl 

def main():
    
    display = Display.getInstance()\
        .setStateProvider(EmulatedDrone.getInstance())\
        .setLauncherMethod(RemoteControl.main)
        
    display.start()


if __name__ == '__main__':
    main()