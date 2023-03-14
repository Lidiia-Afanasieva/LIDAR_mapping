import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import tkinter.font as tk_font
import time
import random

alf = 0.0062  # rads
txt = open('examp6 (1).txt')
data = []
coord_parameters_ = []

d_alf = 0
dx = 0
dy = 0

x = []
y = []

x_p = []
y_p = []

LENGTH = 502
MIDDLE = 0

map = np.zeros([LENGTH, LENGTH], dtype=int)
map[MIDDLE][MIDDLE] = -2

for line in txt:
    # print(line)
    coord_parameters_.append(line[:line.find("; ")].split(', '))
    data.append(line[line.find("; ") + 2:-1].split(', '))

coord_parameters = np.array(coord_parameters_, dtype=np.float64)
data = np.array(data, dtype=np.float64)

angle_start = coord_parameters[0][2]
y_start = coord_parameters[0][0]
x_start = coord_parameters[0][1]


def get_start_pos(scan, new_angle):
    """
    :param scan:
    :param new_angle:
    :return: вернёт массив позиций на полярном скане с учётом смещения
    смещается по рабочей окружности на длину равную количество радиано-точек в угле
    при уменьшении угла смещения точка смещается против часовой стрелки, иначе по
    """
    start_pos = []
    dif = (angle_start - new_angle) / alf
    # print(f'd_phi : {dif}')
    pos = 0

    for n, point in enumerate(scan):
        if dif > 0:
            pos = int(n + abs(dif))
            if pos - 173 > 1024:
                # print('!!!!!!!')
                # print('!!!!!!!')
                # print('REVERS')
                # print('!!!!!!!')
                # print('!!!!!!!')

                # pos = pos - 1024
                pos = 0
                print(pos)
                # pos = abs(pos) - 1024  # decision of overflowing
            # start_pos.append(int(n + abs(dif)))  # can be overflowing
            # print(f'point new pos : {n + abs(dif)}')
        else:
            # print(f'n : {n}')
            pos = int(n - abs(dif))
            if pos + 173 < 0:
                # print('!!!!!!!')
                # print('!!!!!!!')
                # print('REVERS')
                # print('!!!!!!!')
                # print('!!!!!!!')
                pos = 0
                # pos = 1024 + pos#
                print(pos)

                # pos = 1024 - abs(pos) + 173
            # start_pos.append(int(n - abs(dif)))
        start_pos.append(pos)

    return start_pos


def get_check(arr):
    """

    :param arr: список порядка точек скана
    :return: проверка выхода за круг
    """
    for item in arr:
        if abs(item) > 1024:
            print(item)
            # print('get_check !FAILED!')
            return False
    # print('get_check !PASSED!')
    return True


def no_infinity(rad):
    if rad != 5.6 and rad > 0.35:
        return True
    elif rad == 5.6 or rad < 0.35:
        return False


def forth_qtr(rad, n):
    """

    :param rad: порядок точки на полярной окружности со смещением
    :return:
    """
    global map

    if no_infinity(rad):
        # print(rad)
        # print('FORTH')
        rad = rad
        # print(rad)# переводит в десятки радиан
        angle = (n) * alf

        x = np.sin(angle) * rad + dx
        y = -np.cos(angle) * rad + dy
        # print(f'x: {x}, y: {y}')
        # print(f'dx: {dx}, dy: {dy}')

        try:
            # map[y + MIDDLE][x + MIDDLE] = 1
            return [x + MIDDLE, y + MIDDLE]
        except Exception:
            return [MIDDLE, MIDDLE]
    else:
        return [MIDDLE, MIDDLE]


def first_qtr(rad, n):
    global map

    if no_infinity(rad):
        # print(rad)
        # print('FIRST')
        # rad = round(rad,3)   # переводит в десятки радиан
        angle = (n) * alf

        x = np.sin(angle) * rad + dx
        y = -np.cos(angle) * rad + dy
        # print(f'x: {x}, y: {y}')
        # print(f'dx: {dx}, dy: {dy}')

        try:
            # map[y + MIDDLE][x + MIDDLE] = 1
            return [x + MIDDLE, y + MIDDLE]
        except Exception:
            return [MIDDLE, MIDDLE]
    else:
        return [MIDDLE, MIDDLE]


