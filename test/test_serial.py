from serial import Serial
from serial.tools import list_ports

import sys
import time

"""
ports = list(list_ports.grep('usb'))

if len(ports) == 0:
    print("No device found")
    sys.exit()

print(list(ports[0]))
"""

arduino_ids = ((0x2341, 0x0043), (0x2341, 0x0001),
               (0x2A03, 0x0043), (0x2341, 0x0243),
               (0x0403, 0x6001), (0x1A86, 0x7523))

ser = None
baudrate = 115200

devices = list_ports.comports()
for device in devices:
    if (device.vid, device.pid) in arduino_ids:
        ser = Serial(device.device, baudrate, timeout=1)

#ser = Serial(ports[0][0], baudrate, timeout=1)
#ser = Serial('/dev/tty.usbserial-10', baudrate, timeout=1)

with ser:
    while True:
        x = 100
        ser.write(x.to_bytes(1, byteorder='big'))
    #    ser.write(b'd')
    #    ser.write("ddddd".encode('utf-8'))
    #    print(int.from_bytes(ser.read(), byteorder='big', signed=False))
        print(ser.read())

