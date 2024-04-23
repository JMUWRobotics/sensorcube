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

## Configuration
In the root directory is a configuration file _"config.json"_. Please make sure to set _"serial\_port"_ (typically _"/dev/ttyACM[0-9]"_ on Linux or _"COM[1-9]"_ on Windows) and the correct _"camera\_index"_ for the stereo camera.

```
"config.json":
  {
    "serial_port" : "/dev/ttyACM0",
    "serial_baudrate" : 921600,
    "camera_index" : 0,
    "camera_width" : 1600,
    "camera_height": 800
  }
```

The Python examples load this file relative to the _*.py_ source files. For the C++ examples CMake sets the path relative to the project source dir and bakes the path in the executables.

## Using Python
Set up your Python programming environment.

* Install Python3. On GNU/Linux you can use your favorite package manager to install Python, e.g., on Debian/Ubuntu install the package _python3_.
* On GNU/Linux use your favorite package manager to install the Python dependencies, e.g., on Debian/Ubuntu install the packages _python3-opencv, python3-serial, python3-matplotlib, python3-numpy_.
  
  Or, use _pip_ to install the dependencies:
```
  $ pip install opencv-python pyserial matplotlib numpy
```
* Inspect the Python examples in the directory _"examples/python"_.

## Using C++
Set up your C++ programming environment.

* Set up your C++ programming environment and compiler, e.g., _GCC_ on GNU/Linux or _Visual Studio/MSVC_ on Windows.
* Install the _OpenCV_ library.

  For image processing we will be using the _OpenCV_ library which is available	across platforms. It is recommended to use version 4.5.4. However, any version newer than 4.4.0 should be fine to complete the assignments.

  Please refer to: https://docs.opencv.org/4.5.4/df/d65/tutorial_table_of_content_introduction.html

  GNU/Linux: Use your favorite package manager to install OpenCV, e.g., on Debian/Ubuntu install the package _libopencv-dev_.

  Windows: You can download the _OpenCV_ binary release from https://opencv.org/releases/. You need to add the path to the unpacked directory _"opencv/build/x64/vc16/bin"_ to your System Path, such that the _OpenCV_ DLLs are found.

	Of course it is also possible to compile OpenCV yourself or use other ways for the installation as listed in the _OpenCV_ documentation.
* Install the _CMake_ build system.

  GNU/Linux: Use your favorite package manager to install _CMake_, e.g., on Debian/Ubuntu install the package _cmake_.

  Windows: You can download _CMake_ from https://cmake.org/download/.
  
* All other library dependencies (_Eigen3_, _Nlohmann JSON_, and _Asio_) are automatically downloaded by _CMake_. Inspect the _"examples/cpp/CMakeLists.txt"_ project file.
* Build the C++ examples. The recommended way of building a project with _CMake_ is by doing an out-of-source build. This can be done like this:
```
  $ cd examples/cpp
  $ mkdir build && cd build
  $ cmake ..
  $ make
```
  If _OpenCV_ is not installed in the standard paths, you might need to set the _OpenCV_ directory:
```
  $ cmake -DOpenCV_DIR=<Path to directory OpenCVConfig.cmake> ..
```
  If you are using the _OpenCV_ binary release on Windows, you need to specify the path to the unpacked directory _"opencv/build/x64/vc16/lib"_.

  Different _CMake_ Generators are available, such as _Unix Makefiles_ or _Ninja_. On Windows CMake can create, for example, _Visual Studio_ project files, _NMake_, or _Unix Makefiles_: https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html
	
  For example, on Windows you can run from the Visual Studio developer command prompt:
```
  $ cmake -G "NMake Makefiles" ..
  $ nmake
```
* Inspect the C++ examples in the directory _"examples/cpp/src"_.

## Known Issues
* The Arduino UNO R4 WiFi uses the internal oscillator instead of an external crystal as a clock source for the Real Time Clock (RTC). This causes significant time drift.
