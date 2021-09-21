from serial import Serial
from serial.tools import list_ports

import sys
import time

ports = list(list_ports.grep('usb'))

if len(ports) == 0:
    print("No device found")
    sys.exit()

print(list(ports[0]))

baudrate = 115200
#ser = Serial(ports[0][0], baudrate, timeout=1)
ser = Serial('/dev/cu.usbserial-10', baudrate, timeout=1)

while True:
    x = 100
#    ser.write(x.to_bytes(1, byteorder='big'))
#    ser.write(b'd')
    ser.write("ddddd".encode('utf-8'))
#    print(int.from_bytes(ser.read(), byteorder='big', signed=False))
    print(ser.read())

