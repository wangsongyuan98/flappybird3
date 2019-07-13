from __future__ import print_function
import cv2 as cv
import argparse
import flappy


def detectAndDisplay(frame):
    flappy.eyes_detected = False

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h, x:x+w]

        #-- In each face, detect eyes
        #detectmultiscale比对摄像头里的脸和数据库的脸
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            #frame会在camera上圈出眼睛的位置
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)

            #如果camera没有标出眼睛的两个圆圈（必须同时存在两个蓝色的圆圈）
            #如何判断出我的眼睛已经被识别出来了？
            flappy.eyes_detected = True

        #-- detect smile
        # smile = smileCascade.detectMultiScale(frame_gray, scaleFactor=1.5, minNeighbors=15, minSize=(25, 25))
        # for (xx, yy, ww, hh) in smile:
        #     cv.rectangle(frame, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)

    cv.imshow('Capture - Face detection', frame)


parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.',
                    default='C:\\Users\\13332\\PycharmProjects\\opencv2\\data\\haarcascades\\haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.',
                    default='C:\\Users\\13332\\PycharmProjects\\opencv2\\data\\haarcascades\\haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera devide number.', type=int, default=0)
args = parser.parse_args()

face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
# smile_cascade_name = args.smile_cascade

# smileCascade = cv.CascadeClassifier('C:\\Users\\13332\\PycharmProjects\\opencv2\\data\\haarcascades\\haarcascade_smile.xml')

face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

# -- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

# -- 2. Read the video stream
cap = cv.VideoCapture(args.camera)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

# # 运行代码如下
# while True:
#     ret, frame = cap.read()
#     if frame is None:
#         print('--(!) No captured frame -- Break!')
#         break
#
#     detectAndDisplay(frame)
#
#     if cv.waitKey(5) == 27:
#         break