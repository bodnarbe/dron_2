import os

from djitellopy import tello
import cv2 as cv
from datetime import datetime
import keyboard
from time import sleep
import opencv_iav.camera as camera

drone = tello.Tello()
drone.connect()

print(drone.get_battery())

drone.streamon()

for i in range(10):
    print(drone.get_height())

sleep(5)
drone.takeoff()

i=0

def create_folder(folder_name):
    try:
        os.mkdir('C:/test/'+folder_name)
        os.chdir('C:/test/'+folder_name)
        print("Dir made and changed.")
    except FileExistsError:
        print("This directory", folder_name, "already exist")

now = datetime.now()
real_folder_name = now.strftime("%Y_%m_%d__%H_%M_%S")
create_folder(real_folder_name)
drone.move_up(30)
while True:
    img = drone.get_frame_read().frame
    #img = cv.resize(img, (2592, 1936))

    cv.imshow("Image", img)
    cv.waitKey(1)
    picname=str(i) + str(drone.get_height())+".png"
    cv.imwrite(picname, img)
    i+=1
    if i==200:
        drone.land()
        sleep(3)

