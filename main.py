import numpy as np
import tkinter as tk
import tkinter.font as tk_font
import time

txt = open('examp_6.txt')
data = []
coord_parameters = []

# for line in txt:
#     # print(line)
#     coord_parameters.append(line[:line.find("; ")].split(', '))
#     data.append(line[line.find("; ") + 2:-1].split(', '))
#
# coord_parameters = np.array(coord_parameters, dtype=np.float64)
# data = np.array(data, dtype=np.float64)

alf = 0.006  # rads
txt = open('examp_6.txt')
data = []
coord_parameters = []

d_alf = 0
dx = 0
dy = 0
minx = 1000

for line in txt:
    # print(line)
    coord_parameters.append(line[:line.find("; ")].split(', '))
    data.append(line[line.find("; ") + 2:-1].split(', '))

coord_parameters = np.array(coord_parameters, dtype=np.float64)
data = np.array(data, dtype=np.float64)

def no_infinity(rad):
    if rad != 5.6:
        return True
    elif rad == 5.6:
        return False


def angle_calc(data, x_start, y_start, x_new, y_new, angle_start, angle_new):
    global d_alf
    global dx
    global dy
    global minx

    lenght = 130
    middle = 56
    map = np.zeros([lenght, lenght], dtype=str)
    map[middle][middle] = '9'

    dx += x_new - x_start # смещение по оси Ох
    dy += y_new - y_start
    d_alf += -round(angle_new - angle_start, 3)
    posy = angle_new - angle_start > 0


    # 4th
    for n, rad in enumerate(data[:83]):
        if no_infinity(rad):
            # print(rad)
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            # смещение угла
            if posy:
                angle += d_alf
            else:
                angle -= d_alf

            y = int(round(np.sin(angle) * rad + dy))
            # print(f'np.sin(angle) * rad : {np.sin(angle) * rad}')
            # print(f'np.sin(angle) * rad + dy : {y}')

            x = int(round(np.cos(angle) * rad + dx))
            map[y + middle][x + middle] = '4'

            if x + middle < minx:
                minx = x + middle
        else:
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            if posy:
                angle += d_alf
            else:
                angle -= d_alf

            y = int(round(np.sin(angle) * rad + dy))
            x = int(round(np.cos(angle) * rad + dx))
            map[y + middle][x + middle] = ' '

    # 1st
    for n, rad in enumerate(data[84:340]):
        if no_infinity(rad):
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            if posy:
                angle += d_alf
            else:
                angle -= d_alf
            y = int(round(- np.sin(angle) * rad - dy))
            x = int(round(np.cos(angle) * rad + dx))
            map[y + middle][x + middle] = '1'

            if x + middle < minx:
                minx = x + middle
        else:
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            if posy:
                angle -= d_alf
            else:
                angle += d_alf

            y = int(round(np.sin(angle) * rad + dy))
            x = int(round(np.cos(angle) * rad + dx))
            map[y + middle][x + middle] = ' '

    # 2rd
    for n, rad in enumerate(data[341:597]):
        if no_infinity(rad):
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            if posy:
                # print(f'd_alf : {d_alf}')
                angle += d_alf
                # print(f'angle : {angle}')

            else:
                angle -= d_alf

            y = int(round(- np.cos(angle) * rad - dy))
            x = int(round(- np.sin(angle) * rad - dx))
            map[y + middle][x + middle] = '2'

            if x + middle < minx:
                minx = x + middle
        else:
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            if posy:
                angle += d_alf
            else:
                angle -= d_alf

            y = int(round(np.sin(angle) * rad + dy))
            x = int(round(np.cos(angle) * rad + dx))
            map[y + middle][x + middle] = ' '

    # 3rd
    for n, rad in enumerate(data[598:]):
        if no_infinity(rad):
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            if posy:
                angle += d_alf
            else:
                angle -= d_alf

            y = int(round(np.sin(angle) * rad + dy))
            x = int(round(- np.cos(angle) * rad - dx))
            map[y + middle][x + middle] = '3'

            if x + middle < minx:
                minx = x + middle
        else:
            rad = round(rad, 3) * 10
            angle = (n + 1) * alf

            if posy:
                angle += d_alf
            else:
                angle -= d_alf

            y = int(round(np.sin(angle) * rad + dy))
            x = int(round(np.cos(angle) * rad + dx))
            map[y + middle][x + middle] = ' '

    print(f'd_alf : {d_alf}')

    for i in range(len(map)):
        for j in range(len(map[i])):
            if len(map[i][j]) == 0: map[i][j] = ' '

    map[middle][middle] = '9'
    for _ in range(1):
        map[int(middle + 1 + dy)][int(middle + dx)] = '8'
        map[int(middle - 1 + dy)][int(middle + dx)] = '8'
        map[int(middle + dy)][int(middle + 1 + dx)] = '9'
        map[int(middle + dy)][int(middle - 1 + dx)] = '9'

    print(minx)

    return map


