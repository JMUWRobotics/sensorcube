import os
import serial 
import json
import argparse
import time

parser = argparse.ArgumentParser(description='Print and record messages.')
parser.add_argument('-m', '--message', dest='message', action='append', type=str, help='Message type, e.g., "heartbeat".', required=True)
parser.add_argument('-f', '--file', dest='file', type=str, help='Output filename for recording messages.')
args = parser.parse_args()

file = None
if args.file is not None:
    print('Recording to file "' + args.file +'".')
    file = open(args.file, 'x')

messageString = ""
for m in args.message:
    if messageString != "":
        messageString = messageString + ','
    messageString = messageString + '"' + str(m) + '"'

configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/config.json')
config = json.load(configFile)

sensorcube = serial.Serial(port=config["serial_port"], baudrate=config["serial_baudrate"])

command = '{"messages":[' + messageString + ']}\r\n';
sensorcube.write(bytes(command, 'utf-8'))

line = sensorcube.readline().decode('utf-8').rstrip()

while True:
    try:
        line = sensorcube.readline().decode('utf-8').rstrip()
        print(line)
        if file is not None:
            file.write(line + '\n')
    except KeyboardInterrupt:
        break
