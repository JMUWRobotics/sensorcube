import cv2
import numpy as np
import os
import json

def showWebcam():
    # load config file (same directory as this file)
    configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/../../config.json')
    config = json.load(configFile)
    
    # open and configure video capture
    cam = None
    if os.name == 'nt':
        cam = cv2.VideoCapture(config["camera_index"])
    else:
        cam = cv2.VideoCapture(config["camera_index"], cv2.CAP_V4L)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, config["camera_width"])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config["camera_height"])
    fourcc = cv2.VideoWriter_fourcc('B', 'G', 'R', '3')
    cam.set(cv2.CAP_PROP_FOURCC, fourcc)
    
    seq = 0

    if not os.path.isfile("calibration.json"):
        print("No calibration.json file!")
        return

    fs = cv2.FileStorage("calibration.json", cv2.FILE_STORAGE_READ)
    K1 = fs.getNode("stereo").getNode("K1").mat()
    D1 = fs.getNode("stereo").getNode("D1").mat()
    K2 = fs.getNode("stereo").getNode("K2").mat()
    D2 = fs.getNode("stereo").getNode("D2").mat()
    R1 = fs.getNode("stereo").getNode("R1").mat()
    R2 = fs.getNode("stereo").getNode("R2").mat()
    P1 = fs.getNode("stereo").getNode("P1").mat()
    P2 = fs.getNode("stereo").getNode("P2").mat()
    Q = fs.getNode("stereo").getNode("Q").mat()

    while True:
        ret_val, img = cam.read()

        left = img[0:img.shape[0], 0:int(img.shape[1]/2)]
        leftGray = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
        image_size_left = leftGray.shape[::-1]
        leftMapX, leftMapY = cv2.initUndistortRectifyMap(K1, D1, R1, P1, image_size_left, cv2.CV_32FC1)
        leftGray = cv2.remap(leftGray, leftMapX, leftMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

        right = img[0:img.shape[0], int(img.shape[1]/2):img.shape[1]]
        rightGray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
        image_size_right = rightGray.shape[::-1]
        rightMapX, rightMapY = cv2.initUndistortRectifyMap(K2, D2, R2, P2, image_size_right, cv2.CV_32FC1)
        rightGray = cv2.remap(rightGray, rightMapX, rightMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 500
        params.maxArea = 50000
        params.filterByCircularity = True
        params.filterByConvexity = False
        params.filterByInertia = False
        params.minCircularity = 0.9
        detector = cv2.SimpleBlobDetector_create(params)

        leftKeypoints = detector.detect(leftGray)
        leftGray = cv2.drawKeypoints(leftGray, leftKeypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        rightKeypoints = detector.detect(rightGray)
        rightGray = cv2.drawKeypoints(rightGray, rightKeypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        if (len(leftKeypoints) == 1) and (len(rightKeypoints) == 1):
            print("Single blob detected in right and left image:")
            print(f"    Left image: {np.round(leftKeypoints[0].pt,3)}")
            print(f"    Right image: {np.round(rightKeypoints[0].pt,3)}")

        displayImg = cv2.hconcat([leftGray, rightGray])
        proportion = max(displayImg.shape) / 1000.0
        displayImg = cv2.resize(displayImg, (int(displayImg.shape[1]/proportion), int(displayImg.shape[0]/proportion)))

        cv2.imshow('Rectified stereo Image with detected blobs', displayImg)
        key = cv2.waitKey(1)
        if key == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    showWebcam()

if __name__ == '__main__':
    main()
