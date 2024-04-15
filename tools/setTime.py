import serial 
import time 

sensorcube = serial.Serial(port='/dev/ttyACM0', baudrate=921600)

# wait for full second
while int(time.time() * 1000) % 1000 != 0:
    pass

t = time.time()
command = '{"time":' + str(int(t)) + ',"messages":["heartbeat"]}\r\n';
print("Set time: " + str(t))

sensorcube.write(bytes(command, 'utf-8'))

while True:
    print(sensorcube.readline().decode('utf-8').rstrip())
