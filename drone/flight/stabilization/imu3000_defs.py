
# Register Adresses
WHO_AM_I        = 0x00
X_OFFS_USRH     = 0x0C
X_OFFS_USRL     = 0x0D
Y_OFFS_USRH     = 0x0E
Y_OFFS_USRL     = 0x0F
Z_OFFS_USRH     = 0x10
Z_OFFS_USRL     = 0x11
FIFO_EN         = 0x12
AUX_VDDIO       = 0x13
AUX_SLV_ADDR    = 0x14
SMPLRT_DIV      = 0x15
DLPF_FS         = 0x16
INT_CFG         = 0x17
AUX_BURST_ADDR  = 0x18
INT_STATUS      = 0x1A
TEMP_OUT_H      = 0x1B
TEMP_OUT_L      = 0x1C
GYRO_XOUT_H     = 0x1D
GYRO_XOUT_L     = 0x1E
GYRO_YOUT_H     = 0x1F
GYRO_YOUT_L     = 0x20
GYRO_ZOUT_H     = 0x21
GYRO_ZOUT_L     = 0x22
AUX_XOUT_H      = 0x23
AUX_XOUT_L      = 0x24
AUX_YOUT_H      = 0x25
AUX_YOUT_L      = 0x26
AUX_ZOUT_H      = 0x27
AUX_ZOUT_L      = 0x28
FIFO_COUNTH     = 0x3A
FIFO_COUNTL     = 0x3B
FIFO_R          = 0x3C
USER_CTRL       = 0x3D
PWR_MGM         = 0x3E

# 16 Bit registers
X_OFFS     = X_OFFS_USRH
Y_OFFS     = Y_OFFS_USRH
Z_OFFS     = Z_OFFS_USRH
TEMP_OUT   = TEMP_OUT_H
GYRO_XOUT  = GYRO_XOUT_H
GYRO_YOUT  = GYRO_YOUT_H
GYRO_ZOUT  = GYRO_ZOUT_H
AUX_XOUT   = AUX_XOUT_H
AUX_YOUT   = AUX_YOUT_H
AUX_ZOUT   = AUX_ZOUT_H
FIFO_COUNT = FIFO_COUNTH

# Masks and Values by register
# WHO_AM_I
ID      = 0b01111110

# FIFO_EN
TEMP_OUT_EN    = 0b10000000
GYRO_XOUT_EN   = 0b01000000
GYRO_YOUT_EN   = 0b00100000
GYRO_ZOUT_EN   = 0b00010000
AUX_XOUT_EN    = 0b00001000
AUX_YOUT_EN    = 0b00000100
AUX_ZOUT_EN    = 0b00000010
FIFO_FOOTER_EN = 0b00000001

# AUX_VDDIO
AUX_VDDIO_BIT = 0b00000100

# AUX_SLV_ADDR
CLKOUT_EN     = 0b10000000
AUX_ID        = 0b01111111

# DLPF_FS
FS_SEL_MASK   = 0b00011000
FS_SEL_250    = 0b00000000
FS_SEL_500    = 0b00001000
FS_SEL_1000   = 0b00010000
FS_SEL_2000   = 0b00011000
DLPF_CFG      = 0b00000111
DLPF_CFG_256  = 0b00000000
DLPF_CFG_188  = 0b00000001
DLPF_CFG_98   = 0b00000010
DLPF_CFG_42   = 0b00000011
DLPF_CFG_20   = 0b00000100
DLPF_CFG_10   = 0b00000101
DLPF_CFG_5    = 0b00000110

# INT_CFG
ACTL              = 0b10000000
OPEN              = 0b01000000
LATCH_INT_EN      = 0b00100000
INT_ANYRD_2CLEAR  = 0b00010000
I2C_MST_ERR_EN    = 0b00001000
IMU_RDY_EN        = 0b00000100
DMP_DONE_EN       = 0b00000010
RAW_RDY_EN        = 0b00000001

# INT_STATUS
FIFO_FULL         = 0b10000000
I2C_MST_ERR       = 0b00001000
IMU_RDY           = 0b00000100
DMP_DONE          = 0b00000010
RAW_DATA_RDY      = 0b00000001

# USER_CTRL
DMP_EN            = 0b10000000
FIFO_EN_BIT       = 0b01000000
AUX_IF_EN         = 0b00100000
AUX_IF_RST        = 0b00001000
DMP_RST           = 0b00000100
FIFO_RST          = 0b00000010
GYRO_RST          = 0b00000001

# PWR_MGM
H_RESET           = 0b10000000
SLEEP             = 0b01000000
STBY_XG           = 0b00100000
STBY_YG           = 0b00010000
STBY_ZG           = 0b00001000
CLK_SEL_INT       = 0b00000000 #Interal clock
CLK_SEL_X         = 0b00000001
CLK_SEL_Y         = 0b00000010
CLK_SEL_Z         = 0b00000011
CLK_SEL_EXT1      = 0b00000100 #External clock @32.768kHz reference
CLK_SEL_EXT2      = 0b00000101 #External clock @19.2MHz reference
#CLK_SEL_RESV     = 0b00000110 #Reserved. Not used
CLK_SEL_RST       = 0b00000111

