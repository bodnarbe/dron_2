#
#    if not drone.is_flying:
#        cmd = input('Type: First import then take off')
#        # ================================= TAKE OFF =========================================
#        if cmd == "take off" and imported == True:
            drone.takeoff()
            print('Drón felszállt')
            sleep(1)
            drone.send_rc_control(0, 0, 0, 0)
            STATE = "mode_choose"
            now = datetime.now()
            real_folder_name = now.strftime("%Y_%m_%d__%H_%M_%S")
            path = 'C:/test/' + real_folder_name + '/'
            print('This flying operation directory:', path)

        else:
            print("Coordinates are missing...")
        # ================================== IMPORT COORDINATE ================================
        if cmd == "import":
            print("Coordinates have been imported... ready to fly")
            with open('koordinates.txt') as json_file:
                koordinatesjson_r = json.load(json_file)
                for p in koordinatesjson_r['koordinate']:
                    koordinates.append(p[1])
            print("Imported coordinates", koordinates)
            imported = True

    # ============================================= Flying operation ===================================================
    # ==================================================================================================================
    if drone.is_flying:

        if STATE == "mode_choose":

            cmd_mode = input("Time to choose mode... Kézi:'manual'   Automata bejárás:'bejaro'   Permetezés: 'permet'")

            if cmd_mode == "bejaro":
                print("Enter: Auto mode")
                STATE = "AUTO"

            if cmd_mode == "manual":
                print("Enter: Manual mode")
                STATE = "MANUAL"

            if cmd_mode == "permet":
                print("Enter: PERMET mode")
                STATE = "PERMET"
        # ====================================== AUTOMATA BEJÁRÓ =======================================================
        # ==============================================================================================================
        elif STATE == "AUTO":
            print("Height check: 'h' || Bejáró start: 'a' || Land: 'x' ")
            cmd_command_auto = keyboard.read_key()
            koordinates_save = [0, len(koordinates)]

            # ================================= Magasság check =========================================================
            if cmd_command_auto == 'h':
                droneheight = drone.get_height()
                print(droneheight)

            # ================================== Automata bejáró képkészítéssel ========================================
            if cmd_command_auto == 'a':

                print("Auto bejárás, bejárandó pontok:", len(koordinates), "Battery check...")
                battery = drone.get_battery()

                if battery > 15:
                    print("Battery ok", battery, "Might be enough")
                    drone.streamon()
                    folder_create.create_folder(real_folder_name, koordinates)
                    elso = True
                    bejaras_bool = True
                    j = 0
                    # ================================== BEJÁRÓ CIKLUS =================================================
                    while bejaras_bool: # ================================== nem tesztelt ==============================
                    # for j, i in enumerate(koordinates):
                        # ============================== STOP ==========================================================
                        if keyboard.is_pressed('s'):
                            os.chdir('C:/test/' + real_folder_name)
                            for json in enumerate(koordinates_save):
                                coordinatesave['koordinate'].append(json)
                            with open('koordinates_save.txt', 'w') as outfile:
                                json.dump(coordinatesave, outfile)
                            print('The loop is stopped')
                            STATE = "mode_choose"
                            break

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
                            bejaras_bool = False # ================================== nem tesztelt =====================
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
                            STATE = "IMAGE"
                else:
                    print("Aksi csere kell")
                    sleep(2)
                    drone.land()
                    break

            # Leszállás parancs
            if cmd_command_auto == 'x':
                sleep(2)
                drone.land()
                STATE = "mode_choose"

        elif STATE == "MANUAL":

            cmd_command_manual = keyboard.read_key()

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

            if cmd_command_manual == 'g':
                drone.send_rc_control(0, 0, drone_speed, 0)

            if cmd_command_manual == 't':
                drone.send_rc_control(0, 0, -drone_speed, 0)

            if cmd_command_manual == 'e':
                drone.send_rc_control(0, 0, 0, drone_speed)

            if cmd_command_manual == 'q':
                drone.send_rc_control(0, 0, 0, -drone_speed)

            if cmd_command_manual == 'x':
                drone.send_rc_control(0, 0, 0, 0)
                print("Kilépés a manualból....")
                STATE = "mode choose"

        elif STATE == "IMAGE":
            if not image_operation:
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
                image_operation = False
                drone.land()

        elif STATE == "PERMET":
            os.chdir('C:/test')
            if os.path.isfile("permet.txt"):
                print("Permetezés")
                with open('permet.txt') as json_file:
                    koordinatesjson_r = json.load(json_file)
                    for p in koordinatesjson_r['koordinate']:
                        permet.append(p[1])
                    print("Imported: ", permet)
                permet_bool = True
                permet_i = 0
                while permet_bool: # ================================== nem tesztelt ===================================
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
                    sleep(1)
                    drone.move_up(50)
                    permet_i += 1 # ================================== nem tesztelt ====================================
                    # LAST
                    if permet[permet_i] == permet[-1]: # move_order[1] == True:
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
            else:
                print("Nincs permet koordináta")
                drone.land()