import tkinter as tk
from random import randint, seed
import numpy as np
from math import inf, dist
from binar_map import * 

"""
    A*

    TO DO:
    __________________________________________________
    в классе графа создать два массива open_v, closed_v
    в открытый добавить ноду старта
    создать функцию подсчёта f, для стартовой ноды g=0
    создать словарь f {индекс вершины: значение функции f}
    __________________________________________________
    взять вершину с минимальным f в цикле
    создать фильтр 8 точек окружения
    хранить все 8 точек где?
    убрать родительскую вершину из открытых
    __________________________________________________
    содать цикл для всех восьми дочерних точек
    сделать проверку: если точка - эндпоз, остановиться
    иначе: подсчитать f  и занести результат в словарь
    __________________________________________________
    проверка на наличие меньшего f с вершиной с такой же координатой в открытом
    если да: скипнуть суккесер
    иначе: если в закрытом есть такая же вершина с меньшим f(надо ли считать f??) скипнуть суккесер
    | не надо, в закрытом по умолчанию посчитанные ноды
    иначе иначе: добавить суккесер в открытый
    порасширять массивы класса на суккесер


"""


class Map:

    def do_graphic(self, ):
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
                    self.obj_list.append(((row_pos + row), (col + col_pos)))

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
        self.map[row][col] = 6

    def add_stars(self, starss):
        # print(row, col)
        for star in starss:
            self.map[star[0]][star[1]] = 4

    def check_point(self, node):
        if node[0] < 0 or node[1] < 0:
            return True
        if node[0] > self.row - 1 or node[1] > self.col - 1:
            return True
        if node in self.obj_list:
            return True
        return False

    def __init__(self, row, col, OBJ_COUNT):
        self.row = row
        self.col = col
        self.obj_count = OBJ_COUNT

        self.startpos = (0, 0)
        self.endpos = (self.row - 10, self.col - 10)
        self.obj_list = []

        self.map = np.zeros([self.row, self.col], dtype=int)
        self.set_obj()
        self.set_kuka()

def _get_8_successors(mother_node):
    return mother_node[row - 1:row + 2, col - 1:col + 2]


def get_8_successors(mother_node):
    r = mother_node[0]
    c = mother_node[1]
    return [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
            (r, c - 1), (r, c + 1),
            (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]


def get_sucer_distance(idx):
    # star_positions = [4, 2, 4, 2, 2, 4, 2, 4]
    # star_positions = [1, 2, 1, 2, 2, 1, 2, 1]
    star_positions = [1, 1, 1, 1, 1, 1, 1, 1]
    return star_positions[idx]


def A_star():
    discrete_map = Map(row, col, OBJ_COUNT)
    discrete_map.do_graphic()
    astar_graph = Graph(discrete_map.startpos, discrete_map.endpos)
    astar_graph.idx_f_open[0] = 0
    print(f'startpos: {discrete_map.startpos}, endpose: {discrete_map.endpos}')
    iter = 0

    # for _ in range(1000):
    while astar_graph.open_list and not astar_graph.success:
    #     print(f'iter: {iter}')
        # print(f'idx_f_open at the start: {astar_graph.idx_f_open}')
        min_vert_idx = min(astar_graph.idx_f_open, key=astar_graph.idx_f_open.get)
        min_vert = astar_graph.vertices[min_vert_idx]
        # print(f'min_vert: {min_vert}')
        # print(f'min_vert_idx: {min_vert_idx}')
        # min_vert_idx = astar_graph.vex2idx[min_vert]
        astar_graph.open_list.remove(min_vert)
        # astar_graph.idx_f_open
        astar_graph.idx_f_open[min_vert_idx] = inf
        successors = get_8_successors(min_vert)
        # successors = [suc for r in successors for suc in r if suc!=None]
        for his_star_pos, successor in enumerate(successors):
            if discrete_map.check_point(successor):
                continue
            else:
                if successor == discrete_map.endpos:
                    print('SUCCESS')

                    # successor_idx = len(astar_graph.vertices)
                    # astar_graph.parent[successor] = min_vert
                    # astar_graph.vex2idx[successor] = successor_idx
                    #
                    # stared_path = []
                    # current = successor
                    # print(astar_graph.parent)
                    # while successor is not astar_graph.startpos:
                    #     print(f'successor: {successor}')
                    #     stared_path.append(successor)
                    #     # successor_idx = astar_graph.vex2idx[successor]
                    #     # print(astar_graph.vex2idx.values(178))
                    #     print(astar_graph.parent)
                    #     old = successor
                    #     successor = astar_graph.parent[successor]
                    #     astar_graph.parent[old] = None

                        # print(stared_path)
                    discrete_map.add_stars(astar_graph.closed_list)
                    discrete_map.do_graphic()
                    astar_graph.success = True
                    return 'cool'  # Return reversed path
                    # break
                else:
                    successor_f, successor_g = astar_graph.f(successor, min_vert_idx, his_star_pos)
                    # print(f'successor_f: {successor_f}, successor_g: {successor_g}')
                    try:
                        clone_idx = astar_graph.vex2idx[successor]
                        # print(f'clone id : {clone_idx} and successor : {successor} and successor id : {successor_idx}')
                        if successor_f >= astar_graph.idx_f_open[clone_idx]:
                            # print(f'!passing the successor with open_list: {successor}')
                            continue
                        if successor_f >= astar_graph.idx_f_closed[clone_idx]:
                            # print(f'!passing the successor with closed_list: {successor}')
                            continue
                        # print(f'successor_f : {successor_f} aaaaand clone: {astar_graph.idx_f_closed[clone_idx]}')
                    except:
                        pass
                    successor_idx = len(astar_graph.vertices)
                    astar_graph.idx_g[successor_idx] = successor_g
                    astar_graph.parent[successor] = min_vert
                    # print(astar_graph.idx_g)
                    astar_graph.vertices.append(successor)
                    astar_graph.vex2idx[successor] = successor_idx
                    astar_graph.neighbors[min_vert_idx] = [successor_idx, get_manhattan_distance(successor, min_vert)]
                    astar_graph.open_list.append(successor)
                    astar_graph.idx_f_open[successor_idx] = successor_f
        astar_graph.closed_list.append(min_vert)
        astar_graph.idx_f_closed[min_vert_idx] = astar_graph.idx_f_open[min_vert_idx]
        astar_graph.idx_f_open[min_vert_idx] = inf
        # print(f'open_list after {iter} iter: {astar_graph.open_list}')
        # print(f'closed_list after {iter} iter: {astar_graph.closed_list}')
        iter += 1
    for v in astar_graph.closed_list:
        discrete_map.map[v[0]][v[1]] = 4
    # print(astar_graph.closed_list)
    discrete_map.do_graphic()
    return 'NOT_FOUND'

astar_graph = A_star()