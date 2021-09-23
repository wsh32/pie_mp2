import serial
import time

def read2dist(reading):
    num = ((pow((96525*reading)/1088 - 889849181450345845042039/98863019020037128192, 2) + 4320918025146633092526075044890718306748939018668359539455369/6599702224362321183928599545720790629314745847412424704)**(1./2.) - (96525*reading)/1088 + 889849181450345845042039/98863019020037128192)**(1./3.) - 162876592769475220889/(1875749244799811584*((((96525*reading)/1088 - 889849181450345845042039/98863019020037128192)**(2.) + 4320918025146633092526075044890718306748939018668359539455369/6599702224362321183928599545720790629314745847412424704)**(1./2.) - (96525*reading)/1088 + 889849181450345845042039/98863019020037128192)**(1./3.)) + 20779/448

    return num


arduinoComPort = "COM6"
baudRate = 9600
serialPort = serial.Serial(arduinoComPort, baudRate, timeout = 1)

total = 0
dist = 0
avgDist = 0
count = 0
while True:
    lineOfData = serialPort.readline().decode()
    num = str(lineOfData[:-2])
    for index in enumerate(num):
        w = num.split(' ')
        dist = read2dist(float(w[0]))
    # rolling average
    if(count >= 10):
        avgDist = total / count
        print(avgDist)

        total = 0
        count = count % 10


    else:
        count = count + 1
        total = total + dist
