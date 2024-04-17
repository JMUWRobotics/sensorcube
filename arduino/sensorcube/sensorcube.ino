#include <ArduinoJson.h>
#include "RTC.h"
#include <Wire.h>
#include "Arduino_NineAxesMotion.h"
#include <vl53lx_class.h>
#include "DFRobot_BMP280.h"

struct MessageSelection
{
  bool heartbeat = true;
  bool imu_raw = false;
  bool imu_linear = false;
  bool imu_euler = false;
  bool imu_quaternion = false;
  bool tof_raw = false;
  bool pressure_raw = false;
  bool gnss_raw = false;
} messageSelection;

const size_t MAX_DATA_LENGTH = 400;
char buffer[MAX_DATA_LENGTH + 1];

unsigned long seqText = 0;

RTCTime startTime;
StaticJsonDocument<400> doc;
NineAxesMotion imu;
VL53LX tof(&Wire1, A1);
DFRobot_BMP280_IIC bmp(&Wire1, DFRobot_BMP280_IIC::eSdoLow);

void heartbeat()
{
  static unsigned long lastTime = millis();
  static unsigned long seq = 0;

  if (messageSelection.heartbeat && (millis() - lastTime) >= 1000) {  
    lastTime = millis();

    RTCTime currentTime;
    RTC.getTime(currentTime);

    doc.clear();
    doc["msg"] = "heartbeat";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seq++;
    serializeJson(doc, Serial);
    Serial.println();
  }
}

void imu_raw()
{
  static unsigned long lastTime = millis();
  static unsigned long seq = 0;

  if (messageSelection.imu_raw && (millis() - lastTime) >= 10) {
    lastTime = millis();

    RTCTime currentTime;
    RTC.getTime(currentTime);
    imu.updateAccel();
    imu.updateGyro();
    imu.updateMag();

    doc.clear();
    doc["msg"] = "imu_raw";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seq++;
    doc["ax"] = imu.readAccelX();
    doc["ay"] = imu.readAccelY();
    doc["az"] = imu.readAccelZ();
    doc["wx"] = imu.readGyroX();
    doc["wy"] = imu.readGyroY();
    doc["wz"] = imu.readGyroZ();
    doc["mx"] = imu.readMagX();
    doc["my"] = imu.readMagY();
    doc["mz"] = imu.readMagZ();
    serializeJson(doc, Serial);
    Serial.println();
  }
}

void imu_linear()
{
  static unsigned long lastTime = millis();
  static unsigned long seq = 0;

  if (messageSelection.imu_linear && (millis() - lastTime) >= 10) {
    lastTime = millis();

    RTCTime currentTime;
    RTC.getTime(currentTime);
    imu.updateLinearAccel();
    imu.updateGyro();
    imu.updateMag();

    doc.clear();
    doc["msg"] = "imu_linear";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seq++;
    doc["lx"] = imu.readLinearAccelX();
    doc["ly"] = imu.readLinearAccelY();
    doc["lz"] = imu.readLinearAccelZ();
    doc["wx"] = imu.readGyroX();
    doc["wy"] = imu.readGyroY();
    doc["wz"] = imu.readGyroZ();
    doc["mx"] = imu.readMagX();
    doc["my"] = imu.readMagY();
    doc["mz"] = imu.readMagZ();
    serializeJson(doc, Serial);
    Serial.println();
  }
}

void imu_euler()
{
  static unsigned long lastTime = millis();
  static unsigned long seq = 0;

  if (messageSelection.imu_euler && (millis() - lastTime) >= 10) {
    lastTime = millis();

    RTCTime currentTime;
    RTC.getTime(currentTime);
    imu.updateEuler();

    doc.clear();
    doc["msg"] = "imu_euler";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seq++;
    doc["heading"] = imu.readEulerHeading();
    doc["roll"] = imu.readEulerRoll();
    doc["pitch"] = imu.readEulerPitch();
    serializeJson(doc, Serial);
    Serial.println();
  }
}

void imu_quaternion()
{
  static unsigned long lastTime = millis();
  static unsigned long seq = 0;

  if (messageSelection.imu_quaternion && (millis() - lastTime) >= 10) {
    lastTime = millis();

    RTCTime currentTime;
    RTC.getTime(currentTime);
    imu.updateQuat();

    doc.clear();
    doc["msg"] = "imu_quaternion";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seq++;
    doc["qx"] = imu.readQuatX() / 1000.0;
    doc["qy"] = imu.readQuatY() / 1000.0;
    doc["qz"] = imu.readQuatZ() / 1000.0;
    doc["qw"] = imu.readQuatW() / 1000.0;
    serializeJson(doc, Serial);
    Serial.println();
  }
}

void tof_raw()
{
  static unsigned long lastTime = millis();
  static unsigned long seq = 0;
  int status = 0;

  if (messageSelection.tof_raw && (millis() - lastTime) >= 1) {
    lastTime = millis();

    uint8_t NewDataReady = 0;
    status = tof.VL53LX_GetMeasurementDataReady(&NewDataReady);

    if ((!status) && (NewDataReady != 0)) {
      RTCTime currentTime;
      RTC.getTime(currentTime);

      VL53LX_MultiRangingData_t multiRangingData;

      status = tof.VL53LX_GetMultiRangingData(&multiRangingData);
      int numberOfObjects = multiRangingData.NumberOfObjectsFound;

      doc.clear();
      doc["msg"] = "tof_raw";
      doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
      doc["seq"] = seq++;
      doc["objects"] = numberOfObjects;
      JsonArray range = doc.createNestedArray("range");
      for (int i = 0; i < numberOfObjects; i++) {
        range.add(multiRangingData.RangeData[i].RangeMilliMeter / 1000.0);
      }
      JsonArray signal = doc.createNestedArray("signal");
      for (int i = 0; i < numberOfObjects; i++) {
        signal.add(multiRangingData.RangeData[i].SignalRateRtnMegaCps / 65536.0);
      }
      serializeJson(doc, Serial);
      Serial.println();

      if (status == 0) {
        status = tof.VL53LX_ClearInterruptAndStartMeasurement();
      }
    }
  }
}