def second_qtr(rad, n):
    global map

    if no_infinity(rad):
        # print('SECOND')
        rad = rad  # переводит в десятки радиан
        angle = (n) * alf

        x = np.sin(angle) * rad + dx
        y = -np.cos(angle) * rad + dy
        # print(f'x: {x}, y: {y}')
        # print(f'dx: {dx}, dy: {dy}')

        try:
            # map[y + MIDDLE][x + MIDDLE] = 1
            return [x + MIDDLE, y + MIDDLE]
        except Exception:
            return [MIDDLE, MIDDLE]
    else:
        return [MIDDLE, MIDDLE]


def third_qtr(rad, n):
    global map

    if no_infinity(rad):
        # print(rad)
        # print('THIRD')
        rad = rad  # переводит в десятки радиан
        angle = n * alf

        x = np.sin(angle) * rad + dx
        y = -np.cos(angle) * rad + dy
        # print(f'x: {x}, y: {y}')
        # print(f'dx: {dx}, dy: {dy}')

        try:
            # map[y + MIDDLE][x + MIDDLE] = 1
            return [x + MIDDLE, y + MIDDLE]
        except Exception:
            return [MIDDLE, MIDDLE]
    else:
        return [MIDDLE, MIDDLE]


def return_pose(scan, x_new, y_new, new_angle):
    global map
    global d_alf
    global dx
    global dy
    global minx

    global x
    global y
    global x_p
    global y_p

    global angle_start
    global y_start
    global x_start
    # plt.figure(figsize=(15, 10))
    temp = []

    dy = (x_new - x_start)#*0.01  # смещение по оси Ох
    dx = (y_new - y_start)#*0.01
    # d_alf = -round(new_angle - angle_start, 5)


    homecomming_pos = get_start_pos(scan, new_angle)
    # ax.axis([0, 1, 0, 1])

    if get_check(homecomming_pos):

        for point in range(len(scan)):
            # for point in [200,]:
            #     print(f'point :, type :{type(point)}')
            # print(f'point :{point}, new point :{homecomming_pos[point]}')
            # print(point)
            if 0 <= homecomming_pos[point] + 173 < 256:
                pass
                # try:
                temp = forth_qtr(scan[point], homecomming_pos[point])
                x.append(temp[0])
                y.append(temp[1])
                # # print('!!!!!!!!!!', forth_qtr(scan[point], homecomming_pos[point]))
                # # except Exception:
                # #     pass
                # # ax.plot(temp[0], temp[1])
            elif 256 < homecomming_pos[point] + 173 < 512:

                # try:
                #     x.append, y.append = first_qtr(scan[point], homecomming_pos[point])
                # except Exception:
                #     pass
                temp = first_qtr(scan[point], homecomming_pos[point])
                x.append(temp[0])
                y.append(temp[1])
                # ax.plot(temp[0], temp[1])
            elif 512 < homecomming_pos[point] + 173 < 768:
            #
            #     # try:
            #     #     x.append, y.append = second_qtr(scan[point], homecomming_pos[point])
            #     # except Exception:
            #     #     pass
                temp = second_qtr(scan[point], homecomming_pos[point])
                x.append(temp[0])
                y.append(temp[1])
            #     # ax.plot(temp[0], temp[1])
            elif 768 < homecomming_pos[point] + 173 < 1024:

                # try:
                #     x.append, y.append =
                # except Exception:
                #     pass
                temp = third_qtr(scan[point], homecomming_pos[point])
                x.append(temp[0])
                y.append(temp[1])

            # elif homecomming_pos[point] + 173 < 0:
            #     temp = third_qtr(scan[point], homecomming_pos[point])
            #     x.append(temp[0])
            #     y.append(temp[1])

    # print(y)

    map[MIDDLE][MIDDLE] = -2
    # for _ in range(1):
    map[int(MIDDLE + 1 - dy)][int(MIDDLE + dx)] = -1
    map[int(MIDDLE - 1 - dy)][int(MIDDLE + dx)] = -1
    map[int(MIDDLE - dy)][int(MIDDLE + 1 + dx)] = -2
    map[int(MIDDLE - dy)][int(MIDDLE - 1 + dx)] = -2

    # ax_p = plt.axes()
    y_p.append(MIDDLE + dy)
    x_p.append(MIDDLE + dx)

    # ax_p.scatter(x_p, y_p, c='b')

    # ax = plt.axes()
    # plt.plot(int(MIDDLE + 1 - dy, int(MIDDLE + dx)))
    # plt.plot(int(MIDDLE - 1 - dy, int(MIDDLE + dx)))
    # plt.plot(int(MIDDLE - 1 - dy, int(MIDDLE + 1 + dx)))
    # plt.plot(int(MIDDLE - 1 - dy, int(MIDDLE - 1 + dx)))
    # ax.plot(int(MIDDLE + 1 - dy, int(MIDDLE + dx)))
    # plt.xlabel(r'$x$')
    # plt.ylabel(r'$f(x)$')
    # ax.scatter(y, x, linewidths=0.3, c='r')
    # plt.pause(0.001)
    # plt.show()
    return map



