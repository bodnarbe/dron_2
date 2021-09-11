import cv2
import os
import numpy as np

koordinates = [[0, 0], [50, 0], [100, 0], [150, 0], [200, 0], [200, 50], [150, 50], [100, 50], [50, 50], [0, 50],
               [0, 100], [50, 100], [100, 100], [150, 100], [200, 100], [200, 150], [150, 150], [100, 150], [50, 150],
               [0, 150], [0, 200], [50, 200], [100, 200], [150, 200], [200, 200]]

find_max_x_array = []
find_max_y_array = []
image_van_e = []
halo = []
oszto = 50
path = 'C:/test/2021_08_10__11_27_13/'

for i in range(len(koordinates)):
    find_max_x_array.append(koordinates[i][0])
    find_max_y_array.append(koordinates[i][1])

find_min_x = min(find_max_x_array)
find_min_y = min(find_max_y_array)
find_max_x = max(find_max_x_array)
find_max_y = max(find_max_y_array)

print(find_min_x, find_max_x, find_min_y, find_max_y)

i_max_x = find_min_x

while i_max_x < find_max_x + oszto:
    i_max_y = find_min_y
    while i_max_y < find_max_y + oszto:
        i_inserter_y = i_max_y
        halo.append([i_max_x, i_max_y])
        i_max_y += oszto
    i_max_x += oszto

print(halo)

for i_van_e in range(len(halo)):
    image_van_e.append(["nincs", halo[i_van_e]])

for i_van in range(len(image_van_e)):
    for i_koordinate in range(len(koordinates)):
        if image_van_e[i_van][1] == koordinates[i_koordinate]:
            image_van_e[i_van][0] = str(i_koordinate)

print(image_van_e)

i_row = 0

for i_merger in enumerate(image_van_e):
    os.chdir(path)
    print(i_merger)
    if os.path.isfile(str(i_row) + '.png'):

        image_base = cv2.imread('C:/test/2021_08_10__11_27_13/' + str(i_row) + '.png')

        if i_merger[1][0] == 'nincs':
            image_plus = np.zeros((720, 960, 3), np.uint8)
        else:
            image_plus = cv2.imread('C:/test/2021_08_10__11_27_13/' + str(i_merger[0]) + '/' + str(i_merger[0]) + '9.png')

        im_tile = np.concatenate((image_base, image_plus), axis=1)
        cv2.imwrite('C:/test/2021_08_10__11_27_13/' + str(i_row) + '.png', im_tile)

        if i_merger[1][1][1] == find_max_x:
            i_row += 1
    else:
        image_0 = cv2.imread('C:/test/2021_08_10__11_27_13/' + str(i_row) + '/' + str(i_row) + '9.png')
        cv2.imwrite('C:/test/2021_08_10__11_27_13/' + str(i_row) + '.png', image_0)

not_done = True
i_coloumb = 0

while not_done:
    os.chdir(path)
    if os.path.isfile(str(i_coloumb + 1) + '.png'):
        if os.path.isfile('done' + '.png'):
            image_base = cv2.imread('C:/test/2021_08_10__11_27_13/' + 'done' + '.png')
        else:
            image_base = cv2.imread('C:/test/2021_08_10__11_27_13/' + str(i_coloumb) + '.png')
        image_plus = cv2.imread('C:/test/2021_08_10__11_27_13/' + str(i_coloumb + 1) + '.png')
        im_tile = np.concatenate((image_base, image_plus), axis=0)
        cv2.imwrite('C:/test/2021_08_10__11_27_13/' + 'done' + '.png', im_tile)
    else:
        not_done = False
    i_coloumb += 1