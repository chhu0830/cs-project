#!/usr/bin/python3

import smbus
import math
from time import time, sleep
import sys

'''
if (len(sys.argv) != 2):
    print("usage:", sys.argv[0], "<IPaddress>")
    sys.exit();
'''
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

p = 10
q = 0.001
r = 0.05
kGain = 0
prevData = 0

f = open('curve.csv', 'w')

def kalmanFilter(inData):
    global p, q, r, kGain, prevData
    p = p + q
    kGain = p / (p + r)
    inData = prevData + (kGain * (inData - prevData))
    p = (1 - kGain) * p
    prevData = inData
    return inData

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

'''
def post(speed): 
    import requests
    from datetime import datetime
    from uuid import getnode as get_mac

    url = 'http://' + sys.argv[1] + '/data'
    now = datetime.now()

    print(speed)
    payload = {
        'datum[mac]': get_mac(),
        'datum[speed]': speed,
        'datum[distance]': now.second
    }
    r = requests.post(url, data=payload)
    return
'''

def get_speed(x, y, z):
    return (abs(x)**3 + abs(y)**3 + abs(z)**3)**(1/3.0)

Gyrox = 0
Gyroy = 0
Gyroz = 0
lasttimeX = 0
lasttimeY = 0
lasttimeZ = 0
Accx = 0.00
Accy = 0.00
Accz = 0.00
Ax = 0.00
Ay = 0.00
Az = 0.00
lastAx = 0.00
lastAy = 0.00
lastAz = 0.00

while True:
    bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
    address = 0x68       # This is the address value read via the i2cdetect command

    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    '''
    print ("gyro data")
    '''
    # print ("---------")
    t = time()
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    '''
    print ("gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131))
    print ("gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131))
    print ("gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131))

    print
    print ("accelerometer data")
    print ("------------------")
    '''

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
    
    

    '''
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print ("accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled)
    print ("accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled)
    print ("accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled)

    print ("x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print ("y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    '''
    '''
    Accx = (accel_xout / 8192.00 - 0.025) * 9.8
    Accy = (accel_yout / 8192.00 + 0.025) * 9.8
    Accz = (accel_zout / 8192.00 + 0.1) * 9.8
    '''

    Accx = accel_xout / 16384.0 * 9.81
    Accy = accel_yout / 16384.0 * 9.81
    Accz = (accel_zout / 16384.0 - 1) * 9.81

    gx = gyro_xout / 131.00
    gy = gyro_yout / 131.00
    gz = gyro_zout / 131.00

    dt = time() - t

    Gyrox = Gyrox + (lasttimeX + gx) * dt / 2
    Gyroy = Gyroy + (lasttimeY + gy) * dt / 2
    Gyroz = Gyroz + (lasttimeZ + gz) * dt / 2
    
    Ax = (lastAx + Accx) * dt / 2 * 100
    Ay = (lastAy + Accy) * dt / 2 * 100
    Az = (lastAz + Accz) * dt / 2 * 100

    lasttimeX = gx;
    lasttimeY = gy;
    lasttimeZ = gz;

    lastAx = Accx;
    lastAy = Accy;
    lastAz = Accz;
    

    '''
    print("TIME:", dt)
    print("GX:", Gyrox)
    print("GY:", Gyroy)
    print("GZ:", Gyroz)
    '''
    
    print("Ax:", Ax)
    print("Ay:", Ay)
    print("Az:", Az)
    print("dt", dt)
    print
    AAx = kalmanFilter(Ax)
    AAy = kalmanFilter(Ay)
    AAz = kalmanFilter(Az)
    '''
    print("Ax:", Ax)
    print("Ay:", Ay)
    print("Az:", Az)
    print("dt", dt)
    '''
    print("----------------")
    f.write("{0},{1},{2},{3},{4},{5}\n".format( Ax, Ay, Az, AAx, AAy, AAz))
    
    #sleep(0.2)
f.close()
  
