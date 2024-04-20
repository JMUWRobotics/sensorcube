import json
import argparse
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
import numpy as np
import math

def readIMU(infile):
    t = []
    ax = []
    ay = []
    az = []
    wx = []
    wy = []
    wz = []

    file = open(infile, 'r')

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

    return np.array(t), np.array(ax), np.array(ay), np.array(az), np.array(wx), np.array(wy), np.array(wz)

parser = argparse.ArgumentParser(description='Compute FFT of IMU log.')
parser.add_argument(dest='file', type=str, help='Input file with IMU JSON messages.')
args = parser.parse_args()

t, ax, ay, az, wx, wy, wz = readIMU(args.file)

print('Loaded ' + str(len(t)) + ' IMU messages.')

# compute norm of the acceleration vector
a = np.sqrt(ax*ax + ay*ay + az*az)
#a = a - np.mean(a)

x = a
sr = 100 # sampling rate

# compute fft
X = fft(x)
N = len(X)
n = np.arange(N)
T = N / sr
freq = n / T

print("T = " + str(T) + " s.")


plt.figure("FFT of acceleration", figsize = (12, 6))

# plot signal
plt.subplot(121)
plt.plot(t - t[0], x, 'r')
plt.xlabel('Time in s')
plt.ylabel('Amplitude')

# plott fft
plt.subplot(122)
plt.stem(freq, np.abs(X), linefmt='b', markerfmt=" ", basefmt="-b")
plt.xlabel('Frequency in Hz')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, sr)

plt.show()
