import cv2 as cv
import os
import numpy as np
import keyboard
from djitellopy import tello
from time import sleep
from datetime import datetime
import folder_create
import decode_coordinates
import json
import socket
import math
import copy
from PIL import Image

PERMET_HOST = '192.168.4.1'  # Permetező IP
PERMET_PORT = 80  # Permetező port

# Drone parameters
drone = tello.Tello()
drone.connect()
print('Drone connected', 'Battery:', drone.get_battery())

# Drone parameters
drone_speed = 50
expectedheight = 100
drone.set_speed(drone_speed)

# Area [x,y][min(0,0)][max(200,200)]]
koordinatesjson = {}
koordinatesjson['koordinate'] = []
koordinates = []
bejaras = []
bejarando_terulet = []
bejaro_coordinate = []
coordinatesave = {}
coordinatesave['koordinate'] = []
moveback = []
permet = []

# Default sets
STATE = '0'

# Drone operation
imported = False
pictures = False
oszto = 50
image_operation = False
now = datetime.now()
real_folder_name = now.strftime("%Y_%m_%d__%H_%M_%S")
path = 'C:/test/' + real_folder_name + '/'

def send_tcp_data(HOST, PORT, input_message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(input_message, 'utf-8') + b'#')
        megvan = True
        while megvan:
            data = s.recv(1024)
            if data == b'ok':
                megvan = False

def get_data_tcp_data(HOST, PORT, mit):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(mit, 'utf-8') + b'#')
        data = s.recv(1024)
        return data

def distance(start_point, end_point):
    return math.dist(start_point, end_point)

def nearest_point(start_point, array):
    start_point = [start_point[0], start_point[1]]
    distances_array = []
    for i in array:
        distances_array.append(distance(start_point, [i[0], i[1]]))
    # print(min(distances_array))
    return distances_array.index(min(distances_array))

def floodfill(going_over_coords, start_coord):
    # (x,y)
    actual_coord = start_coord
    # (x,y,0)
    going_over_coords_queue = copy.deepcopy(going_over_coords)
    while len(going_over_coords_queue) != 0:
        print('Katt')
        if actual_coord in going_over_coords_queue:
            going_over_coords[going_over_coords.index(actual_coord)][2] = 1
            bejaras.append(actual_coord)
            going_over_coords_queue.remove(actual_coord)
            if(len(going_over_coords_queue) != 0):
                actual_coord = going_over_coords_queue[nearest_point(actual_coord, going_over_coords_queue)]
    return bejaras

