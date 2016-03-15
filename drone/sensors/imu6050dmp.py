# -*- coding: utf-8 -*-
'''
Created on 04/03/2016

@author: david
'''

import logging
from math import degrees
from threading import Thread, Lock
from copy import deepcopy
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

        self._anglesStats = [{ "count": 0, "sum": 0.0,  "max": 0.0, "min": 0.0 }, \
                                  { "count": 0, "sum": 0.0,  "max": 0.0, "min": 0.0 }, \
                                  { "count": 0, "sum": 0.0,  "max": 0.0, "min": 0.0 }]

        self._accelsStats = [{ "count": 0, "sum": 0.0,  "max": 0.0, "min": 0.0 }, \
                                  { "count": 0, "sum": 0.0,  "max": 0.0, "min": 0.0 }, \
                                  { "count": 0, "sum": 0.0,  "max": 0.0, "min": 0.0 }]
        
        self._maxErrorAccelZ = 0.1
        
        self._packet = None
        self._isRunning = False
        self._packetReadingThread = Thread(target=self._doPacketReading)
        self._packetLock = Lock()

        
    @staticmethod
    def _calculateStatistics(stats, values):

        for index in range(len(stats)):
            stats[index]["count"] += 1
            stats[index]["sum"] += value

            if value > stats[index]["max"]:
                stats[index]["max"] = value

            if value < stats[index]["min"]:
                stats[index]["min"] = value


    @staticmethod
    def _statisticsToString(stats):

        text = ""

        for stat in stats:

            average = 0.0
            if stat["count"] != 0.0:
                average = stat["sum"] / stat["count"]

            text += "\tavg: {0}; max: {1}; min: {2}\n".format(average, stat["max"], stat["min"])

        return text


    def readAngleSpeeds(self):

        return self._angleSpeeds

    
    def readAngles(self):
        
        angles = [degrees(angle) for angle in self._angles]

        Imu6050Dmp._calculateStatistics(self._anglesStats, angles)

        return angles


    def readDeviceAngles(self):
        
        deviceAngles = [0.0]*3
        for index in range(3):
            deviceAngles[index] = self._angles[index] - self._angleOffset[index]

        return [degrees(angle) for angle in deviceAngles]

    
    def readAccels(self):
        
        accels = [0.0]*3
        for index in range(3):
            accels[index] = (self._accels[index] - self._gravityOffset[index]) * Imu6050Dmp.GRAVITY
        
        Imu6050Dmp._calculateStatistics(self._accelsStats, accels)

        return accels

    
    def resetGyroReadTime(self):        
        pass

    def _readPacket(self):
    
        while self._imu.getIntStatus() < 2:
            time.sleep(0.001)

        fifoCount = self._imu.getFIFOCount()
        
        if fifoCount == 1024:
            self._imu.resetFIFO()
            fifoCount = 0
        
        while fifoCount < self._packetSize:
            fifoCount = self._imu.getFIFOCount()
        
        with self._packetLock:
            self._packet = self._imu.getFIFOBlock()
            fifoCount = self._imu.getFIFOCount()
            while fifoCount > 0:
                self._packet += self._imu.getFIFOBlock()
                fifoCount = self._imu.getFIFOCount()
    

    def refreshState(self):
        
        with self._packetLock:
            packet = deepcopy(self._packet)
        
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
        
        self._isRunning = True
        self._packetReadingThread.start()
        
        self.calibrate()

    
    def calibrate(self):
        
        print "Calibrating..."
        time.sleep(20)        
        self._imu.resetFIFO()
        
        #Wait for next packet
        time.sleep(0.05)
        
        with self._packetLock:
            packet = deepcopy(self._packet) #self._readPacket()
        
        q = self._imu.dmpGetQuaternion(packet)
        g = self._imu.dmpGetGravity(q)
        
        ypr = self._imu.dmpGetYawPitchRoll(q, g)
        self._angleOffset = [ypr["pitch"], ypr["roll"], ypr["yaw"]]
        
        accelRaw = self._imu.dmpGetAccel(packet)
        linearAccel = self._imu.dmpGetLinearAccel(accelRaw, g)
        self._gravityOffset = Vector.rotateVector3D(linearAccel, self._angleOffset)


    def getMaxErrorZ(self):

        return self._maxErrorAccelZ


    def stop(self):
        
        self._isRunning = False
        
        if self._packetReadingThread.isAlive():
            self._packetReadingThread.join()
        
        self._imu.setDMPEnabled(False)
        self._imu.setSleepEnabled(True)

        print "IMU stats:"
        print "-angles"
        print Imu6050Dmp._statisticsToString(self._anglesStats)
        print "-accels"
        print Imu6050Dmp._statisticsToString(self._accelsStats)
        

    def _doPacketReading(self):
        
        while self._isRunning:
            self._readPacket()
        