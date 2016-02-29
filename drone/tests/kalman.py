# -*- coding: utf-8 -*-

'''
Created on 22/04/2015

@author: david
'''
#from flight.stabilization.sensor import Sensor
import math
import random
import time

from flight.stabilization.data_structures import DataSmoothWindow


x1 = 0
p1 = 1

smooth = DataSmoothWindow(7)
smooth.push(x1)

random.seed()
#sensor = Sensor()
#sensor.start()

try:
    
    while True:
    
        base = math.floor(random.uniform(0, 100))
        print "base = {0}".format(base)
    
        for i in range(100):
            z = base + random.uniform(-0.5, 0.5) #sensor.readAccelY()
        
            #prediction
            a = smooth.average()
            ex = x1 + z - a
            ep = p1
        
            #correction
            k = ep / (ep + 0.5)
            p = (1-k)*ep
            x = ex + k*(z-ex)

            print "raw: {0}\tfiltered: {1}".format(z, x)
            time.sleep(0.1)
        
            smooth.push(z)
        
            x1 = x
            p1 = p
    
finally:    
    #sensor.stop()
    pass

