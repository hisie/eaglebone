# -*- coding: utf-8 -*-

import logging
import math
import time

import flight.stabilization.imu3000_defs as imu3000
import flight.stabilization.kxtf9_defs as kxtf9


try:
    import smbus
    
except ImportError:
    
    class smbus(object):
        @staticmethod
        def SMBus(channel):
            raise Exception("smbus module not found!")


bus = smbus.SMBus(1)

GYRO_ADDRESS = 0x68
ACCEL_ADDRESS = 0x0f

def readWord(address, regH, regL):

    byteH = bus.read_byte_data(address, regH)
    byteL = bus.read_byte_data(address, regL)

    word = (byteH << 8) | byteL
    if (byteH & 0x80) != 0:
        word = -(0xffff - word + 1)

    return word

def readWordHL(address, reg):

    return readWord(address, reg, reg+1)

def readWordLH(address, reg):

    return readWord(address, reg+1, reg)

def writeWord(address, regH, regL, word):

    byteH = word >> 8
    byteL = word & 0xff

    bus.write_byte_data(address, regH, byteH)
    bus.write_byte_data(address, regL, byteL)


def writeWordHL(address, reg, word):

    writeWord(address, reg, reg+1, word)


def writeWordLH(address, reg, word):

    writeWord(address, reg+1, reg, word)

def readGyroX():
    return readWordHL(GYRO_ADDRESS, imu3000.GYRO_XOUT)

def readGyroY():
    return readWordHL(GYRO_ADDRESS, imu3000.GYRO_YOUT)

def readGyroZ():
    return readWordHL(GYRO_ADDRESS, imu3000.GYRO_ZOUT)

def readAuxX():
    return readWordHL(GYRO_ADDRESS, imu3000.AUX_XOUT)

def readAuxY():
    return readWordHL(GYRO_ADDRESS, imu3000.AUX_YOUT)

def readAuxZ():
    return readWordHL(GYRO_ADDRESS, imu3000.AUX_ZOUT)

def readAccelX():
    return readWordLH(ACCEL_ADDRESS, kxtf9.XOUT) / 16

def readAccelY():
    return readWordLH(ACCEL_ADDRESS, kxtf9.YOUT) / 16

def readAccelZ():
    return readWordLH(ACCEL_ADDRESS, kxtf9.ZOUT) / 16

'''
def readTemp():
    return readWord(addrGyro, 0x1b, 0x1c)
'''

def initGyro():
    
    #Initializes gyro
    bus.write_byte_data(GYRO_ADDRESS, imu3000.PWR_MGM, imu3000.H_RESET)
    bus.write_byte_data(GYRO_ADDRESS, imu3000.PWR_MGM, imu3000.CLK_SEL_X)
    bus.write_byte_data(GYRO_ADDRESS, imu3000.SMPLRT_DIV, 49)
    bus.write_byte_data(GYRO_ADDRESS, imu3000.DLPF_FS, imu3000.FS_SEL_2000 | imu3000.DLPF_CFG_42)

    #bus.write_byte_data(GYRO_ADDRESS, imu3000.FIFO_EN, imu3000.GYRO_XOUT_EN | imu3000.GYRO_YOUT_EN | imu3000.GYRO_ZOUT_EN | imu3000.FIFO_FOOTER_EN)
    
    gyroOffsetX = readGyroX()
    gyroOffsetY = readGyroY()
    gyroOffsetZ = readGyroZ()
    
    writeWordHL(GYRO_ADDRESS, imu3000.X_OFFS, gyroOffsetX)
    writeWordHL(GYRO_ADDRESS, imu3000.Y_OFFS, gyroOffsetY)
    writeWordHL(GYRO_ADDRESS, imu3000.Z_OFFS, gyroOffsetZ)
    
    '''
    bus.write_byte_data(GYRO_ADDRESS, imu3000.AUX_SLV_ADDR, ACCEL_ADDRESS)
    bus.write_byte_data(GYRO_ADDRESS, imu3000.AUX_BURST_ADDR, kxtf9.XOUT)
    '''

    # Initialize accelerometer
    bus.write_byte_data(GYRO_ADDRESS, imu3000.USER_CTRL, imu3000.AUX_IF_RST)
    
    bus.write_byte_data(ACCEL_ADDRESS, kxtf9.CTRL_REG1, 0)
    bus.write_byte_data(ACCEL_ADDRESS, kxtf9.CTRL_REG1, kxtf9.RES | kxtf9.GSEL_4G)
    bus.write_byte_data(ACCEL_ADDRESS, kxtf9.CTRL_REG1, kxtf9.RES | kxtf9.GSEL_4G | kxtf9.PC1)
    
    #bus.write_byte_data(GYRO_ADDRESS, imu3000.USER_CTRL, imu3000.AUX_IF_EN | imu3000.AUX_IF_RST) # | imu3000.DMP_EN | imu3000.DMP_RST)
    #bus.write_byte_data(GYRO_ADDRESS, imu3000.USER_CTRL, imu3000.FIFO_EN_BIT | imu3000.FIFO_RST)
    
    #bus.write_byte_data(GYRO_ADDRESS, imu3000.INT_CFG, imu3000.RAW_DATA_RDY)

