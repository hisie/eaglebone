# -*- coding: utf-8 -*-

'''
Created on 10/06/2015

@author: david
'''

import datetime
import logging
import time

from sensors.imu6050dmp import Imu6050Dmp as Sensor


logging.basicConfig(filename="imu6050dmp_test_{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")), \
                    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', datefmt='%d/%m/%y %H:%M:%S', \
                    level=logging.ERROR)

sensor = Sensor()
sensor.start()

lastAccels = [0.0]*3
lastSpeeds = [0.0]*3
speeds = [0.0]*3
height = 0.0

lasttime = time.time()

try:
    sensor.resetGyroReadTime()
    while True:
    
        sensor.refreshState()
        angles = sensor.readDeviceAngles()
        angles[2] = sensor.readAngleSpeeds()[2]

        accels = sensor.readAccels()    
        
        nowtime = time.time()
        dt2 = (nowtime-lasttime) / 2.0
        lasttime = nowtime
        
        for index in range(3):
            oldSpeed = speeds[index]
            speeds[index] += (lastAccels[index] + accels[index]) * dt2
            
            #errors[index]+=accels[index]
        
        height += (lastSpeeds[2] + speeds[2]) * dt2
        
        lastAccels = accels
        lastSpeeds = speeds
        
        anglesStr = "An({0:.3f}, {1:.3f}, {2:.3f})".format(angles[0], angles[1], angles[2])
        accelsStr = "Ac({0:.3f}, {1:.3f}, {2:.3f})".format(accels[0], accels[1], accels[2])
        speedsStr = "Sp({0:.3f}, {1:.3f}, {2:.3f})".format(speeds[0], speeds[1], speeds[2])
        #heightStr = "H ({0:.3f})".format(height)
    
        #print "{0}; {1}; {2}; {3}".format(heightStr, speedsStr, anglesStr, accelsStr)
        print "{0}; {1}; {2}".format(speedsStr, anglesStr, accelsStr)

        time.sleep(0.1)
        
except KeyboardInterrupt:
    
    print "[Ctrl+C] -> stop"    
    
finally:    
    sensor.stop()
