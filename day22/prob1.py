from datetime import datetime
import functools
import itertools
import time
import math

input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    map_rows = []
    for line in lines[:-2]:
        margin = 0
        cells = []
        for c in line:
            if c == '.': cells.append(0)
            elif c == '#': cells.append(1)
            else:
                if len(cells) > 0: raise Exception("wtf")
                margin += 1
        map_rows.append((margin, cells))

    path = []
    for g in itertools.groupby(lines[-1], key=lambda x: x in '0123456789'):
        if g[0]: path.append(int(''.join(g[1])))
        else: path.extend(g[1])

    return map_rows, path

def map_row_min(map_row):
    return map_row[0]

def map_row_max(map_row):
    return map_row[0] + len(map_row[1])

def map_get(map_rows, pos):
    x, y = pos
    return map_rows[y][1][x - map_rows[y][0]]

def next_row_where_x_in_range(map_rows, pos, y_offset):
    x, y = pos
    while True:
        y = (y + y_offset) % len(map_rows)
        if x >= map_row_min(map_rows[y]) and x < map_row_max(map_rows[y]): return y
        if y == pos[1]: raise Exception("infinite loop")

def move_pos(map_rows, pos, heading):
    x, y = pos
    match heading:
        case 0: 
            x += 1
            if x >= map_row_max(map_rows[y]): x = map_row_min(map_rows[y])
        case 2:
            x -= 1
            if x < map_row_min(map_rows[y]): x = map_row_max(map_rows[y]) - 1
        case 1:
            y = next_row_where_x_in_range(map_rows, pos, 1)
        case 3:
            y = next_row_where_x_in_range(map_rows, pos, -1)
    return (x, y)            

start_time = datetime.now()

map_rows, path_instructions = parse_input()
# print(map_rows)
# print(path_instructions)

start_pos = (map_rows[0][0], 0)
start_heading = 0

heading_offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]

cur_pos, cur_heading = (start_pos, start_heading)
for instruction in path_instructions:
    # print(instruction)
    if instruction == 'L':
        cur_heading = (cur_heading - 1) % 4
    elif instruction == 'R':
        cur_heading = (cur_heading + 1) % 4
    else:
        for _ in range(instruction):
            next_pos = move_pos(map_rows, cur_pos, cur_heading)
            if map_get(map_rows, next_pos) == 1: break
            cur_pos = next_pos
            # print(f'{cur_pos} ({cur_heading})')

print(4 * (cur_pos[0] + 1) + 1000 * (cur_pos[1] + 1) + cur_heading)

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
