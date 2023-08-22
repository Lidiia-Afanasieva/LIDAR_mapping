import tkinter as tk
from random import randint, seed
import numpy as np
from math import inf, dist
from binar_map import * 


"""
    RRT
"""

class Map:

    def do_graphic(self,):
        # global self.  # x
        # global WIDTH  # y
        global CELL_SIZE

        root = tk.Tk()
        root.geometry("+700+85")
        root.configure(bg='#96AFB9', relief='groove')
        # canvas = tk.Canvas()

        canvas = tk.Canvas(root, width=CELL_SIZE * self.col, height=CELL_SIZE * self.row, bg='#96AFB9')
        # canvas.grid(row=4)

        cell_colors = ['black', 'red', 'white', 'blue', 'yellow', 'orange', 'green', 'purple', 'gray', 'brown']
        # ci = 0  # color index
        # color = ''

        for i in range(self.col):  # bool_map[0]
            for j in range(self.row):  # bool_map
                row1, col1 = i * CELL_SIZE, j * CELL_SIZE
                row2, col2 = row1 + CELL_SIZE, col1 + CELL_SIZE

                if self.map[j][i] == 1:
                    color = cell_colors[1]
                elif self.map[j][i] == 2:
                    color = cell_colors[2]
                elif self.map[j][i] == 3:
                    color = cell_colors[3]
                elif self.map[j][i] == 4:
                    color = cell_colors[4]
                elif self.map[j][i] == 5:
                    color = cell_colors[5]
                else:
                    color = cell_colors[0]
                if j == self.endpos[0] and i == self.endpos[1]:
                    color = cell_colors[3]
                elif j == self.startpos[0] and i == self.startpos[1]:
                    color = cell_colors[2]

                canvas.create_rectangle((row1, col1), (row2, col2), fill=color)

        canvas.pack()
        root.mainloop()

    def set_kuka(self):
        self.map[self.startpos[0]][self.startpos[1]] = 2
        self.map[self.endpos[0]][self.endpos[1]] = 3

    def set_obj(self):
        """
        :param map_zero: binar np arr
        :return: matrix with obj
        """
        seed(42)

        for _ in range(self.obj_count):
            leng = randint(1, 10)
            width = randint(1, 10)
            # map[row_pos][row_pos + leng]
            row_pos = randint(0, self.row - leng)
            col_pos = randint(0, self.col - width)

            for row in range(leng):
                for col in range(width):
                    self.map[(row_pos + row)][(col + col_pos)] = 1

    '''
        map = np.zeros([LENGTH, WIDTH], dtype=int)
        map = set_obj(map)
        map = set_kuka(map)
    '''

    def add_vert(self, row, col):
        # print(row, col)
        self.map[row][col] = 4

    def add_path(self, row, col):
        # print(row, col)
        self.map[row][col] = 4

    def __init__(self, row, col, OBJ_COUNT):
        self.row = row
        self.col = col
        self.obj_count = OBJ_COUNT

        self.startpos = (0, 0)
        self.endpos = (self.row - 10, self.col - 10)

        self.map = np.zeros([self.row, self.col], dtype=int)
        self.set_obj()
        self.set_kuka()


def set_point(iter_v, rand_v):
    O_x = rand_v[1] - iter_v[1]  # col
    O_y = rand_v[0] - iter_v[0]  # row

    if O_x > -1 and O_y > -1:
        if O_x < O_y and O_x / O_y < 0.3: return 0, 2
        elif O_x > O_y and O_y / O_x < 0.3: return 2, 0
        else: return 1, 1
    elif O_x < 1 and O_y > -1:
        O_x = abs(O_x)
        if O_x < O_y and O_x / O_y < 0.3: return 0, 2
        elif O_x > O_y and O_y / O_x < 0.3: return -2, 0
        else: return -1, 1
    elif O_x < 1 and O_y < 1:
        O_x = abs(O_x)
        O_y = abs(O_y)
        if O_x < O_y and O_x / O_y < 0.3: return 0, -2
        elif O_x > O_y and O_y / O_x < 0.3: return -2, 0
        else: return -1, -1
    elif O_x > -1 and O_y < 1:
        O_y = abs(O_y)
        if O_x < O_y and O_x / O_y < 0.3: return 0, -2
        elif O_x > O_y and O_y / O_x < 0.3: return 2, 0
        else: return 1, -1


