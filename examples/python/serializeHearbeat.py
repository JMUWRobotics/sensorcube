import os
import serial 
import time 
import json

# load config file (same directory as this file)
configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/../../config.json')
config = json.load(configFile)

# open serial port
sensorcube = serial.Serial(port=config["serial_port"], baudrate=config["serial_baudrate"])

# enable only heartbeat message
command = '{"messages":["heartbeat"]}\r\n';
sensorcube.write(bytes(command, 'utf-8'))

while True:
    try:
        # read one line from serial and parse json
        try:
            line = sensorcube.readline().decode('utf-8').rstrip()
            data = json.loads(line)
        except:
            continue

        if not "msg" in data:
            continue

        # process heartbeat messages
        if data["msg"] == "heartbeat":
            stamp = data["stamp"]
            seq = data["seq"]
            print("Received heartbeat at time " + str(stamp) + " with sequence number " + str(seq) + ".")

        time.sleep(1)
    except KeyboardInterrupt:
        break
