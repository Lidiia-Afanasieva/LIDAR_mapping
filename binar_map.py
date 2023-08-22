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
