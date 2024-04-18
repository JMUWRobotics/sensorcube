import cv2
import os
import json

def showWebcam():
    configFile = open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json')
    config = json.load(configFile)

    cam = None
    if os.name == 'nt':
        cam = cv2.VideoCapture(config["camera_index"])
    else:
        cam = cv2.VideoCapture(config["camera_index"], cv2.CAP_V4L)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, config["camera_width"])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config["camera_height"])
    fourcc = cv2.VideoWriter_fourcc('B', 'G', 'R', '3')
    cam.set(cv2.CAP_PROP_FOURCC, fourcc)

    imageSeq = 0
    fileSeq = 0
    while True:
        ret_val, img = cam.read()
        cv2.imshow('Stereo Image', img)

        height, width = img.shape[:2]
        print("Image " + str(imageSeq) + " received with size " + str(width) + " x " + str(height) + ".")
        imageSeq = imageSeq + 1

        key = cv2.waitKey(1)
        if key == 27: # esc to quit
            break
        elif key == 32: # space to save image
            print("Saving image " + "\"stereo" + str(fileSeq).zfill(3) + ".png\".")
            cv2.imwrite("stereo" + str(fileSeq).zfill(3) + ".png", img)
            fileSeq = fileSeq + 1

    cv2.destroyAllWindows()

def main():
    showWebcam()

if __name__ == '__main__':
    main()
