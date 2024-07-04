import numpy as np
import cv2
from cv2 import aruco
import argparse
import glob
import os.path
import click

def is_opencv47():
    (major, minor, _) = cv2.__version__.split(".")
    return int(major) >= 4 and int(minor) >= 7

if is_opencv47():
    print("OpenCV >= 4.7.0 detected. Using new API.")
else:
    print("OpenCV < 4.7.0 detected. Using old API.")

parser = argparse.ArgumentParser(description='Compute camera calibration.')
parser.add_argument(dest='folder', type=str, help='Folder with stereo***.png images.')
args = parser.parse_args()

CHARUCOBOARD_ROWCOUNT = 6
CHARUCOBOARD_COLCOUNT = 9
CHARUCOBOARD_SQUARE_LENGTH = 0.030
CHARUCOBOARD_MARKER_SIZE = 0.022

if is_opencv47():
    dictionary = cv2.aruco.getPredefinedDictionary(aruco.DICT_6X6_1000)
    board = cv2.aruco.CharucoBoard((CHARUCOBOARD_COLCOUNT, CHARUCOBOARD_ROWCOUNT), CHARUCOBOARD_SQUARE_LENGTH, CHARUCOBOARD_MARKER_SIZE, dictionary)
    board.setLegacyPattern(True)
    detctorparams = cv2.aruco.DetectorParameters()
    charucoparams = cv2.aruco.CharucoParameters()
    charucoparams.tryRefineMarkers = True
    detector = cv2.aruco.CharucoDetector(board, charucoparams, detctorparams)
else:
    dictionary = aruco.Dictionary_get(aruco.DICT_6X6_1000)
    board = aruco.CharucoBoard_create(
        squaresX=CHARUCOBOARD_COLCOUNT,
        squaresY=CHARUCOBOARD_ROWCOUNT,
        squareLength=0.030,
        markerLength=0.022,
        dictionary=dictionary)

images = glob.glob(args.folder + '/stereo*.png')

if len(images) < 3:
    print("Calibration was unsuccessful. Too few images were found.")
    exit()

image_size_left = None
corners_all_left = []
ids_all_left = []
image_left = []

image_size_right = None
corners_all_right = []
ids_all_right = []
image_right = []

for iname in images:
    print(iname)
    img = cv2.imread(iname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    left = img[0:img.shape[0], 0:int(img.shape[1]/2)]
    leftGray = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    if len(image_left) < 1:
        image_left = left.copy()

    if is_opencv47():
        charuco_corners, charuco_ids, corners, ids = detector.detectBoard(leftGray)
    else:
        corners, ids, _ = aruco.detectMarkers(
            image=leftGray,
            dictionary=dictionary)
        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=leftGray,
            board=board)
    left = aruco.drawDetectedMarkers(
        image=left, 
        corners=corners)
    if len(charuco_ids) > 1:
        corners_all_left.append(charuco_corners)
        ids_all_left.append(charuco_ids)
        
        left = aruco.drawDetectedCornersCharuco(
            image=left,
            charucoCorners=charuco_corners,
            charucoIds=charuco_ids)

    if not image_size_left:
        image_size_left = leftGray.shape[::-1]

    right = img[0:img.shape[0], int(img.shape[1]/2):img.shape[1]]
    rightGray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    if len(image_right) < 1:
        image_right = right.copy()

    if is_opencv47():
        charuco_corners, charuco_ids, corners, ids = detector.detectBoard(rightGray)
    else:
        corners, ids, _ = aruco.detectMarkers(
            image=rightGray,
            dictionary=dictionary)
        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=rightGray,
            board=board)
    right = aruco.drawDetectedMarkers(
        image=right, 
        corners=corners)
    if len(charuco_ids) > 1:
        corners_all_right.append(charuco_corners)
        ids_all_right.append(charuco_ids)
        
        right = aruco.drawDetectedCornersCharuco(
            image=right,
            charucoCorners=charuco_corners,
            charucoIds=charuco_ids)

    if not image_size_right:
        image_size_right = rightGray.shape[::-1]

    displayImg = cv2.hconcat([left, right])
    proportion = max(displayImg.shape) / 1000.0
    displayImg = cv2.resize(displayImg,
        (int(displayImg.shape[1]/proportion), int(displayImg.shape[0]/proportion)))

    cv2.imshow('Detected ChArUco markers', displayImg)
    cv2.waitKey(100)

cv2.destroyAllWindows()

fs = None
if os.path.isfile("calibration.json"):
    if click.confirm('\nFile calibration.json exists. Overwrite?', default=True):
        fs = cv2.FileStorage("calibration.json", cv2.FILE_STORAGE_WRITE)
else:
    fs = cv2.FileStorage("calibration.json", cv2.FILE_STORAGE_WRITE)

ret, camera_matrix_left, dist_coeffs_left, rvecs, tvecs = aruco.calibrateCameraCharuco(
    charucoCorners=corners_all_left,
    charucoIds=ids_all_left,
    board=board,
    imageSize=image_size_left,
    cameraMatrix=None,
    distCoeffs=None)

print("\nLeft camera:")
print(f"Error: {ret}")
print("Camera matrix:")
print(camera_matrix_left)
print("Distortion coefficients:")
print(dist_coeffs_left)

