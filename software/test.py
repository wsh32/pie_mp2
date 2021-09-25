import device
import serial
import serial_process
import time


if __name__ == '__main__':
    d = device.find_arduino_port()

    p = serial_process.SerialProcess(d, 115200)

    time.sleep(10)