def scan_iter(iter):

    if iter == 0:
        # поворот
        angle_start = coord_parameters[iter][2]
        angle_new = angle_start
        # смещение по осям
        y_start = coord_parameters[iter][1]
        x_start = coord_parameters[iter][0]
        y_new = y_start
        x_new = x_start

    else:
        angle_start = coord_parameters[iter - 1][2]
        angle_new = coord_parameters[iter][2]

        y_start = coord_parameters[iter - 1][1]
        x_start = coord_parameters[iter - 1][0]
        y_new = coord_parameters[iter][1]
        x_new = coord_parameters[iter][0]

    bool_map = angle_calc(data[iter], x_start, y_start, x_new, y_new, angle_start, angle_new)

    return bool_map


def do_graphic(bool_map):
    ROOM_LENGTH = len(bool_map[0]) #x
    ROOM_WIDTH = len(bool_map) #y
    CELL_SIZE = 4

    root = tk.Tk()
    root.wm_geometry("+0+0")
    root.configure(bg='#96AFB9', relief='groove')
    canvas = tk.Canvas()

    canvas = tk.Canvas(root, width=CELL_SIZE * ROOM_LENGTH, height=CELL_SIZE * ROOM_WIDTH, bg='#96AFB9')
    # canvas.grid(row=4)

    cell_colors = ['white', 'black', 'red']
    ci = 0  # color index
    color = ''

    for i in range(ROOM_LENGTH): #bool_map[0]
        for j in range(ROOM_WIDTH): #bool_map
            x1, y1 = i * CELL_SIZE, j * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

            if bool_map[j][i] != ' ' and bool_map[j][i] != '8' and bool_map[j][i] != '9':
                color = cell_colors[0]
            elif bool_map[j][i] == '8' or bool_map[j][i] == '9':
                color = cell_colors[2]
            else:
                color = cell_colors[1]

            canvas.create_rectangle((x1, y1), (x2, y2), fill=color)
            # canvas.create_rectangle((x1+1, y1), (x2+1, y2), fill=color)
            # canvas.create_rectangle((x1-1, y1), (x2-1, y2), fill=color)
            # canvas.create_rectangle((x1, y1+1), (x2, y2+1), fill=color)
            # canvas.create_rectangle((x1, y1-1), (x2, y2-1), fill=color)



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

#bool_map
"""
    ввести фильтр
    ввести уменьшение значимости
    дополнить перемещение красного по осям
    убрать шум
    изменить направление вычета
"""
# scan_map
# for scan in range(len(data)):
for scan in range(5):

    if scan == 0:
        scan_map = scan_iter(scan) # вся карта с учётом предыдущих сканов

        LENGTH = len(scan_map[0])  # x
        WIDTH = len(scan_map)  # y

    else:
        bool_map = scan_iter(scan)
        for row in range(WIDTH): # итерация сканов
            for col in range(LENGTH): # итерация точек
                if scan_map[row][col] == ' ' and bool_map[row][col] != ' ':
                    if bool_map[row+1][col] == ' ' and bool_map[row][col+1] == ' ' and bool_map[row-1][col] == ' ' and bool_map[row][col-1] == ' ':
                        # print('MATCH!')
                        scan_map[row][col] = bool_map[row][col]

        print(f'scan: {scan}')

do_graphic(scan_map)