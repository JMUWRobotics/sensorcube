import serial 
import time 
import json
import matplotlib.pyplot as plt
import os
import multiprocessing

def readSerialData(queue, shutdownEvent):
    configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/config.json')
    config = json.load(configFile)

    sensorcube = serial.Serial(port=config["serial_port"], baudrate=config["serial_baudrate"])

    command = '{"messages":["imu_raw"]}\r\n';
    sensorcube.write(bytes(command, 'utf-8'))

    sensorcube.readline()

    while not shutdownEvent.is_set():
        s = sensorcube.readline()
        queue.put(s)

if __name__ == '__main__':
    queue = multiprocessing.Queue(maxsize=100)
    shutdownEvent = multiprocessing.Event()
    serialProcess = multiprocessing.Process(target=readSerialData, args=(queue, shutdownEvent))
    serialProcess.start()

    fig = plt.figure("IMU Plot")
    subplot1 = fig.add_subplot(2, 1, 1)
    subplot2 = fig.add_subplot(2, 1, 2)
    fig.subplots_adjust(hspace=.5)

    t = []
    ax = []
    ay = []
    az = []
    wx = []
    wy = []
    wz = []

    while True:
        while not queue.empty():
            s = queue.get()

            try:
                data = json.loads(s)
            except:
                continue

            if not "msg" in data:
                continue

            if data["msg"] == "imu_raw":
                t.append(float(data["stamp"]))
                ax.append(float(data["ax"]))
                ay.append(float(data["ay"]))
                az.append(float(data["az"]))
                wx.append(float(data["wx"]))
                wy.append(float(data["wy"]))
                wz.append(float(data["wz"]))

        # limit to 500 messages
        t=t[-500:]
        ax=ax[-500:]
        ay=ay[-500:]
        az=az[-500:]
        wx=wx[-500:]
        wy=wy[-500:]
        wz=wz[-500:]

        subplot1.clear()
        subplot1.plot(t,ax,'r',t,ay,'g',t,az,'b', linewidth=0.5)
        subplot1.set(xlabel="Time in s",ylabel="Acceleration in m/s^2")
        subplot1.set(ylim=[-10,10])
        subplot1.legend(["X", "Y", "Z"], loc='upper right')

        subplot2.clear()
        subplot2.plot(t,wx,'r',t,wy,'g',t,wz,'b', linewidth=0.5)
        subplot2.set(xlabel="Time in s",ylabel="Angular velocity in deg/s")
        subplot2.set(ylim=[-90,90])
        subplot2.legend(["X", "Y", "Z"], loc='upper right')

        if not plt.fignum_exists("IMU Plot"):
            break
        plt.pause(0.001)

    shutdownEvent.set()
    serialProcess.join()