logging.basicConfig(filename="gyro.log", level=logging.DEBUG)

initGyro()

angX = 0.0
angY = 0.0
angZ = 0.0

vangX = 0
vangY = 0
vangZ = 0

ready = 0

sleepTime = 0.005

accOffsetX = 0
accOffsetY = 0
accOffsetZ = 0

gyroOffsetX = 0
gyroOffsetY = 0
gyroOffsetZ = 0

print "Calibrando acelerómetro..."

for i in range(30):
    accOffsetX = (accOffsetX + readAccelX()) / 2
    accOffsetY = (accOffsetY + readAccelY()) / 2
    accOffsetZ = (accOffsetZ + readAccelZ()) / 2
    time.sleep(sleepTime)

print "Calibrando giróscopo..."

for i in range(30):
    gyroOffsetX = (gyroOffsetX + readGyroX()) / 2
    gyroOffsetY = (gyroOffsetY + readGyroY()) / 2
    gyroOffsetZ = (gyroOffsetZ + readGyroZ()) / 2
    time.sleep(sleepTime)

rawAccX = readAccelX() 
rawAccY = readAccelY() 
rawAccZ = readAccelZ() 

angOffsetX = (math.atan2(rawAccY, rawAccZ)) * 180.0 / math.pi
angOffsetY = -(math.atan2(rawAccX, rawAccZ)) * 180.0 / math.pi

logtext = "Offset acelerómetro: {0}, {1}, {2}".format(accOffsetX, accOffsetY, accOffsetZ)
print logtext
logging.info(logtext)

logtext = "Offset giróscopo: {0}, {1}, {2}".format(gyroOffsetX, gyroOffsetY, gyroOffsetZ)
print logtext
logging.info(logtext)

time.sleep(3)

initTime = lastReadTime = time.time()
counter = 0


while True:

    counter = counter + 1

    vangX = float(readGyroX() - gyroOffsetX) * 2000.0 / 32767.0
    vangY = float(readGyroY() - gyroOffsetY) * 2000.0 / 32767.0
    vangZ = float(readGyroZ() - gyroOffsetZ) * 2000.0 / 32767.0
    readTime = time.time()
    dt = readTime - lastReadTime
    lastReadTime = readTime
    
    rawAccX = readAccelX() 
    rawAccY = readAccelY() 
    rawAccZ = readAccelZ() 

    accX = float(rawAccX - accOffsetX) / 512.0
    accY = float(rawAccY - accOffsetY) / 512.0
    accZ = float(rawAccZ - accOffsetZ) / 512.0
    '''
    accX = readAuxX() #- accOffsetX
    accY = readAuxY() #- accOffsetY
    accZ = readAuxZ() #- accOffsetZ
    '''
    
    accAngX = ((math.atan2(rawAccY, rawAccZ)) * 180.0 / math.pi) - angOffsetX
    accAngY = -((math.atan2(rawAccX, rawAccZ)) * 180.0 / math.pi) - angOffsetY    
    
    if counter < 100:
        dx = vangX * dt
        dy = vangY * dt
        dz = vangZ * dt
        angX = 0.98 * (angX + dx) + 0.02 * accAngX
        angY = 0.98 * (angY + dy) + 0.02 * accAngY
        angZ = angZ + dz
    
    else:
        angX = accAngX
        angY = accAngY
        angZ = 0.0

        counter = 0
    
    '''
    angX = angX + vangX * dt
    angY = angY + vangY * dt
    angZ = angZ + vangZ * dt
    '''
    elapsedTime = lastReadTime - initTime
    logtext = "{0}s: G({1:.3f}, {2:.3f}, {3:.3f}) A({4:.4f}, {5:.4f}, {6:.4f})".format(elapsedTime, angX, angY, angZ, accX, accY, accZ)
    print logtext
    logging.debug(logtext)

    time.sleep(sleepTime)
    '''
    ready = 0
    while ready == 0:
        
        ready = bus.read_byte_data(GYRO_ADDRESS, imu3000.INT_STATUS)
        ready = ready & imu3000.RAW_DATA_RDY
    '''
