import os
import serial 
import json
import argparse
import time

parser = argparse.ArgumentParser(description='Print and record messages.')
parser.add_argument('-f', '--file', dest='file', type=str, help='Output filename for recording messages.')
parser.add_argument('--overwrite', help='Overwrite exisiting files.', action="store_true")
args = parser.parse_args()

file = None
if args.file is not None:
    print('Recording to file "' + args.file +'".')
    if args.overwrite:
        file = open(args.file, 'wb')
    else:
        file = open(args.file, 'xb')

configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json')
config = json.load(configFile)

sensorcube = serial.Serial(port=config["serial_port"], baudrate=config["serial_baudrate"])

command = '{"messages":["gnss_raw"]}\r\n';
sensorcube.write(bytes(command, 'utf-8'))

line = sensorcube.readline()

while True:
    try:
        line = sensorcube.readline()
        print(line)
        if file is not None:
            file.write(line)
    except KeyboardInterrupt:
        break
