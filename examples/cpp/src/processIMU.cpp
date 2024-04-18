#include <nlohmann/json.hpp>
#include <Eigen/Core>
#include <iostream>
#include <fstream>

using json = nlohmann::json;


void readIMU(const std::string &infile, Eigen::VectorXd &t, Eigen::VectorXd &ax, Eigen::VectorXd &ay,
    Eigen::VectorXd &az, Eigen::VectorXd &wx, Eigen::VectorXd &wy, Eigen::VectorXd &wz)
{
    std::ifstream ifs(infile, std::ifstream::in);

    std::vector<double> _t, _ax, _ay, _az, _wx, _wy, _wz;

    std::string line;
    while (std::getline(ifs, line)) {
        json data = json::parse(line);

        if (!data.contains("msg")) {
            continue;
        }

        if (data["msg"].get<std::string>().compare("imu_raw") == 0) {
            double stamp = data["stamp"].get<double>();
            unsigned long seq = data["seq"].get<unsigned long>();
            _t.push_back(data["stamp"].get<double>());
            _ax.push_back(data["ax"].get<double>());
            _ay.push_back(data["ay"].get<double>());
            _az.push_back(data["az"].get<double>());
            _wx.push_back(data["wx"].get<double>());
            _wy.push_back(data["wy"].get<double>());
            _wz.push_back(data["wz"].get<double>());
        }
    }

    t = Eigen::Map<Eigen::VectorXd>(_t.data(), _t.size());
    ax = Eigen::Map<Eigen::VectorXd>(_ax.data(), _ax.size());
    ay = Eigen::Map<Eigen::VectorXd>(_ay.data(), _ay.size());
    az = Eigen::Map<Eigen::VectorXd>(_az.data(), _az.size());
    wx = Eigen::Map<Eigen::VectorXd>(_wx.data(), _wx.size());
    wy = Eigen::Map<Eigen::VectorXd>(_wy.data(), _wy.size());
    wz = Eigen::Map<Eigen::VectorXd>(_wz.data(), _wz.size());
}

int main(int argc, char *argv[])
{
    if (argc <= 1) {
        std::cout << "Input file required!" << std::endl;
        std::cout << "Usage: processIMU <input file>" << std::endl;
        return -1;
    }

    Eigen::VectorXd t, ax, ay, az, wx, wy, wz;
    readIMU(std::string(argv[1]), t, ax, ay, az, wx, wy, wz);

    std::cout << "Loaded " << t.size() << " IMU messages." << std::endl;

    // process IMU data

    // compute norm of the acceleration vector
    //a = np.sqrt(ax*ax + ay*ay + az*az)
    Eigen::VectorXd a = (ax.array() * ax.array() + ay.array() * ay.array() + az.array() * az.array()).cwiseSqrt();

    std::cout << "a = " << std::endl << a << std::endl;

    return 0;
}