while True:
    # ==================================================================================================================
    # ==================================================================================================================
    # =========================$$$$$$$$$$$$$$$$$$$ IDLE MODE $$$$$$$$$$$$$$$$$$$========================================
    # ==================================================================================================================
    # ==================================================================================================================
    if STATE == '0':
        print("Welcome! Collaborative system has started. IDLE MODE!")
        cmd_idle = input("Choose mode: plan, flying, image")

        if cmd_idle == "plan":
            print("Enter plane mode")
            STATE = "PLAN"
        if cmd_idle == "flying":
            print("Enter flying mode")
            STATE = "FLYING"
        if cmd_idle == "image":
            print("Enter image mode")
            STATE = "IMAGE"
    # ==================================================================================================================
    # ==================================================================================================================
    # =========================$$$$$$$$$$$$$$$$$$$ PLAN MODE $$$$$$$$$$$$$$$$$$$========================================
    # ==================================================================================================================
    # ==================================================================================================================
    if STATE == "PLAN":
        print("Enter PLAN mode, just rectangle!")
        max_x_bejaras = int(input("max_x_bejaras"))
        max_y_bejaras = int(input("max_y_bejaras"))
        start_x = int(input("start_x"))
        start_y = int(input("start_y"))
        start_coord = [start_x, start_y, 0]
        plan_x = 0
        while plan_x != max_x_bejaras + oszto:
            plan_y = 0
            while plan_y != max_y_bejaras + oszto:
                bejarando_terulet.append([plan_x, plan_y, 0])
                plan_y += oszto
            plan_x += oszto
        print(bejarando_terulet)

        bejaras_eredmeny = floodfill(bejarando_terulet, start_coord)
        print('kész')
        while len(bejaras_eredmeny) != 0:
            print(bejaras_eredmeny[0][0], bejaras_eredmeny[0][1])
            bejaro_coordinate.append([bejaras_eredmeny[0][0], bejaras_eredmeny[0][1]])
            bejaras_eredmeny.pop(0)
        print(bejaro_coordinate)

        for i in enumerate(bejaro_coordinate):
            koordinatesjson['koordinate'].append(i)

        with open('koordinates.txt', 'w') as outfile:
            json.dump(koordinatesjson, outfile)

        STATE = "0"
        print('Planing done and saved')
    # ==================================================================================================================
    # ==================================================================================================================
    # =========================$$$$$$$$$$$$$$$$$$$ FLYING MODE $$$$$$$$$$$$$$$$$$$======================================
    # ==================================================================================================================
    # ==================================================================================================================
    if STATE == "FLYING":
        print('Drone connected', 'Battery:', drone.get_battery())
        cmd_flying = input("Choose mode: Automatic inspection: 'auto' Manual flying mode: 'manual' Spraying: 'spray' LAND: 'land' QUIT: 'quit'")

        if cmd_flying == "auto":
            print("Enter Automatic inspection mode")
            STATE = "AUTO"
        if cmd_flying == "manual":
            print("Enter manual mode")
            STATE = "MANUAL"
        if cmd_flying == "spray":
            print("Enter spraying mode")
            STATE = "SPRAY"
        if cmd_flying == "land":
            drone.land()
        if cmd_flying == "quit":
            STATE = "0"
    # ============================================== AUTO MODE =========================================================
    # ==================================================================================================================
    if STATE == "AUTO":

        if not drone.is_flying:
            cmd_auto = input("Check coordinate's file than import!")
            if cmd_auto == "import":
                print("Coordinates have been imported... ready to fly")
                with open('koordinates.txt') as json_file:
                    koordinatesjson_r = json.load(json_file)
                    for p in koordinatesjson_r['koordinate']:
                        koordinates.append(p[1])
                print("Imported coordinates", koordinates)
                imported = True

            if imported:
                cmd_auto = input("Ready to take off")
                if cmd_auto == "take off":
                    now = datetime.now()
                    real_folder_name = now.strftime("%Y_%m_%d__%H_%M_%S")
                    path = 'C:/test/' + real_folder_name + '/'
                    print('This flying operation directory:', path)
                    folder_create.create_folder(real_folder_name, koordinates)
                    drone.takeoff()
                    drone.send_rc_control(0, 0, 0, 0)

        if drone.is_flying:
            print("Set height: 'h' || Inspection start: 'a' || Land and quit: 'x' ")
            cmd_command_auto = keyboard.read_key()
            koordinates_save = [0, len(koordinates)]
            # ================================================================================= SET HEIGHT =============
            if cmd_command_auto == 'h':
                #droneheight = get_data_tcp_data(PERMET_HOST, PERMET_PORT, 'height')
                #print(droneheight)
                #if droneheight < expectedheight:
                #    drone.move_up(expectedheight-droneheight)
                #if droneheight > expectedheight:
                #    drone.move_down(droneheight-expectedheight)
                print("Height calibration done")
            # ================================================================================= INSPECTION =============
            if cmd_command_auto == 'a':

                print("Auto bejárás, bejárandó pontok:", len(koordinates), "Battery check...")
                battery = drone.get_battery()

                if battery > 15:
                    print("Battery ok", battery, "Might be enough")
                    drone.streamon()
                    elso = True
                    bejaras_bool = True
                    j = 0
                    # ================================== BEJÁRÓ CIKLUS =================================================
                    while bejaras_bool:
                        # ============================== STOP ==========================================================
                        if keyboard.is_pressed('s'):
                            os.chdir('C:/test/' + real_folder_name)
                            for json in enumerate(koordinates_save):
                                coordinatesave['koordinate'].append(json)
                            with open('koordinates_save.txt', 'w') as outfile:
                                json.dump(coordinatesave, outfile)
                            print('The loop is stopped')
                            STATE = "MANUAL"
                            bejaras_bool = False

                        # ============================== Mentünk már erre ==============================================
                        if j == 0 and os.path.isfile('C:/test/' + real_folder_name +'/' + 'koordinates_save.txt'):
                            with open('koordinates_save.txt') as json_file:
                                koordinatesjson_r = json.load(json_file)
                                j_save = 0 # ================================== nem tesztelt ===========================
                                for p in koordinatesjson_r['koordinate']:
                                    koordinates_save.append(p[1])
                                    j_save += 1 # ================================== nem tesztelt ======================
                            j = j_save # ================================== nem tesztelt ===============================
                            # i = koordinates[j]
                            print("Votmá ilyen")

                        print("Actual coordinate:", j)

                        # Első
                        if elso:
                            os.chdir('C:/test/' + real_folder_name + '/' + str(j))
                            not_image = True
                            k = 0
                            while not_image:
                                drone_speed = [drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z()]
                                if drone_speed[0] == 0 or drone_speed[1] == 0 or drone_speed[2] == 0:
                                    img = drone.get_frame_read().frame
                                    img = cv.flip(img, 0)
                                    cv.imwrite(str(j) + str(k) + '.png', img)
                                    k += 1
                                    if k == 10:
                                        not_image = False
                            print("Első done")
                            elso = False
                        else:
                            os.chdir('C:/test/' + real_folder_name + '/' + str(j + 1))
                            move_order = decode_coordinates.decode_coordinates(koordinates, j)
                            if move_order[1] == False:
                                # Előre
                                if move_order[0][0] != 0:
                                    forwardmovedistance = move_order[0][0]
                                    print('Move forward', forwardmovedistance, 'cm')
                                    drone.move_forward(forwardmovedistance)

                                # Hátra
                                if move_order[0][1] != 0:
                                    backmovedistance = move_order[0][1]
                                    print('Move back', backmovedistance, 'cm')
                                    drone.move_back(backmovedistance)

                                # Jobbra
                                if move_order[0][2] != 0:
                                    rightmovedistance = move_order[0][2]
                                    print('Move right', rightmovedistance, 'cm')
                                    drone.move_right(rightmovedistance)

                                # Balra
                                if move_order[0][3] != 0:
                                    leftmovedistance = move_order[0][3]
                                    print('Move left', leftmovedistance, 'cm')
                                    drone.move_left(leftmovedistance)

                                not_image = True
                                k = 0
                                while not_image:
                                    drone_speed = [drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z()]
                                    print(drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z())
                                    if drone_speed[0] < 1 or drone_speed[1] < 1 or drone_speed[2] < 1:
                                        img = drone.get_frame_read().frame
                                        img = cv.flip(img, 0)
                                        cv.imwrite(str(j + 1) + str(k) + '.png', img)
                                        k = k + 1
                                        if k == 10:
                                            not_image = False
                                print("Kép kész")
                                j += 1

                        if j == len(koordinates) - 1:
                            print('Az egész kész')
                            bejaras_bool = False
                            koordinates_save[0] = 0
                            image_operation = True
                            print("Go back to zero, zero")
                            moveback = koordinates[-1]
                            if moveback[0] > 0:
                                drone.move_back(moveback[0])
                            if moveback[0] < 0:
                                drone.move_forward(moveback[0])
                            if moveback[1] > 0:
                                drone.move_left(moveback[1])
                            if moveback[1] < 0:
                                drone.move_right(moveback[1])
                            sleep(1)
                            print('Time to image operate...')
                            pictures = True
                            bejaras_bool = False
                else:
                    print("Aksi csere kell")
            # ================================================================================= LAND AND QUIT ==========
            if cmd_command_auto == 'x':
                sleep(2)
                drone.land()
                STATE = "FLYING"
    # ============================================ MANUAL MODE =========================================================
    # ==================================================================================================================
    if STATE == "MANUAL":
        cmd_command_manual = keyboard.read_key()
        if cmd_command_manual == 't':
            drone.takeoff()

        if cmd_command_manual == 'c':
            drone.send_rc_control(0, 0, 0, 0)

        if cmd_command_manual == 'w':
            drone.send_rc_control(0, drone_speed, 0, 0)

        if cmd_command_manual == 's':
            drone.send_rc_control(0, -drone_speed, 0, 0)

        if cmd_command_manual == 'a':
            drone.send_rc_control(-drone_speed, 0, 0, 0)

        if cmd_command_manual == 'd':
            drone.send_rc_control(drone_speed, 0, 0, 0)

        if cmd_command_manual == 'r':
            drone.send_rc_control(0, 0, drone_speed, 0)

        if cmd_command_manual == 'f':
            drone.send_rc_control(0, 0, -drone_speed, 0)

        if cmd_command_manual == 'e':
            drone.send_rc_control(0, 0, 0, drone_speed)

        if cmd_command_manual == 'q':
            drone.send_rc_control(0, 0, 0, -drone_speed)

        if cmd_command_manual == 'x':
            drone.send_rc_control(0, 0, 0, 0)
            drone.land()
            print("Kilépés a manualból....")
            STATE = "FLYING"
    # ============================================= SPRAY MODE =========================================================
    # ==================================================================================================================
    if STATE == "SPRAY":
        drone.takeoff()
        os.chdir('C:/test')
        send_tcp_data(PERMET_HOST, PERMET_PORT, 'SPRAY ON')
        if os.path.isfile("permet.txt"):
            print("Permetezés")
            with open('permet.txt') as json_file:
                koordinatesjson_r = json.load(json_file)
                for p in koordinatesjson_r['koordinate']:
                    permet.append(p[1])
                print("Imported: ", permet)
            permet_bool = True
            permet_i = 0

            while permet_bool:  # ================================== nem tesztelt ===================================
                # for permet_i, k in enumerate(permet):
                move_order = decode_coordinates.decode_coordinates(permet, permet_i)
                # Előre
                if move_order[0][0] != 0:
                    forwardmovedistance = move_order[0][0]
                    print('Move forward', forwardmovedistance, 'cm')
                    drone.move_forward(forwardmovedistance)

                # Hátra
                if move_order[0][1] != 0:
                    backmovedistance = move_order[0][1]
                    print('Move back', backmovedistance, 'cm')
                    drone.move_back(backmovedistance)

                # Jobbra
                if move_order[0][2] != 0:
                    rightmovedistance = move_order[0][2]
                    print('Move right', rightmovedistance, 'cm')
                    drone.move_right(rightmovedistance)

                # Balra
                if move_order[0][3] != 0:
                    leftmovedistance = move_order[0][3]
                    print('Move left', leftmovedistance, 'cm')
                    drone.move_left(leftmovedistance)

                drone.move_down(50)
                send_tcp_data(PERMET_HOST, PERMET_PORT, 'LEDS ON')
                sleep(1)
                drone.move_up(50)
                permet_i += 1  # ================================== nem tesztelt ====================================
                # LAST
                if permet[permet_i] == permet[-1]:  # move_order[1] == True:
                    print("Go back to zero, zero")
                    moveback = permet[-1]
                    if moveback[0] > 0:
                        drone.move_back(moveback[0])
                    if moveback[0] < 0:
                        drone.move_forward(moveback[0])
                    if moveback[1] > 0:
                        drone.move_left(moveback[1])
                    if moveback[1] < 0:
                        drone.move_right(moveback[1])
                    sleep(1)
                    drone.land()
                    send_tcp_data(PERMET_HOST, PERMET_PORT, 'SPRAY OFF')
                    STATE = "FLYING"
        else:
            print("Nincs permet koordináta")
            STATE = "FLYING"
    # ==================================================================================================================
    # ==================================================================================================================
    # ==========================$$$$$$$$$$$$$$$$$$$ IMAGE MODE $$$$$$$$$$$$$$$$$$$======================================
    # ==================================================================================================================
    # ==================================================================================================================
    if STATE == "IMAGE":
        cmd_image = input("Select void: 'merge' ; 'analysis' ; 'quit'")
        # =========================================================================================== MERGER ===========
        # ==============================================================================================================
        if cmd_image == "merge":
            if not pictures:
                print('There is no functional information')
                STATE = "mode_choose"

            else:
                find_max_x_array = []
                find_max_y_array = []
                image_van_e = []
                halo = []

                for i in range(len(koordinates)):
                    find_max_x_array.append(koordinates[i][0])
                    find_max_y_array.append(koordinates[i][1])

                find_min_x = min(find_max_x_array)
                find_min_y = min(find_max_y_array)
                find_max_x = max(find_max_x_array)
                find_max_y = max(find_max_y_array)

                print('Min és Max:', find_min_x, find_max_x, find_min_y, find_max_y)

                i_max_x = find_min_x

                while i_max_x < find_max_x + oszto:
                    i_max_y = find_min_y
                    while i_max_y < find_max_y + oszto:
                        i_inserter_y = i_max_y
                        halo.append([i_max_x, i_max_y])
                        i_max_y += oszto
                    i_max_x += oszto

                for i_van_e in range(len(halo)):
                    image_van_e.append(["nincs", halo[i_van_e]])

                for i_van in range(len(image_van_e)):
                    for i_koordinate in range(len(koordinates)):
                        if image_van_e[i_van][1] == koordinates[i_koordinate]:
                            image_van_e[i_van][0] = str(i_koordinate)

                print('Created virtual net:', image_van_e)

                i_row = 0

                for i_merger in enumerate(image_van_e):
                    os.chdir(path)
                    print(i_merger)
                    if os.path.isfile(str(i_row) + '.png'):

                        image_base = cv.imread(path + str(i_row) + '.png')

                        if i_merger[1][0] == 'nincs':
                            image_plus = np.zeros((720, 960, 3), np.uint8)
                        else:
                            image_plus = cv.imread(path + str(i_merger[1][0]) + '/' + str(i_merger[1][0]) + '9.png')

                        im_tile = np.concatenate((image_base, image_plus), axis=1)
                        cv.imwrite(path + str(i_row) + '.png', im_tile)

                        if i_merger[1][1][1] == find_max_x:
                            i_row += 1
                    else:
                        image_0 = cv.imread(path + str(i_row) + '/' + str(i_row) + '9.png')
                        cv.imwrite(path + str(i_row) + '.png', image_0)

                not_done = True
                i_column = 0

                while not_done:
                    os.chdir(path)
                    if os.path.isfile(str(i_column + 1) + '.png'):
                        if os.path.isfile('done' + '.png'):
                            image_base = cv.imread(path + 'done' + '.png')
                        else:
                            image_base = cv.imread(path + str(i_column) + '.png')
                        image_plus = cv.imread(path + str(i_column + 1) + '.png')
                        im_tile = np.concatenate((image_plus, image_base), axis=0)
                        cv.imwrite(path + 'done' + '.png', im_tile)
                    else:
                        not_done = False
                    i_column += 1

                print('Done')
                pictures = False
        # =========================================================================================== ANALYSIS =========
        # ==============================================================================================================
        if cmd_image == "analysis":
            print()
        # =========================================================================================== QUIT =============
        # ==============================================================================================================
        if cmd_image == "quit":
            STATE == "0"