void pressure_raw()
{
  static unsigned long lastTime = millis();
  static unsigned long seq = 0;

  if (messageSelection.pressure_raw && (millis() - lastTime) >= 1000) {
    lastTime = millis();

    RTCTime currentTime;
    RTC.getTime(currentTime);
    float temperature = bmp.getTemperature();
    uint32_t pressure = bmp.getPressure();

    doc.clear();
    doc["msg"] = "pressure_raw";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seq++;
    doc["temperature"] = serialized(String(temperature,2));
    doc["pressure"] = pressure;
    serializeJson(doc, Serial);
    Serial.println();
  }
}

void gnss_raw()
{
  if (messageSelection.gnss_raw && Serial1.available()) {
    Serial.write(Serial1.read());
  }
}

bool add_data(char nextChar)
{  
  static uint8_t currentIndex = 0;

  if (nextChar == '\n') {
      buffer[currentIndex] = '\0';
      currentIndex = 0;
      return true;
  }

  buffer[currentIndex] = nextChar;
  currentIndex++;

  if (currentIndex >= MAX_DATA_LENGTH) {
    buffer[MAX_DATA_LENGTH] = '\0';
    currentIndex = 0;
    return true;
  }

  return false;
}

void process_command()
{
  StaticJsonDocument<400> docCommand;
  DeserializationError error = deserializeJson(docCommand, buffer);

  if (error) {
    RTCTime currentTime;
    RTC.getTime(currentTime);
    doc.clear();
    doc["msg"] = "text";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seqText++;
    doc["text"] = "Failed to deserialize command!";
    serializeJson(doc, Serial);
    Serial.println();
    
    return;
  }

  if (docCommand.containsKey("messages")) {
    messageSelection.heartbeat = false;
    messageSelection.imu_raw = false;
    messageSelection.imu_linear = false;
    messageSelection.imu_euler = false;
    messageSelection.imu_quaternion = false;
    messageSelection.tof_raw = false;
    messageSelection.pressure_raw = false;
    messageSelection.gnss_raw = false;

    JsonArray array = docCommand["messages"].as<JsonArray>();
    for (JsonVariant v : array) {
      std::string s = v.as<std::string>();

      if (s.compare("heartbeat") == 0) { messageSelection.heartbeat = true; }
      if (s.compare("imu_raw") == 0) { messageSelection.imu_raw = true; }
      if (s.compare("imu_linear") == 0) { messageSelection.imu_linear = true; }
      if (s.compare("imu_euler") == 0) { messageSelection.imu_euler = true; }
      if (s.compare("imu_quaternion") == 0) { messageSelection.imu_quaternion = true; }
      if (s.compare("tof_raw") == 0) { messageSelection.tof_raw = true; }
      if (s.compare("pressure_raw") == 0) { messageSelection.pressure_raw = true; }
      if (s.compare("gnss_raw") == 0) { messageSelection.gnss_raw = true; }
    }
  }

  if (docCommand.containsKey("time")) {
    RTCTime newTime;
    newTime.setUnixTime(docCommand["time"].as<unsigned long>());
    RTC.setTime(newTime);
    startTime.setUnixTime(docCommand["time"].as<unsigned long>() - (millis() / 1000ul));

    RTCTime currentTime;
    RTC.getTime(currentTime);
    doc.clear();
    doc["msg"] = "text";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seqText++;
    doc["text"] = "Updated RTC!";
    serializeJson(doc, Serial);
    Serial.println();
  }
}

void process_serial()
{
  bool dataReady = false;

  while (Serial.available() > 0) {
      char data = Serial.read();
      dataReady = add_data(data);
      if (dataReady) {
        process_command();
      }
  }
}

void setup()
{
  RTC.begin();
  RTC.getTime(startTime);
  RTC.setTime(startTime);

  Serial.begin(921600);

  Wire.begin();
  Wire.setClock(I2C_MASTER_RATE_FAST);
  imu.initSensor();
  imu.setOperationMode(OPERATION_MODE_NDOF);
  imu.setUpdateMode(MANUAL);

  Wire1.begin();
  tof.begin();
  tof.VL53LX_Off();
  tof.InitSensor(0x12);
  tof.VL53LX_StartMeasurement();
  
  bmp.reset();
  while(bmp.begin() != DFRobot_BMP280_IIC::eStatusOK) {
    RTCTime currentTime;
    RTC.getTime(currentTime);
    doc.clear();
    doc["msg"] = "text";
    doc["stamp"] = serialized(String(startTime.getUnixTime() + millis() / 1000.0, 3));
    doc["seq"] = seqText++;
    doc["text"] = "BMP280 begin failed!";
    serializeJson(doc, Serial);
    Serial.println();

    delay(1000);
  }

  Serial1.begin(9600);

  // start aligned with full seconds
  while (millis() % 1000 != 0) {}
}

void loop()
{
  heartbeat();
  imu_raw();
  imu_linear();
  imu_euler();
  imu_quaternion();
  tof_raw();
  pressure_raw();
  gnss_raw();

  process_serial();
}
