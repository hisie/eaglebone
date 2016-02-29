'''
Created on 12/04/2015

@author: david
'''
from math import sin, cos
import random
from threading import Thread
import time

from flight.stabilization.pid import PID


class SensorReader(object):
    
    def __init__(self, readDelegate):
        
        self._readDelegate = readDelegate        
        
    
    def readCurrentValue(self):
        
        return self._readDelegate()
    

class ResultSetter(object):
    
    def __init__(self, setResultDelegate):
        
        self._setResultDelegate = setResultDelegate
        
    
    def setResult(self, newValue):
        
        self._setResultDelegate(newValue)    
        

class SimulatedDrone(object):       
    
    def __init__(self):
    
        random.seed()
    
        self._accData = [0.0, 0.0]   
        self._accTarget = [0.0, 0.0]
             
        #self._accZ = 0.0
        #self._gyroZ = 0.0
        
        self._motors = [0.0, 0.0, 0.0, 0.0]
        
        self._sensorReaderX = SensorReader(self._readAccX)
        self._sensorReaderY = SensorReader(self._readAccY)
        
        self._resultSetterX = ResultSetter(self._setX)
        self._resultSetterY = ResultSetter(self._setY)
    
        self._pidAnglesSpeed = PID([0.1]*2, [0.1]*2, 0,[self._sensorReaderX,self._sensorReaderY], \
                         [self._resultSetterX, self._resultSetterY], [0]*2, 2)
        self._pidAnglesSpeed.setTargets(self._accTarget)
        
        self._printThread = Thread(target=self._printStatusDelegate)
        self._isRunning = False
        
    
    def _calculateAcc(self, motorPos1Id, motorPos2Id, motorNeg1Id, motorNeg2Id, accIndex, defect):

        acc = self._motors[motorPos1Id] + self._motors[motorPos2Id] - self._motors[motorNeg1Id] - self._motors[motorNeg2Id]        
        self._accData[accIndex] = acc + defect
    
    
    def _readAccX(self):
        
        #self._accData[0] = self._accData[0] + random.uniform(-0.1, 0.1)        
        
        return self._accData[0]
    
    
    def _readAccY(self):
        
        #self._accData[1] = self._accData[1] + random.uniform(-0.01, 0.01)
        
        return self._accData[1]
        
    
    def _setMotor(self, motorId, increment):
        
        newValue = self._motors[motorId] + increment
        if newValue > 100.0:
            newValue = 100.0
        elif newValue < 0.0:
            newValue = 0.0
        
        self._motors[motorId] = newValue
        
    
    def _setY(self, increment):
        
        self._setMotor(0, -increment)
        self._setMotor(3, -increment)
        
        self._setMotor(1, increment)
        self._setMotor(2, increment)
        
        self._calculateAcc(1, 2, 0, 3, 1, 0.0)
        
    def _setX(self, increment):

        self._setMotor(0, -increment)
        self._setMotor(1, -increment)
        
        self._setMotor(2, increment)
        self._setMotor(3, increment)
        
        self._calculateAcc(2, 3, 0, 1, 0, 0.5)
        
    
    def _printStatusDelegate(self):
        
        while self._isRunning:        
            print "Accel :{0}; Motors:{1})".format(self._accData, self._motors)
            time.sleep(1)
    
        
    def addThrottle(self, increment):
        
        for motorId in range(4):
            self._motors[motorId] = self._motors[motorId] + increment
        

    def shift(self, angle, radius):
    
        acc = 0.1 * radius / 100.0
        xacc = sin(angle) * acc
        yacc = cos(angle) * acc
        
        self._accTarget[0] = xacc
        self._accTarget[1] = yacc
        
        self._pidAnglesSpeed.setTargets(self._accTarget)
        
        print "Target: {0}".format(self._accTarget)
        

    def start(self):
        
        self._isRunning = True
        
        self._printThread.start()
        
        self._pidAnglesSpeed.start()
        
    
    def stop(self):
        
        self._isRunning = False
        
        self._pidAnglesSpeed.stop()
        self._pidAnglesSpeed.join()
        
        self._printThread.join()

    
if __name__ == '__main__':
    
    drone = SimulatedDrone()    
    drone.start()
   
    
    done = False
    while not done:
        command = raw_input("Command? >").strip().split()
        command0 = command[0]
        
        if command0 == "Q":
            done = True
            
        elif command0 == "T":
            increment = float(command[1])
            drone.addThrottle(increment)            
            
        elif command0 == "S":
            angle = float(command[1])
            increment = float(command[2])
            drone.shift(angle, increment)           
        
    
    print "Finishing..."
    drone.stop()
    print "Goodbye!"
    