new_camera_matrix_left, roi = cv2.getOptimalNewCameraMatrix(camera_matrix_left, dist_coeffs_left, image_size_left, 1, image_size_left)
undistorted_image_left = cv2.undistort(image_left, camera_matrix_left, dist_coeffs_left, None, new_camera_matrix_left)

if fs:
    fs.startWriteStruct('left', cv2.FileNode_MAP)
    fs.write(name='image_size',val=image_size_left)
    fs.write(name='camera_matrix',val=camera_matrix_left)
    fs.write(name='distortion_coefficients',val=dist_coeffs_left)
    fs.endWriteStruct()

ret, camera_matrix_right, dist_coeffs_right, rvecs, tvecs = aruco.calibrateCameraCharuco(
    charucoCorners=corners_all_right,
    charucoIds=ids_all_right,
    board=board,
    imageSize=image_size_right,
    cameraMatrix=None,
    distCoeffs=None)

print("\nRight camera:")
print(f"Error: {ret}")
print("Camera matrix:")
print(camera_matrix_right)
print("Distortion coefficients:")
print(dist_coeffs_right)

new_camera_matrix_right, roi = cv2.getOptimalNewCameraMatrix(camera_matrix_right, dist_coeffs_right, image_size_right, 1, image_size_right)
undistorted_image_right = cv2.undistort(image_right, camera_matrix_right, dist_coeffs_right, None, new_camera_matrix_right)

if fs:
    fs.startWriteStruct('right', cv2.FileNode_MAP)
    fs.write(name='image_size',val=image_size_right)
    fs.write(name='camera_matrix',val=camera_matrix_right)
    fs.write(name='distortion_coefficients',val=dist_coeffs_right)
    fs.endWriteStruct()

displayImg = cv2.vconcat([cv2.hconcat([image_left, image_right]), cv2.hconcat([undistorted_image_left, undistorted_image_right])])
proportion = max(displayImg.shape) / 1000.0
displayImg = cv2.resize(displayImg, (int(displayImg.shape[1]/proportion), int(displayImg.shape[0]/proportion)))


cv2.imshow('Original and undistorted image', displayImg)

obj_all = [];
pts_all_left = [];
pts_all_right = [];
for i in range(len(ids_all_left)):
    ids_left = ids_all_left[i]
    ids_right = ids_all_right[i]
    
    obj = None;
    pts_left = [];
    pts_right = [];
    
    for j in range(len(ids_left)):
        for k in range(len(ids_right)):
            if ids_right[k] == ids_left[j]:
                if obj is None:
                    if is_opencv47():
                        obj = board.getChessboardCorners()[ids_left[j][0]]
                    else:
                        obj = board.chessboardCorners[ids_left[j][0]]
                    pts_left = corners_all_left[i][j]
                    pts_right = corners_all_right[i][k]
                else:
                    if is_opencv47():
                        obj = np.vstack((obj, board.getChessboardCorners()[ids_left[j][0]]))
                    else:
                        obj = np.vstack((obj, board.chessboardCorners[ids_left[j][0]]))
                    pts_left = np.vstack((pts_left, corners_all_left[i][j]))
                    pts_right = np.vstack((pts_right, corners_all_right[i][k]))
    if len(obj) > 4:
        obj_all.append(obj)
        pts_all_left.append(pts_left)
        pts_all_right.append(pts_right)

ret, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(
    obj_all,
    pts_all_left,
    pts_all_right,
    camera_matrix_left, dist_coeffs_left, camera_matrix_right, dist_coeffs_right,
    image_size_left)

R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(K1, D1, K2, D2, image_size_left, R, T, flags=cv2.CALIB_ZERO_DISPARITY, alpha=0.9)

print("\nStereo:")
print(f"Error: {ret}")
print("R:")
print(R)
print("T:")
print(T)

if fs:
    fs.startWriteStruct('stereo', cv2.FileNode_MAP)
    fs.write(name='image_size',val=image_size_left)
    fs.write(name='K1',val=K1)
    fs.write(name='D1',val=D1)
    fs.write(name='K2',val=K2)
    fs.write(name='D2',val=D2)
    fs.write(name='R',val=R)
    fs.write(name='T',val=T)
    fs.write(name='E',val=E)
    fs.write(name='F',val=F)
    fs.write(name='R1',val=R1)
    fs.write(name='R2',val=R2)
    fs.write(name='P1',val=P1)
    fs.write(name='P2',val=P2)
    fs.write(name='Q',val=Q)
    fs.endWriteStruct()

leftMapX, leftMapY = cv2.initUndistortRectifyMap(K1, D1, R1, P1, image_size_left, cv2.CV_32FC1)
left_rectified = cv2.remap(image_left, leftMapX, leftMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
rightMapX, rightMapY = cv2.initUndistortRectifyMap(K2, D2, R2, P2, image_size_right, cv2.CV_32FC1)
right_rectified = cv2.remap(image_right, rightMapX, rightMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

displayImg = cv2.vconcat([cv2.hconcat([image_left, image_right]), cv2.hconcat([left_rectified, right_rectified])])
proportion = max(displayImg.shape) / 1000.0
displayImg = cv2.resize(displayImg, (int(displayImg.shape[1]/proportion), int(displayImg.shape[0]/proportion)))

cv2.imshow('Original and stereo rectified image', displayImg)
cv2.waitKey(0)

if fs:
    fs.release()