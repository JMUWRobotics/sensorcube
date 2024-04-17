import cv2
import os
import json

def showWebcam():
    # load config file (same directory as this file)
    configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/config.json')
    config = json.load(configFile)
    
    # open and configure video capture
    cam = cv2.VideoCapture(config["camera_index"], cv2.CAP_V4L)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, config["camera_width"])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config["camera_height"])
    fourcc = cv2.VideoWriter_fourcc('B', 'G', 'R', '3')
    cam.set(cv2.CAP_PROP_FOURCC, fourcc)

    imageSeq = 0
    while True:
        # read and display image
        ret_val, img = cam.read()
        cv2.imshow('Stereo Image', img)

        # print size of image
        height, width = img.shape[:2]
        print("Image " + str(imageSeq) + " received with size " + str(width) + " x " + str(height) + ".")
        imageSeq = imageSeq +1

        # process key press
        key = cv2.waitKey(1)
        if key == 27: # esc to quit
            break

    cv2.destroyAllWindows()

def main():
    showWebcam()

if __name__ == '__main__':
    main()
