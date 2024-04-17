import serial 
import time 
import json
import os

# load config file (same directory as this file)
configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/config.json')
config = json.load(configFile)

# open serial port
sensorcube = serial.Serial(port=config["serial_port"], baudrate=config["serial_baudrate"])

# wait for full second
while int(time.time() * 1000) % 1000 != 0:
    pass

t = time.time()
command = '{"time":' + str(int(t)) + ',"messages":["heartbeat"]}\r\n';
print("Set time " + str(t) + ".")

sensorcube.write(bytes(command, 'utf-8'))

while True:
    print(sensorcube.readline().decode('utf-8').rstrip())
