import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import tkinter.font as tk_font
import time
from random import randint, seed

LENGTH = 50
WIDTH = 50
OBJ_COUNT = 20
CELL_SIZE = 10

def random_color():
    de = ("%02x" % randint(0, 255))
    re = ("%02x" % randint(0, 255))
    we = ("%02x" % randint(0, 255))
    ge = "#"
    color = ge + de + re + we

    return color


def do_graphic(bool_map):
    global LENGTH  # x
    global WIDTH  # y
    global CELL_SIZE

    root = tk.Tk()
    root.wm_geometry("+0+0")
    root.configure(bg='#96AFB9', relief='groove')
    canvas = tk.Canvas()

    canvas = tk.Canvas(root, width=CELL_SIZE * LENGTH, height=CELL_SIZE * WIDTH, bg='#96AFB9')
    # canvas.grid(row=4)

    cell_colors = ['black', 'red', 'white', 'blue', 'yellow', 'orange', 'green', 'purple', 'gray', 'brown']
    ci = 0  # color index
    color = ''

    for i in range(LENGTH):  # bool_map[0]
        for j in range(WIDTH):  # bool_map
            x1, y1 = i * CELL_SIZE, j * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

            if bool_map[j][i] == 1:
                color = cell_colors[1]
            elif bool_map[j][i] == 2:
                color = cell_colors[2]
            elif bool_map[j][i] == 3:
                color = cell_colors[3]
            else:
                color = cell_colors[0]

            canvas.create_rectangle((x1, y1), (x2, y2), fill=color)

    canvas.pack()
    root.mainloop()


def set_kuka(binar_map):

    binar_map[0][0] = 2
    binar_map[LENGTH-1][WIDTH-1] = 3
    binar_map[LENGTH-2][WIDTH-1] = 3
    binar_map[LENGTH-1][WIDTH-2] = 3

    return binar_map


def set_obj(map_zero):
    '''

    :param map_zero: binar np arr
    :return: matrix with obj
    '''

    global LENGTH
    global WIDTH

    seed(42)

    for _ in range(OBJ_COUNT):
        leng = randint(1, 10)
        width = randint(1, 10)
        # map[row_pos][row_pos + leng]
        row_pos = randint(0, LENGTH - leng)
        col_pos = randint(0, WIDTH - width)

        for row in range(leng):
            for col in range(width):
                map_zero[(row_pos + row)][(col + col_pos)] = 1
                # print((row_pos + row), (col + col_pos))

    return map_zero


map = np.zeros([LENGTH, WIDTH], dtype=int)

map = set_obj(map)
map = set_kuka(map)
# print(map)
do_graphic(map)
