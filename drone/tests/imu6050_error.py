# -*- coding: utf-8 -*-

'''
Created on 10/06/2015

@author: david
'''

import datetime
import logging
import time

from flight.stabilization.imu6050 import Imu6050 as Sensor


logging.basicConfig(filename="imu3000-error_test_{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")), \
                    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', datefmt='%d/%m/%y %H:%M:%S', \
                    level=logging.ERROR)

sensor = Sensor()
sensor.start()

accelErrorRange = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
angleErrorRange = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]

lasttime = time.time()

try:
    sensor.resetGyroReadTime()
    print "Reading (ctrl+C to finish) ..."
    while True:
    
        sensor.refreshState()
        angles = sensor.readDeviceAngles()
        angles[2] = sensor.readAngleSpeeds()[2]

        for index in range(3):
    
            if angles[index] > angleErrorRange[index][0]:
                angleErrorRange[index][0] = angles[index]
            
            if angles[index] < angleErrorRange[index][1]:
                angleErrorRange[index][1] = angles[index]
            

            accels = sensor.readAccels()    
        
        for index in range(3):
    
            if accels[index] > accelErrorRange[index][0]:
                accelErrorRange[index][0] = accels[index]
            
            if accels[index] < accelErrorRange[index][1]:
                accelErrorRange[index][1] = accels[index]
    
    
        time.sleep(0.02)
        
except KeyboardInterrupt:
    
    print "[Ctrl+C] -> stop"    
    
finally:
    print "accel range", accelErrorRange
    print "angles range", angleErrorRange
    sensor.stop()