def check_root(orda, delta, iter_v, map):
    # print('check row', iter_v[1] + (delta // 2), iter_v[0])
    if orda == 'row' and map[iter_v[0] + (delta // 2)][iter_v[1]] != 0:
        return True
    elif orda == 'col' and map[iter_v[0]][iter_v[1] + (delta // 2)] != 0:
        return True


def wall_is_broken(iter_v, dcol, drow, map):
    if iter_v[0] + drow > len(map) or iter_v[0] + drow < 0: return True
    if iter_v[1] + dcol > len(map[0]) or iter_v[1] + dcol < 0: return True
    if map[iter_v[0] + drow][iter_v[1] + dcol] == 1:
        return True
    else:
        return False


def nearest(G, vex, map):
    Nvex = None
    Nidx = None
    min_row = None
    min_col = None
    minDist = float("inf")

    for idx, v in enumerate(G.vertices):
        dcol, drow = set_point(v, vex)
        print(dcol, drow, ' = ', v, vex)

        if wall_is_broken(v, dcol, drow, map):
            continue
        if abs(drow) == 2 and check_root('row', drow, v, map):
            continue
        elif abs(dcol) == 2 and check_root('col', dcol, v, map):
            continue

        dist = get_manhattan_distance(v, vex)
        if dist < minDist:
            min_row = drow
            min_col = dcol
            minDist = dist
            Nidx = idx
            Nvex = v

    return Nvex, Nidx, min_row, min_col


def RRT(startpos, endpos, map, n_iter):
    graph = Graph(startpos, endpos)

    for _ in range(n_iter):
        randvex = graph.random_position()
        # print(f'randvex: {randvex}')
        # if isInObstacle(randvex, map, radius):
        #     continue
        nearvex, nearidx, drow, dcol = nearest(G, randvex, map)
        # print('more inf', nearvex, nearidx, drow, dcol)
        # print(f'to nearest drow: {drow}')
        # print(f'to nearest dcol: {dcol}')
        if nearvex is None:
            continue
        # print(f'nearvex[0] + drow = {nearvex[0]} + {drow}')
        # print(f'nearvex[1] + dcol = {nearvex[1]} + {dcol}')
        newvex = (nearvex[0] + drow, nearvex[1] + dcol)
        # add_path(nearvex, drow, dcol)
        # print('/newvex', newvex)

        if dcol == 0:
            graph.path.append((nearvex[0] + (drow // 2), nearvex[1] + dcol))
        elif drow == 0:
            graph.path.append((nearvex[0] + drow, nearvex[1] + (dcol // 2)))
        # G.path.append(path_point)

        newidx = graph.add_vex(newvex)
        dist = get_manhattan_distance(newvex, nearvex)
        graph.add_edge(newidx, nearidx, dist)

        dist = get_manhattan_distance(newvex, graph.endpos)
        if dist < 2:
            endidx = graph.add_vex(graph.endpos)
            graph.add_edge(newidx, endidx, dist)
            graph.success = True
            print('success')
            break
    return graph


# discrete_map = Map(row, col, OBJ_COUNT)
# discrete_map.do_graphic()
#
# rrt_graph = RRT(discrete_map.startpos, discrete_map.endpos, discrete_map.map, 1000)
# for vert in rrt_graph.vertices:
#     discrete_map.add_vert(vert[0], vert[1])
# print(rrt_graph.path)
# for path in rrt_graph.path:
#     discrete_map.add_path(path[0], path[1])
#
# discrete_map.do_graphic()