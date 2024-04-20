import json
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Plot IMU log.')
parser.add_argument(dest='file', type=str, help='Input file with IMU JSON messages.')
args = parser.parse_args()

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

file = open(args.file, 'r')

while True:
    line = file.readline()

    if not line:
        break

    try:
        data = json.loads(line)
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

subplot1.clear()
subplot1.plot(t,ax,'r',t,ay,'g',t,az,'b', linewidth=0.5)
subplot1.set(xlabel="Time in s",ylabel="Acceleration in m/s^2")
subplot1.set(ylim=[-12,12])
subplot1.legend(["X", "Y", "Z"], loc='upper right')

subplot2.clear()
subplot2.plot(t,wx,'r',t,wy,'g',t,wz,'b', linewidth=0.5)
subplot2.set(xlabel="Time in s",ylabel="Angular velocity in deg/s")
subplot2.set(ylim=[-100,100])
subplot2.legend(["X", "Y", "Z"], loc='upper right')

plt.show()
