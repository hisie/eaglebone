# -*- coding: utf-8 -*-
'''
Created on 04/03/2016

@author: david
'''

import logging
from math import degrees
import time

from sensors.pycomms.mpu6050 import MPU6050
from sensors.vector import Vector


class Imu6050Dmp(object):
    '''
    IMU-6050 using the DMP (digital motion processing) feature
    '''

    GRAVITY = 9.807

    def __init__(self):
        
        self._imu = MPU6050(channel=1)

        self._packetSize = 0
        self._angleOffset = [0.0]*3 #radians
        self._gravityOffset = [0.0]*3 #g
        
        self._angleSpeeds = [0.0]*3 #degrees
        self._angles = [0.0]*3 #radians
        self._accels = [0.0]*3 #g
        
        self._maxErrorAccelZ = 0.0
        

    def readAngleSpeeds(self):

        return self._angleSpeeds

    
    def readAngles(self):
        
        return [degrees(angle) for angle in self._angles]


    def readDeviceAngles(self):
        
        deviceAngles = [0.0]*3
        for index in range(3):
            deviceAngles[index] = self._angles[index] - self._angleOffset[index]

        return [degrees(angle) for angle in deviceAngles]

    
    def readAccels(self):
        
        accels = [0.0]*3
        for index in range(3):
            accels[index] = (self._accels[index] - self._gravityOffset[index]) * Imu6050Dmp.GRAVITY
        
        return accels

    
    def resetGyroReadTime(self):        
        pass

    def _readPacket(self):

        fifoCount = self._imu.getFIFOCount()
        
        #Wait for data
        while fifoCount < 64:
            fifoCount = self._imu.getFIFOCount()
        
        fifo = []
        fifo += self._imu.getFIFOBlock()
        fifo += self._imu.getFIFOBlock()

        self._imu.resetFIFO()	
        
        return fifo[:42]
    

    def refreshState(self):
        
        packet = self._readPacket()
        
        q = self._imu.dmpGetQuaternion(packet)
        g = self._imu.dmpGetGravity(q)
        
        self._angleSpeeds = self._imu.dmpGetGyro(packet)
        
        ypr = self._imu.dmpGetYawPitchRoll(q, g)
        self._angles = [ypr["pitch"], ypr["roll"], ypr["yaw"]]

        accelRaw = self._imu.dmpGetAccel(packet)
        linearAccel = self._imu.dmpGetLinearAccel(accelRaw, g)        
        
        self._accels = Vector.rotateVector3D(linearAccel, self._angles)

    
    def start(self):

        text = "Using IMU-6050 (DMP)." 

        print text
        logging.info(text)

        self._imu.dmpInitialize()
        self._imu.setDMPEnabled(True)

        # Get expected DMP packet size for later comparison
        self._packetSize = self._imu.dmpGetFIFOPacketSize()

        self.calibrate()

    
    def calibrate(self):
        
        print "Calibrating..."
        time.sleep(20)
        self._imu.resetFIFO()
        
        packet = self._readPacket()
        
        q = self._imu.dmpGetQuaternion(packet)
        g = self._imu.dmpGetGravity(q)
        
        ypr = self._imu.dmpGetYawPitchRoll(q, g)
        self._angleOffset = [ypr["pitch"], ypr["roll"], ypr["yaw"]]

        accelRaw = self._imu.dmpGetAccel(packet)
        linearAccel = self._imu.dmpGetLinearAccel(accelRaw, g)
        self._gravityOffset = Vector.rotateVector3D(linearAccel, self._angleOffset)
        
        #Calculate Z-accel max error
        self._maxErrorAccelZ = 0.0
        
        count = 0
        while count < 50:
            self.refreshState()
            accelZ = self.readAccels()
            if accelZ > self._maxErrorAccelZ:
                self._maxErrorAccelZ = accelZ
            
            time.sleep(0.02)    
            count += 1
        

    def getMaxErrorZ(self):

        return self._maxErrorAccelZ


    def stop(self):
        
        self._imu.setDMPEnabled(False)
        self._imu.setSleepEnabled(True)
