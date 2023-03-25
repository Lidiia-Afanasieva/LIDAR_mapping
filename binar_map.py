import tkinter as tk
from random import randint, seed
import numpy as np
from math import inf, dist

col = 60
row = 60
OBJ_COUNT = 20
CELL_SIZE = 10

max_speed = 2
spread_area = list(range(col))


def random_color():
    de = ("%02x" % randint(0, 255))
    re = ("%02x" % randint(0, 255))
    we = ("%02x" % randint(0, 255))
    ge = "#"
    color = ge + de + re + we

    return color


def get_manhattan_distance(p_1, p_2):
    return sum(abs(ord_1 - ord_2) for ord_1, ord_2 in zip(p_1, p_2))


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


class Graph:
    def __init__(self, startpos, endpos):
        self.startpos = startpos
        self.endpos = endpos

        self.vertices = [startpos]  # список координат всех вершин
        self.edges = []  # связи-пары вершин
        self.path = []  # координаты ячеек пути
        self.success = False

        self.vex2idx = {startpos: 0}  # поиск индекса вершины по координатам
        self.neighbors = {0: []}  # ключ-индекс вершины, значение-[индекс соседней вершины, расстояние до неё]
        self.parent = {(0,0): (0,0)}

        self.open_list = [startpos, ]
        self.closed_list = []
        self.idx_g = {0: 0, }
        self.idx_f_open = {}
        self.idx_f_closed = {}

    def add_vex(self, pos):
        try:
            idx = self.vex2idx[pos]  # проверка наличия вершины в этой точке
        except:
            idx = len(self.vertices)  # добавляет индекс вершине
            self.vertices.append(pos)  # добавляет координату вершины в масс верш
            self.vex2idx[pos] = idx  # обратный поиск координат по вершине
            self.neighbors[idx] = []  # добавление массива соседей этой вершины
        return idx  # индекс вершины в графе

    def add_edge(self, idx1, idx2, cost):
        self.edges.append((idx1, idx2))
        self.neighbors[idx1].append((idx2, cost))
        self.neighbors[idx2].append((idx1, cost))

    def random_position(self):  # )
        posrow = randint(0, row - 2)  # x=50
        poscol = randint(0, col - 2)  # y=60
        return posrow, poscol

    def h(self, node):
        return int(dist(node, self.endpos))

    def g(self, node, mother_node_idx, his_star_pos):
        g_mom = self.idx_g[mother_node_idx]
        return g_mom + get_sucer_distance(his_star_pos)

    def f(self, node, mother_node_idx, his_star_pos):
        g = self.g(node, mother_node_idx, his_star_pos)
        return g + self.h(node), g


"""
    RRT
"""


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