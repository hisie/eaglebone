﻿
# Register addresses

XOUT_HPF_L = 0x00
XOUT_HPF_H = 0x01
YOUT_HPF_L = 0x02
YOUT_HPF_H = 0x03
ZOUT_HPF_L = 0x04
ZOUT_HPF_H = 0x05
XOUT_L = 0x06
XOUT_H = 0x07
YOUT_L = 0x08
YOUT_H = 0x09
ZOUT_L = 0x0a
ZOUT_H = 0x0b

XOUT_HPF = XOUT_HPF_L
YOUT_HPF = YOUT_HPF_L
ZOUT_HPF = ZOUT_HPF_L
XOUT = XOUT_L
YOUT = YOUT_L
ZOUT = ZOUT_L

CTRL_REG1 = 0x1b


# Masks and values

#CTRL_REG1
PC1		= 0b10000000
RES		= 0b01000000
DRDYE	= 0b00100000
GSEL1	= 0b00010000
GSEL0	= 0b00001000
TDTE	= 0b00000100
WUFE	= 0b00000010
TPE		= 0b00000001

GSEL_2G = 0
GSEL_4G = 1
GSEL_8G = 2

