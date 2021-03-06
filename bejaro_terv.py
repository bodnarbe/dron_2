import math
import logging
import time

from PIL import Image, ImageDraw
import copy
import pygame


def debug(str,var):
    print(str)
    print(var)


def distance(start_point, end_point):
    return math.dist(start_point, end_point)


def nearest_point(start_point, array):
    debug("start point:", start_point)
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
    # debug("queue: ", going_over_coords_queue)
    while len(going_over_coords_queue) != 0:
        if actual_coord in going_over_coords_queue:
            going_over_coords[going_over_coords.index(actual_coord)][2] = 1
            bejaras.append(actual_coord)
            going_over_coords_queue.remove(actual_coord)
            if(len(going_over_coords_queue) != 0):
                actual_coord = going_over_coords_queue[nearest_point(actual_coord, going_over_coords_queue)]
            # print(actual_coord)
    # print("bejaras: ", bejaras)
    return bejaras

max_x_bejaras = 200
max_y_bejaras = 200
start_x = 0
start_y = 0

def draw_area(dis):
    y = 0
    x = 0
    while y < max_y_bejaras + 100:
        x = 0
        while x < max_x_bejaras + 100:
            if x == 0 or x == max_x_bejaras + 50 or y == 0 or y == max_y_bejaras + 50: # y == 150 and x > 150 or y == 200 and x > 150 or x == 0 or x == 350 or y == 0 or y == 350:
                area_coords.append([x, y, 1])
                # ImageDraw.Draw(img).rectangle([(x, y), (x + 50, y + 50)], fill="#FF0000", outline="green")
                pygame.draw.rect(dis, "red", [x, y, 50, 50])
                pygame.draw.rect(dis, "green", [x, y, 50, 50], 1)
                pygame.display.update()
            else:
                # ImageDraw.Draw(img).rectangle([(x, y), (x + 50, y + 50)], fill="#FFFFFF", outline="green")
                area_coords.append([x, y, 0])
                pygame.draw.rect(dis, "white", [x, y, 50, 50])
                pygame.draw.rect(dis, "green", [x, y, 50, 50], 1)
                pygame.display.update()
            if y > 0 and x > 0:
                pygame.draw.circle(dis, "blue", [x, y], 5)
                pygame.display.update()
                going_over_coords.append([x, y, 0])
                # if y == 200 and x > 200 or y == 200 and x > 200:
                    # ()
                # else:
                    # ImageDraw.Draw(img).ellipse((x - 5, y - 5, x + 5, y + 5), fill="green", outline="white")
                    # pygame.draw.circle(dis, "blue", [x, y], 5)
                    # pygame.display.update()
                    # going_over_coords.append([x, y, 0])

            x += 50
        y += 50

w, h = max_x_bejaras + 100, max_y_bejaras + 100
x, y = 0, 0
shape = [(x, y), (50, 50)]

# creating new Image object
img = Image.new("RGB", (w, h))

# create  rectangleimage

# ##valtozok a bejarashoz
# ##(x,y,color)
area_coords = []
start_coord = [start_x + 50, start_y + 50, 0]
# ##(x,y,color)
going_over_coords = []
bejaras = []
koordinates_output = []

# y = 0
# x = 0
# while y < 400:
#     x = 0
#     while x < 400:
#         if y == 150 and x > 150 or y == 200 and x > 150 or x == 0 or x == 350 or y == 0 or y == 350:
#             area_coords.append([x, y, 1])
#             ImageDraw.Draw(img).rectangle([(x, y), (x + 50, y + 50)], fill="#FF0000", outline="green")
#         else:
#             ImageDraw.Draw(img).rectangle([(x, y), (x + 50, y + 50)], fill="#FFFFFF", outline="green")
#             area_coords.append([x, y, 0])
#         if y > 0 and x > 0:
#             if y == 200 and x > 200 or y == 200 and x > 200:
#                 ()
#             else:
#                 ImageDraw.Draw(img).ellipse((x - 5, y - 5, x + 5, y + 5), fill="green", outline="white")
#                 going_over_coords.append([x, y, 0])
#
#         x += 50
#     y += 50
#
# print(area_coords)
# print(going_over_coords)
# img.show()
#
# floodfill(going_over_coords, start_coord)
#
#
#
#

import pygame
pygame.init()
dis = pygame.display.set_mode((max_x_bejaras + 100, max_y_bejaras + 100))

draw_area(dis)
bejaras = floodfill(going_over_coords, start_coord)

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    while len(bejaras) != 0:
        print(bejaras[0][0], bejaras[0][1])
        koordinates_output.append([bejaras[0][0] - 50, bejaras[0][1] - 50])
        pygame.draw.circle(dis, "yellow", [bejaras[0][0], bejaras[0][1]], 5)
        pygame.display.update()
        bejaras.pop(0)
        pygame.time.wait(1000)
print(koordinates_output)