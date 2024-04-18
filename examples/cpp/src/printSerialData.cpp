#include <asio/serial_port.hpp>
#include <asio/read_until.hpp>
#include <asio/streambuf.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include <fstream>

using json = nlohmann::json;


sig_atomic_t volatile running = true;
void sigHandler(int signum)
{
    if (signum == SIGINT) {
        running = false;
    }
}

int main(int argc, char *argv[])
{
    signal(SIGINT, &sigHandler);

    std::ifstream configFile(CONFIG_JSON_FILE_PATH, std::ifstream::in);
    json config = json::parse(configFile);

    std::cout << "Opening port " << config["serial_port"].get<std::string>() << " with baudrate " << config["serial_baudrate"].get<int>() << "." << std::endl;
    asio::io_context ctx;
    asio::serial_port sensorcube(ctx);
    sensorcube.open(config["serial_port"].get<std::string>());
    sensorcube.set_option(asio::serial_port::baud_rate(config["serial_baudrate"].get<int>()));

    asio::streambuf buf;
    asio::read_until(sensorcube, buf, "\n");

    while (running) {
        asio::streambuf buf;
        try {
            asio::read_until(sensorcube, buf, "\n");
        } catch (...) {
            if (running) {
                std::cerr << "Error: Failed reading from serial port!" << std::endl;
            }
            continue;
        }

        std::string line = asio::buffer_cast<const char*>(buf.data());
        line.erase(line.find_last_not_of(" \n\r\t")+1);

        std::cout << line << std::endl;
    }

    return 0;
}
