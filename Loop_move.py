from djitellopy import tello
from time import sleep
from datetime import datetime
import cv2 as cv
import os
import keyboard

# Drone connect
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

# Drone parameters
drone.set_speed(20)

# [x,y][min(0,0)][max(2,2)]]
koordinates = [[0, 0], [50, 0], [100, 0], [150, 0], [200, 0], [200, 50], [150, 50], [100, 50], [50, 50], [0, 50],
               [0, 100], [50, 100], [100, 100],
               [150, 100], [200, 100], [200, 150], [150, 150], [100, 150], [50, 150], [0, 150], [0, 200], [50, 200],
               [100, 200], [150, 200], [200, 200]]


def create_folder(folder_name, valami):
    try:
        os.mkdir('C:/test/' + folder_name)
        for mappa_i in range(len(valami)):
            os.chdir('C:/test/' + folder_name)
            os.mkdir('C:/test/' + folder_name + '/' + str(mappa_i))
        os.chdir('C:/test/' + folder_name)
        print("Directory made and changed.")
    except FileExistsError:
        print("This directory", folder_name, "already exist")


def decode_coordinates(coordinates_input, current):
    last = False
    if coordinates_input[current] == coordinates_input[-1]:
        move_array = [0, 0, 0, 0]
        last = True
        return move_array, last
    else:
        jelen_x = coordinates_input[current][0]
        jelen_y = coordinates_input[current][1]
        next = current + 1
        next_x = coordinates_input[next][0]
        next_y = coordinates_input[next][1]

        move_x = next_x - jelen_x
        move_y = next_y - jelen_y

        move_array = [0, 0, 0, 0]

        if move_x > 0:
            move_array[0] = move_x
        if move_x < 0:
            move_array[1] = abs(move_x)
        if move_y > 0:
            move_array[2] = move_y
        if move_y < 0:
            move_array[3] = abs(move_y)

        return move_array, last

# INIT
STATE = "0"
koordinates_save = [0, len(koordinates)]

while True:
    if not drone.is_flying:
        cmd = input('Drone ready to take off:')

        if cmd == "take off":
            drone.takeoff()
            print('Drón felszállt')
            sleep(1)
            drone.send_rc_control(0, 0, 0, 0)
            STATE = "mode_choose"

    if drone.is_flying:

        if STATE == "mode_choose":
            print("Time to choose mode... Kézi:'0'   Automata:'1'")
            cmd_mode = keyboard.read_key()

            if cmd_mode == "1":
                print("Enter: Auto mode")
                STATE = "AUTO"

            if cmd_mode == "0":
                print("Enter: Manual mode")
                STATE = "MANUAL"

        elif STATE == "AUTO":

            print("Height check: 'h' || Bejáró mode: 'a' || Land: 'x' ")
            cmd_command_auto = keyboard.read_key()

            # Magasság check
            if cmd_command_auto == 'h':
                droneheight = drone.get_height()
                print(droneheight)

            # Automata bejáró képkészítéssel
            if cmd_command_auto == 'a':

                print("Auto bejárás, bejárandó pontok:", len(koordinates), "Battery check...")
                battery = drone.get_battery()

                if battery > 10:
                    print("Battery ok", battery, "Might be enough")

                    drone.streamon()

                    now = datetime.now()
                    real_folder_name = now.strftime("%Y_%m_%d__%H_%M_%S")
                    create_folder(real_folder_name, koordinates)

                    for j, i in enumerate(koordinates):

                        # STOP
                        if keyboard.is_pressed('s'):
                            STATE = "mode_choose"
                            print('The loop is stopped')
                            break

                        # Mentünk már erre
                        if j == 0 and koordinates_save[0] != 0:
                            j = koordinates_save[0]
                            i = koordinates[j]
                            print("Votmá ilyen")

                        os.chdir('C:/test/' + real_folder_name + '/' + str(j))
                        move_order = decode_coordinates(koordinates, j)
                        print("Actual coordinate:", j)

                        # Első
                        if j == 0:
                            not_image = True
                            k = 0
                            while not_image:
                                drone_speed = [drone.get_speed_x(),drone.get_speed_y(),drone.get_speed_z()]
                                if drone_speed[0] < 1 or drone_speed[1] < 1 or drone_speed[2] < 1:
                                    img = drone.get_frame_read().frame
                                    cv.imwrite(str(j) + str(k) + '.png', img)
                                    k = k + 1
                                    if k == 10:
                                        not_image = False

                        elif move_order[1] == False:
                            # Előre
                            if move_order[0][0] != 0:
                                forwardmovedistance = move_order[0][0]
                                print('Move forward', forwardmovedistance, 'cm')
                                drone.move_forward(forwardmovedistance)

                                not_image = True
                                k = 0
                                while not_image:
                                    drone_speed = [drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z()]
                                    if drone_speed[0] < 1 or drone_speed[1] < 1 or drone_speed[2] < 1:
                                        img = drone.get_frame_read().frame
                                        cv.imwrite(str(j) + str(k) + '.png', img)
                                        k = k + 1
                                        if k == 10:
                                            not_image = False
                            # Hátra
                            if move_order[0][1] != 0:
                                backmovedistance = move_order[0][1]
                                print('Move back', backmovedistance, 'cm')
                                drone.move_back(backmovedistance)

                                not_image = True
                                k = 0
                                while not_image:
                                    drone_speed = [drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z()]
                                    if drone_speed[0] < 1 or drone_speed[1] < 1 or drone_speed[2] < 1:
                                        img = drone.get_frame_read().frame
                                        cv.imwrite(str(j) + str(k) + '.png', img)
                                        k = k + 1
                                        if k == 10:
                                            not_image = False
                            # Jobbra
                            if move_order[0][2] != 0:
                                rightmovedistance = move_order[0][2]
                                print('Move right', rightmovedistance, 'cm')
                                drone.move_right(rightmovedistance)

                                not_image = True
                                k = 0
                                while not_image:
                                    drone_speed = [drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z()]
                                    if drone_speed[0] < 1 or drone_speed[1] < 1 or drone_speed[2] < 1:
                                        img = drone.get_frame_read().frame
                                        cv.imwrite(str(j) + str(k) + '.png', img)
                                        k = k + 1
                                        if k == 10:
                                            not_image = False
                            # Balra
                            if move_order[0][3] != 0:
                                leftmovedistance = move_order[0][3]
                                print('Move left', leftmovedistance, 'cm')
                                drone.move_left(leftmovedistance)

                                not_image = True
                                k = 0
                                while not_image:
                                    drone_speed = [drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z()]
                                    if drone_speed[0] < 1 or drone_speed[1] < 1 or drone_speed[2] < 1:
                                        img = drone.get_frame_read().frame
                                        cv.imwrite(str(j) + str(k) + '.png', img)
                                        k = k + 1
                                        if k == 10:
                                            not_image = False

                        elif move_order[1] == True:
                            print('Az egész kész')
                            koordinates_save[0] = 0

                        koordinates_save[0] = j
                        print("Saved and Done:", j)

                else:
                    print("Aksi csere kell")
                    sleep(2)
                    drone.land()

            # Leszállás parancs
            if cmd_command_auto == 'x':
                sleep(2)
                drone.land()
                STATE = "mode_choose"