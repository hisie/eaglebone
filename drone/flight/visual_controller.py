'''
Created on 30/05/2015

@author: david
'''
from flight.driving.driver import Driver
from flight.stabilization.pid import PID
from flight.stabilization.visual_tracking import VisualTracker


class VisualFlightController(object):
    
    PID_ANGLES_SPEED_PERIOD = 0.05 #seconds
    
    PID_ANGLES_SPEED_KP = 0.0
    PID_ANGLES_SPEED_KI = 0.02
    PID_ANGLES_SPEED_KD = 0.08
    
    _instance = None
    
    @staticmethod
    def getInstance():
        
        if VisualFlightController._instance == None:
            VisualFlightController._instance = VisualFlightController()
            
        return VisualFlightController._instance
    
    
    def __init__(self):
        
        self._driver = Driver()
        self._sensor = VisualTracker()
        
        kpMatrix = [VisualFlightController.PID_ANGLES_SPEED_KP]*4
        kiMatrix = [VisualFlightController.PID_ANGLES_SPEED_KI]*4
        kdMatrix = [VisualFlightController.PID_ANGLES_SPEED_KD]*4
        
        tolerances  = [20.0, 20.0, 20.0, 10.0]
        initialTargets = [0.0]*4
        
        self._pidAnglesSpeed = PID(VisualFlightController.PID_ANGLES_SPEED_PERIOD, kpMatrix, kiMatrix, kdMatrix, \
                        self._readSensor, self._setResult, tolerances, len(kpMatrix))
        self._pidAnglesSpeed.setTargets(initialTargets)
        
        self._isRunning = False
    
    
    def _readSensor(self):
        
        inputData = self._sensor.track()
        inputData[2] = 0.0 #Z-input is disabled
        
        return inputData
    
    
    def _setX(self, increment):

        if increment != 0.0:
            self._driver.shiftX(increment)

    
    def _setY(self, increment):
        
        if increment != 0.0:
            self._driver.shiftY(increment)
        
            
    def _setZ(self, increment):
        
        if increment != 0.0:
            self._driver.addThrottle(increment)
    
    
    def _setAZ(self, increment):
        
        if increment != 0.0:
            self._driver.spin(increment)
            
    
    def _setResult(self, results):
        
        self._setX(results[0])
        self._setY(results[1])
        #self._setZ(results[2])
        self._setAZ(results[3])
   
        
    def addThrottle(self, increment):
        
        self._driver.addThrottle(increment)
        

    '''
    def shift(self, angle, radius):
    
        acc = VisualFlightController.MAX_ACCELERATION * radius / 100.0
        xacc = sin(angle) * acc
        yacc = cos(angle) * acc
        
        targetX = VisualFlightController._g2SensorUnit(xacc)
        targetY = VisualFlightController._g2SensorUnit(yacc)
        
        self._pidX.setTarget(targetX, 0)
        self._pidY.setTarget(targetY, 1)
        
        #logging.debug("Target: {0}".format(self._accTarget))
    '''   

    def start(self):
        
        self._isRunning = True
        
        #self._sensor.start()
        
        self._driver.start()
        self._driver.standBy()   
        
        self._pidAnglesSpeed.start()     

    
    def stop(self):
        
        self._isRunning = False
                       
        self._pidAnglesSpeed.stop()
        
        self.standBy()
        
        self._driver.stop()        
        self._sensor.stop()
        
        
    def standBy(self):
        
        self._driver.standBy()
    

    def idle(self):
        
        self._driver.idle()
        
    
