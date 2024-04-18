#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include <fstream>

using json = nlohmann::json;


int main(int argc, char *argv[])
{
    std::ifstream configFile(CONFIG_JSON_FILE_PATH, std::ifstream::in);
    json config = json::parse(configFile);

    cv::Mat frame;
    cv::VideoCapture cap;

    int apiPreference = cv::CAP_ANY;
#ifdef LINUX_OS
    apiPreference = cv::CAP_V4L;
#endif

    cap.open(config["camera_index"].get<int>(), apiPreference);
    cap.set(cv::CAP_PROP_FRAME_WIDTH, config["camera_width"].get<int>());
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, config["camera_height"].get<int>());
    int fourcc = cv::VideoWriter::fourcc('B', 'G', 'R', '3');
    cap.set(cv::CAP_PROP_FOURCC, fourcc);

    if (!cap.isOpened()) {
        std::cerr << "Error: Unable to open camera!" << std::endl;
        return -1;
    }
 
    int imageSeq = 0;
    for (;;) {
        cap.read(frame);

        if (frame.empty()) {
            std::cerr << "Error: Blank frame grabbed!" << std::endl;
            break;
        }

        cv::imshow("Stereo Image", frame);

        std::cout << "Image " << imageSeq++ << " received with size " << frame.cols << " x " << frame.rows << "." << std::endl;

        // esc to quit
        if (cv::waitKey(1) == 27) {
            break;
        }
    }
    
    return 0;
}
