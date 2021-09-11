def decode_coordinates(coordinates_input, current):
    last = False
    if coordinates_input[current] == coordinates_input[-1]:
        print('utsó')
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
        print("move_array: ", move_array, "current: ", coordinates_input[current])
        return move_array, last