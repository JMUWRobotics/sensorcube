import serial 
import time 

sensorcube = serial.Serial(port='/dev/ttyACM0', baudrate=921600)

while True:
    print(sensorcube.readline().decode('utf-8').rstrip())
