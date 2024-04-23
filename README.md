# Sensor Cube
Documentation, design and example code for the Sensor Cube used for teaching at the Robotics Lab of the Julius Maximilian University of Würzburg.
* The sensors can be used without specialized drivers. The stereo camera behaves like a webcam. The Arduino offers a virtual serial port over USB with sensor messages in JSON format.
* Contact: Michael Bleier (michael.bleier@uni-wuerzburg.de)

![Image of Sensor Cube](doc/images/sensorcube.jpg?raw=true "Sensor Cube")

## Sensors and Kit
* Stereo camera module (https://www.elpcctv.com/elp-4mp-3840x1080p-60fps-synchronous-dual-lens-usb-camera-module-with-no-distortion-85-degree-lens-p-406.html)
* Arduino UNO R4 WiFi
  * U-blox NEO-M8T timing GNSS module (https://www.u-blox.com/en/product/neolea-m8t-series, https://gnss.store/neo-m8t-timing-gnss-modules/53-elt0040.html)
  * ST VL53L3CX Time-of-Flight multi-target distance sensor (https://www.st.com/en/imaging-and-photonics-solutions/vl53l3cx.html, https://www.pololu.com/product/3416)
  * Bosch BMP280 pressure and temperature sensor (https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp280/, https://www.berrybase.de/bmp280-breakout-board-2in1-sensor-fuer-temperatur-und-luftdruck)
  * Bosch BNO055 Inertial Measurement Unit (https://www.bosch-sensortec.com/products/smart-sensor-systems/bno055/, https://docs.arduino.cc/hardware/9-axis-motion-shield/)
* Red Line Laser 650nm (https://www.laserfuchs.de/p/70134933)
* Calibration Board

## Datasheets
* U-blox NEO-M8T timing GNSS module: https://www.u-blox.com/sites/default/files/documents/NEO-LEA-M8T-FW3_DataSheet_UBX-15025193.pdf
* ST VL53L3CX Time-of-Flight multi-target distance sensor: https://www.st.com/resource/en/datasheet/vl53l3cx.pdf
* Bosch BMP280 pressure and temperature sensor: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf
* Bosch BNO055 Inertial Measurement Unit: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bno055-ds000.pdf

## Known Issues
* The Arduino UNO R4 WiFi uses the internal oscillator instead of an external crystal as a clock source for the Real Time Clock (RTC). This causes significant time drift.
