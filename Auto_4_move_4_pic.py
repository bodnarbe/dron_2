from djitellopy import tello
from time import sleep
import cv2 as cv
import os

import keyboard

drone = tello.Tello()
drone.connect()

print(drone.get_battery())

while True:
    if not drone.is_flying:
        cmd = input('Enter take off:')

        if cmd == "take off":
            drone.takeoff()
            print('Drón felszállt')
            drone.streamon()
            print('Stream on')
            sleep(1)
            drone.send_rc_control(0, 0, 0, 0)
            STATE = "mode_choose"

    if drone.is_flying:
        if STATE == "mode_choose":
            print("Time to choose mode")
            cmd_mode = keyboard.read_key()
            wait = True
            print("Kézi:0   Automata:1")
            if cmd_mode == "1":
                print("Auto mode")
                STATE = "AUTO"
            if cmd_mode == "0":
                print("Manual mode")
                STATE = "MANUAL"

        elif STATE == "AUTO":

            cmd_command_auto = keyboard.read_key()

            if cmd_command_auto == 'd':
                droneheight = drone.get_height()
                print(droneheight)

            if cmd_command_auto == 'w':
                #drone.send_rc_control(0, 0, -20, 0)
                #sleep(4)
                #drone.send_rc_control(0, 0, 0, 0)
                #sleep(2)
                #drone.send_rc_control(0, 20, 0, 0)
                #sleep(5)
                #drone.send_rc_control(0, 0, 0, 0)
                drone.move_forward(100)
                sleep(1)
                drone.land()
                STATE="mode_choose"

            if cmd_command_auto == 'a':
                drone.send_rc_control(0, 0, -20, 0)
                sleep(2)

                drone.send_rc_control(0, 20, 0, 0)
                sleep(5)
                drone.send_rc_control(0, 0, 0, 0)
                sleep(1)
                img = drone.get_frame_read().frame
                os.chdir('C:/test')
                cv.imwrite('1.png', img)

                drone.send_rc_control(20, 0, 0, 0)
                sleep(5)
                drone.send_rc_control(0, 0, 0, 0)
                sleep(1)
                img = drone.get_frame_read().frame
                os.chdir('C:/test')
                cv.imwrite('2.png', img)

                drone.send_rc_control(0, -20, 0, 0)
                sleep(5)
                drone.send_rc_control(0, 0, 0, 0)
                sleep(1)
                img = drone.get_frame_read().frame
                os.chdir('C:/test')
                cv.imwrite('3.png', img)

                drone.send_rc_control(-20, 0, 0, 0)
                sleep(5)
                drone.send_rc_control(0, 0, 0, 0)
                sleep(1)
                img = drone.get_frame_read().frame
                os.chdir('C:/test')
                cv.imwrite('4.png', img)

                print('Kész')

            if cmd_command_auto == 'x':
                sleep(2)
                drone.land()
                STATE == "mode_choose"

