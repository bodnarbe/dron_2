from djitellopy import tello
from time import sleep
import keyboard

drone = tello.Tello()
drone.connect()

print(drone.get_battery())
STATE = "NONE"

droneheight = 0

while True:

    if not drone.is_flying:
        cmd = input('Enter take off:')

        if cmd == "take off":
            drone.takeoff()
            print('Drón felszállt')
            sleep(1)
            drone.send_rc_control(0, 0, 0, 0)
            STATE = "mode_choose"

    if drone.is_flying:
        if keyboard.is_pressed('esc'):
            print("Interupted")
            STATE = "INTERUPT"

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

        elif STATE == "INTERUPT":
            drone.send_rc_control(0, 0, 0, 0)
            sleep(1)
            drone.land()

        elif STATE == "AUTO":

            cmd_command_auto = keyboard.read_key()

            if cmd_command_auto == 'd':
                droneheight = drone.get_height()
                print(droneheight)

            if cmd_command_auto == 'q':

                if droneheight < 20:
                    drone.send_rc_control(0,0,10,0)
                    while droneheight < 20:
                        sleep(1)
                        droneheight = drone.get_height()
                        print(droneheight)

                if droneheight > 30:
                    drone.send_rc_control(0,0,-10,0)
                    while droneheight > 30:
                        sleep(1)
                        droneheight = drone.get_height()
                        print(droneheight)

                if 60 < droneheight < 70:
                    drone.send_rc_control(0,0,0,0)

            if cmd_command_auto == 'a':
                drone.set_speed(10)
                drone.move_forward(100)
                sleep(2)
                drone.move_left(100)
                sleep(2)
                drone.move_back(100)
                sleep(2)
                drone.move_right(100)

            if cmd_command_auto == 'x':
                sleep(2)
                drone.land()
                STATE == "mode_choose"

        elif STATE == "MANUAL":

            cmd_command_manual = keyboard.read_key()
            if cmd_command_manual == 'c':
                drone.send_rc_control(0, 0, 0, 0)
            if cmd_command_manual == 'w':
                drone.send_rc_control(0, 50, 0, 0)

            if cmd_command_manual == 's':
                drone.send_rc_control(0, -50, 0, 0)

            if cmd_command_manual == 'a':
                drone.send_rc_control(-50, 0, 0, 0)

            if cmd_command_manual == 'd':
                drone.send_rc_control(50, 0, 0, 0)

            if cmd_command_manual == 'g':
                drone.send_rc_control(0, 0, 50, 0)

            if cmd_command_manual == 't':
                drone.send_rc_control(0, 0, -50, 0)

            if cmd_command_manual == 'e':
                drone.send_rc_control(0, 0, 0, 50)

            if cmd_command_manual == 'q':
                drone.send_rc_control(0, 0, 0, -50)

            if cmd_command_manual == 'x':
                drone.send_rc_control(0, 0, 0, 0)
                print("Leszállás folyamatban....")
                drone.land()
                sleep(5)
                print("Leszállt")
                sleep(1)
                STATE = "NONE"
