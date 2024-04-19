cmake_minimum_required(VERSION 3.11)
project(SensorCubeExamples)
include(FetchContent)


set(CMAKE_CXX_STANDARD 11)
if(NOT CMAKE_BUILD_TYPE)
    message(STATUS "Setting build type to RelWithDebInfo")
    set(CMAKE_BUILD_TYPE "RelWithDebInfo")
endif()


# OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# Nlohmann JSON
FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz URL_HASH MD5=c23a33f04786d85c29fda8d16b5f0efd)
FetchContent_MakeAvailable(json)

# Eigen
FetchContent_Declare(eigen URL https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz URL_HASH MD5=4c527a9171d71a72a9d4186e65bea559)
FetchContent_MakeAvailable(eigen)

# Asio
FetchContent_Declare(asio URL https://github.com/chriskohlhoff/asio/archive/refs/tags/asio-1-30-2.tar.gz URL_HASH MD5=5ae7dc2b2ee13bc49144f2f867eab15c)
FetchContent_MakeAvailable(asio)
FetchContent_GetProperties(asio)
if(NOT asio_POPULATED)
  FetchContent_Populate(asio)
endif()
add_library(asio INTERFACE)
target_include_directories(asio INTERFACE ${asio_SOURCE_DIR}/asio/include)
find_package(Threads)
target_link_libraries(asio INTERFACE Threads::Threads)


# set variable for the C preprocessor to detect the operatong system
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
  add_compile_definitions("LINUX_OS")
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  add_compile_definitions("MACOS_OS")
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
  add_compile_definitions("WINDOWS_OS")
endif()

# set variable for the C preprocessor with the path to the config file
set(CONFIG_JSON_FILE_PATH ${CMAKE_SOURCE_DIR}/../../config.json)
message("Config file path: " ${CONFIG_JSON_FILE_PATH})
add_compile_definitions(CONFIG_JSON_FILE_PATH="${CONFIG_JSON_FILE_PATH}")


# showCamera
add_executable(showCamera src/showCamera.cpp)
target_link_libraries(showCamera nlohmann_json::nlohmann_json ${OpenCV_LIBS})

# printSerialData
add_executable(printSerialData src/printSerialData.cpp)
target_link_libraries(printSerialData nlohmann_json::nlohmann_json asio)

# serializeHeartbeat
add_executable(serializeHeartbeat src/serializeHeartbeat.cpp)
target_link_libraries(serializeHeartbeat nlohmann_json::nlohmann_json asio)

# processIMU
add_executable(processIMU src/processIMU.cpp)
target_link_libraries(processIMU nlohmann_json::nlohmann_json Eigen3::Eigen)