def scan_iter(iter):
    # angle_start = coord_parameters[0][2]
    # y_start = coord_parameters[0][0]
    # x_start = coord_parameters[0][1]

    if iter == 0:
        # поворот
        # angle_start = coord_parameters[iter][2]
        angle_new = angle_start
        # смещение по осям
        # reversed!!!!!!!!!! 09.03
        # y_start = coord_parameters[iter][0]
        # x_start = coord_parameters[iter][1]
        y_new = y_start
        x_new = x_start

    else:
        # angle_start = coord_parameters[iter - 1][2]
        angle_new = coord_parameters[iter][2]

        # y_start = coord_parameters[iter - 1][0]
        # x_start = coord_parameters[iter - 1][1]
        y_new = coord_parameters[iter][0]
        x_new = coord_parameters[iter][1]

    bool_map = return_pose(data[iter], x_new, y_new, angle_new)

    return bool_map


def random_color():
    de = ("%02x" % random.randint(0, 255))
    re = ("%02x" % random.randint(0, 255))
    we = ("%02x" % random.randint(0, 255))
    ge = "#"
    color = ge + de + re + we

    return color


def do_graphic(bool_map):
    ROOM_LENGTH = len(bool_map[0])  # x
    ROOM_WIDTH = len(bool_map)  # y
    CELL_SIZE = 2

    root = tk.Tk()
    root.wm_geometry("+0+0")
    root.configure(bg='#96AFB9', relief='groove')
    canvas = tk.Canvas()

    canvas = tk.Canvas(root, width=CELL_SIZE * ROOM_LENGTH, height=CELL_SIZE * ROOM_WIDTH, bg='#96AFB9')
    # canvas.grid(row=4)

    cell_colors = ['black', 'red', 'white', 'blue', 'yellow', 'orange', 'green', 'purple', 'gray', 'brown']
    ci = 0  # color index
    color = ''

    for i in range(ROOM_LENGTH):  # bool_map[0]
        for j in range(ROOM_WIDTH):  # bool_map
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

    # root.update_idletasks()
    # root.update()
    # time.sleep(0.5)
    # canvas.destroy()
    # root.destroy()


###############################
'''
    MAIN
'''
###############################

# bool_map
"""
    ввести фильтр
    ввести уменьшение значимости
    дополнить перемещение красного по осям
    убрать шум
    изменить направление вычета
    
    09.03
    O_y error
    
    11.03
    возврат по точкам
"""

kernel = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 0, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1]])
plt.figure(figsize=(8, 8))
ax = plt.axes()

# scan_map
# for scan in range(len(data)):
for scan in range(40):

    if scan == 0:
        scan_map = scan_iter(scan)  # вся карта с учётом предыдущих сканов

        LENGTH = len(scan_map[0])  # x
        WIDTH = len(scan_map)  # y

    else:
        bool_map = scan_iter(scan)
        for row in range(WIDTH):  # итерация сканов
            for col in range(LENGTH):  # итерация точек
                if scan_map[row][col] == 0 and bool_map[row][col] == 1:
                    # if bool_map[row + 1][col] == '0' and bool_map[row][col + 1] == '0' \
                    #         and bool_map[row - 1][col] == '0' and bool_map[row][col - 1] == '0':
                    # print('MATCH!')
                    # exhausted = scan_map[row - 2:row + 5, col - 2:col + 5]
                    #
                    # if np.sum(exhausted * kernel) < 3:
                    #     scan_map[row][col] = bool_map[row][col]
                    scan_map[row][col] = bool_map[row][col]

        print(f'scan: {scan}')
ax.scatter(x, y, linewidths=0.3, c='black')
ax.scatter(x_p, y_p, linewidths=0.3, c='red')
plt.show()
# plt.pause(0.001)
# do_graphic(scan_map)
'''
    не поворячивает угол при подсчёте синуса в месте 
'''