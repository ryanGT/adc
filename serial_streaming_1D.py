#USB

# RPi:
portname = '/dev/ttyACM0'
# Mac (probably)
#portname = '/dev/cu.usbmodem1421'
# Get the windows portname from the Arduino IDE

import serial
import time
from numpy import *
from matplotlib.pyplot import *

ser = serial.Serial(portname, 115200, timeout=1)
#ser.open()

ser.flushInput()
ser.flushOutput()

def Read_Line(ser):
    out = []
    i = 0
    while i < 1e5:
        data1 = ser.read(1)
        if data1 in ['\n','\r']:
            break
        out.append(data1)
        i += 1
    return out


def send_and_listen(send_me):
    ser.write(send_me)
    response_list = Read_Line(ser)
    response = ''.join(response_list)
    return response

time.sleep(2)
msg = send_and_listen(chr(1))

N = 256
nvect = zeros(N)
ser.write(chr(2))
time.sleep(0.5)
resp_list = []

for i in range(N):
    resp = ser.read(1)
    #nvect[i] = ord(resp)
    resp_list.append(resp)
    
ser.write(chr(3))
time.sleep(0.5)
ser.write(chr(3))


# drop empty responses:
resp_list2 = filter(None, resp_list)
resp_int_list = [ord(item) for item in resp_list2]
resp_array = array(resp_int_list)


ser.close()
show()
