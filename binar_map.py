import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import tkinter.font as tk_font
import time
import random

LENGTH = 50
WIDTH = 50
OBJ_COUNT = 4


def random_color():
    de = ("%02x" % random.randint(0, 255))
    re = ("%02x" % random.randint(0, 255))
    we = ("%02x" % random.randint(0, 255))
    ge = "#"
    color = ge + de + re + we

    return color


def do_graphic(bool_map):
    LENGTH = len(bool_map[0])  # x
    WIDTH = len(bool_map)  # y
    CELL_SIZE = 2

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

            if bool_map[j][i] != 0 and bool_map[j][i] != -1 and bool_map[j][i] != -2:
                # itura = int(bool_map[j][i]) + 2
                color = random_color()

            elif bool_map[j][i] == -1 or bool_map[j][i] == -2:
                color = cell_colors[1]
            else:
                color = cell_colors[0]

            canvas.create_rectangle((x1, y1), (x2, y2), fill=color)

    canvas.pack()
    root.mainloop()


def set_obj(map):
    '''

    :param map: zero/1 matrix
    :return: matrix with obj
    '''
    for iter in range(OBJ_COUNT):
        len = random.random(1, 5, int)
    pass

map = np.zeros([LENGTH, LENGTH], dtype=int)

set_obj(map)