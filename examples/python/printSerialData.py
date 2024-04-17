import os
import serial 
import json

# load config file (same directory as this file)
configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/config.json')
config = json.load(configFile)

# open serial port
sensorcube = serial.Serial(port=config["serial_port"], baudrate=config["serial_baudrate"])

while True:
    try:
        print(sensorcube.readline().decode('utf-8').rstrip())
    except KeyboardInterrupt:
        break
