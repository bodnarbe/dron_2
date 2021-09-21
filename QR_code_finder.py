from QR_code_utilitis import *
import cv2

import numpy as np
from pyzbar.pyzbar import decode

myDrone = initializeTello()

w, h = 960, 720
pid = [0.05, 0.05, 0]
wError = 0
hError = 0
mozgato = 0
startCounter = 0
while True:

    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    ## Step 1
    img = telloGetFrame(myDrone, w, h)
    img = cv2.flip(img, 0)

    info = findQR(img)
    print(info[1])
    # myQRLIST.append([cx, cy])
    if mozgato == 4:
        mozgato = 0
    Error = trackQR(myDrone, info[1], w, h, pid, wError, hError, mozgato)
    mozgato += 1
    wError = Error[0]
    hError = Error[1]
    print(wError, hError)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        myDrone.land()
        break