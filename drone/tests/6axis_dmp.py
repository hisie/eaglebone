import math

import sensors.pycomms.mpu6050 as mpu6050


# Sensor initialization
mpu = mpu6050.MPU6050(channel=1)
mpu.dmpInitialize()
mpu.setDMPEnabled(True)
    
# get expected DMP packet size for later comparison
packetSize = mpu.dmpGetFIFOPacketSize() 

offset = None

while True:
    # Get INT_STATUS byte
    mpuIntStatus = mpu.getIntStatus()
  
    if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently) 
        # get current FIFO count
        fifoCount = mpu.getFIFOCount()
        
        # check for overflow (this should never happen unless our code is too inefficient)
        if fifoCount == 1024:
            # reset so we can continue cleanly
            mpu.resetFIFO()
            print('FIFO overflow!')
            
            
        # wait for correct available data length, should be a VERY short wait
        fifoCount = mpu.getFIFOCount()
        while fifoCount < packetSize:
            fifoCount = mpu.getFIFOCount()
        
        result = mpu.getFIFOBytes(packetSize)
        q = mpu.dmpGetQuaternion(result)
        
        accelRaw = mpu.dmpGetAccel(result)
        g = mpu.dmpGetGravity(q)
        linearAccel = mpu.dmpGetLinearAccel(accelRaw, g)
        
        ypr = mpu.dmpGetYawPitchRoll(q, g)
        
        if offset == None:
            offset = ypr      
        
        deviceAngles = [math.degrees(angle) \
                        for angle in [ypr['pitch']-offset['pitch'],ypr['roll']-offset['roll'],ypr['yaw']-offset['yaw']]]
        
        accels = mpu.dmpGetLinearAccelInWorld(linearAccel, [ypr['pitch'],ypr['roll'],ypr['yaw']])
        
        accels = [accel * 9.807 for accel in accels]
        
        accelStr = "({0:.3f},{1:.3f},{2:.3f})".format(accels[0],accels[1],accels[2])
        angleStr = "({0:.3f},{1:.3f},{2:.3f})".format(deviceAngles[0],deviceAngles[1],deviceAngles[2])
        
        print "Acc: {0}; Ang: {1}".format(accelStr, angleStr)
    
        # track FIFO count here in case there is > 1 packet available
        # (this lets us immediately read more without waiting for an interrupt)        
        fifoCount -= packetSize  