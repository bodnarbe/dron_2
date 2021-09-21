from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode
import numpy as np
from time import sleep

def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def telloGetFrame(myDrone, w=360,h=240):
    myFrame = myDrone.get_frame_read().frame
    img = cv2.resize(myFrame,(w,h))
    return img

def findQR(img):
    code = decode(img)
    if code != []:
        myQRLIST = []

        for barcode in code:
            myData = barcode.data.decode('utf-8')
            handw = np.array([barcode.rect], np.int32)
            pts = np.array([barcode.polygon], np.int32)
            handw = handw.reshape((-1, 1, 2))
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (0, 0, 255), 5)
            x = pts[0][0][0]
            y = pts[0][0][1]
            w_img = handw[1][0][0]
            h_img = handw[1][0][1]
            cx = x + w_img // 2
            cy = y + h_img // 2
            myQRLIST.append([cx, cy])
        return img, [cx, cy]
        print([cx, cy])
    else:
        return img, [0, 0]
        print([0, 0])

def trackQR (myDrone, info, w, h, pid, wError, hError, mozgato):
    if info == [0, 0]:
        if mozgato == 0:
            myDrone.move_forward(20)
        if mozgato == 1:
            myDrone.move_right(20)
        if mozgato == 2:
            myDrone.move_back(20)
        if mozgato == 3:
            myDrone.move_left(20)
        return 0, 0
    else:
        error_w = info[0] - w//2
        error_h = info[1] - h//2
        speed_w = pid[0] * error_w + pid[1] * (error_w - wError)
        speed_h = pid[0] * error_h + pid[1] * (error_h - hError)
        speed_w = int(np.clip(speed_w, -50, 50))
        speed_h = int(np.clip(speed_h, -50, 50))

        if error_h > 100 or error_h < -100 or error_w > 100 or error_w < -100:
            myDrone.left_right_velocity = speed_w
            myDrone.for_back_velocity = speed_h
        else:
            myDrone.for_back_velocity = 0
            myDrone.left_right_velocity = 0
            myDrone.up_down_velocity = 0
            myDrone.yaw_velocity = 0
            error = 0
        if myDrone.send_rc_control:
            myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity, myDrone.up_down_velocity, myDrone.yaw_velocity)
        return error_w, error_h