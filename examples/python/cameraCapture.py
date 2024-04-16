import cv2

def showWebcam():
    seq = 0
    cam = cv2.VideoCapture(1, cv2.CAP_V4L)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cam.set(cv2.CAP_PROP_FPS, 30)
    fourcc = cv2.VideoWriter_fourcc('B', 'G', 'R', '3')
    cam.set(cv2.CAP_PROP_FOURCC, fourcc)
    while True:
        ret_val, img = cam.read()
        cv2.imshow('Stereo Image', img)
        height, width = img.shape[:2]
        print("Image: ", width, "x", height)
        key = cv2.waitKey(1)
        if key == 27: 
            break  # esc to quit
        elif key == 32:
            cv2.imwrite("stereo" + str(seq).zfill(3) + ".png", img)
            left = img[0:600,0:800]
            cv2.imwrite("left" + str(seq).zfill(3) + ".png", left)
            right = img[0:600,800:1600]
            cv2.imwrite("right" + str(seq).zfill(3) + ".png", right)
            seq = seq + 1
    cv2.destroyAllWindows()

def main():
    showWebcam()

if __name__ == '__main__':
    main()
