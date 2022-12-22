from datetime import datetime
import functools
import itertools
import time
import math

is_example = False
input_file = 'example_input.txt' if is_example else 'input.txt'

def v_set(a, idx, value):
    if idx < 0 or idx >= len(a): raise Exception(f'index out of bounds: len(a) == {len(a)}, idx == {idx}')
    return a[0:idx] + (value,) + a[idx+1 : len(a)]
def v_check(a, b):
    if isinstance(b, tuple):
        if len(a) != len(b): raise Exception(f'length mismatch: len(a) == {len(a)}, len(b) == {len(b)}')
        return True
    return False
def v_add(a, b): return tuple(map(lambda x, y: x + y, a, b)) if v_check(a, b) else tuple(map(lambda x: x + b, a))
def v_sub(a, b): return tuple(map(lambda x, y: x - y, a, b)) if v_check(a, b) else tuple(map(lambda x: x - b, a))
def v_mul(a, b): return tuple(map(lambda x, y: x * y, a, b)) if v_check(a, b) else tuple(map(lambda x: x * b, a))
def v_div(a, b): return tuple(map(lambda x, y: x / y, a, b)) if v_check(a, b) else tuple(map(lambda x: x / b, a))
def v_floor(a): return tuple(map(math.floor, a))
def v_ceil(a): return tuple(map(math.ceil, a))
def v_min(a, b): return tuple(map(lambda x, y: min(x, y), a, b)) if v_check(a, b) else None
def v_max(a, b): return tuple(map(lambda x, y: max(x, y), a, b)) if v_check(a, b) else None

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

def map_to_cube_pos(pos):
    x, y = pos
    for side in range(6):
        side_x, side_y = v_sub(pos, CUBE_SIDE_ORIGINS[side])
        # print(f'{side_x}, {side_y} ({CUBE_DIM})')
        if side_x < 0 or side_x >= CUBE_DIM: continue
        if side_y < 0 or side_y >= CUBE_DIM: continue
        return (side, (side_x, side_y))
    raise Exception(f'did not find cube side for map pos: {pos}')

def cube_to_map_pos(map_pos):
    side, pos = map_pos
    return v_add(CUBE_SIDE_ORIGINS[side], pos)

def cube_wrap(src_side, src_pos, src_heading):
    # print(f'wrap-src {src_side}, {src_pos}, {src_heading}')
    dst_side, dst_heading, invert = CUBE_SIDE_WRAPS[src_side][src_heading]

    src_coord = src_pos[1] if src_heading == 0 or src_heading == 2 else src_pos[0]
    dst_coord = CUBE_DIM - 1 - src_coord if invert else src_coord

    match dst_heading:
        case 0: dst_pos = (0, dst_coord) # come from left
        case 1: dst_pos = (dst_coord, 0) # come from up
        case 2: dst_pos = (CUBE_DIM - 1, dst_coord) # come from right
        case 3: dst_pos = (dst_coord, CUBE_DIM - 1) # come from down
    # print(f'wrap-dst {dst_side}, {dst_pos}, {dst_heading}')
    return dst_side, dst_pos, dst_heading

def move_pos(map_pos, heading):
    side, (x, y) = map_to_cube_pos(map_pos)
    match heading:
        case 0: x += 1
        case 1: y += 1
        case 2: x -= 1
        case 3: y -= 1

    if x < 0 or y < 0 or x >= CUBE_DIM or y >= CUBE_DIM:
        side, (x, y), heading = cube_wrap(side, (x, y), heading)
    return cube_to_map_pos((side, (x, y))), heading

if is_example:
    CUBE_DIM = 4
    CUBE_SIDE_ORIGINS = [v_mul(x, CUBE_DIM) for x in [ (2,0), (0,1), (1,1), (2,1), (2,2), (3,2) ]]
    CUBE_SIDE_WRAPS = [
        # dst_side, dst_heading, invert coord
        [ (5, 2, True), (3, 1, False), (2, 1, False), (3, 1, True) ], # 0
        [ (2, 0, False), (4, 3, True), (5, 3, True), (0, 1, True) ], # 1
        [ (3, 0, False), (4, 0, True), (2, 2, False), (0, 0, False) ], # 2
        [ (5, 1, True), (4, 1, False), (2, 2, False), (0, 3, False) ], # 3
        [ (5, 0, False), (1, 3, True), (2, 3, True), (3, 3, False) ], # 4
        [ (0, 2, True), (1, 0, True), (4, 2, False), (3, 2, True) ], # 5
    ]
else:
    CUBE_DIM = 50
    CUBE_SIDE_ORIGINS = [v_mul(x, CUBE_DIM) for x in [ (1,0), (2,0), (1,1), (0,2), (1,2), (0,3) ]]
    CUBE_SIDE_WRAPS = [
        # dst_side, dst_heading, invert coord
        [ (1, 0, False), (2, 1, False), (3, 0, True), (5, 0, False) ], # 0
        [ (4, 2, True), (2, 2, False), (0, 2, False), (5, 3, False) ], # 1
        [ (1, 3, False), (4, 1, False), (3, 1, False), (0, 3, False) ], # 2
        [ (4, 0, False), (5, 1, False), (0, 0, True), (2, 0, False) ], # 3
        [ (1, 2, True), (5, 2, False), (3, 2, False), (2, 3, False) ], # 4
        [ (4, 3, False), (1, 1, False), (0, 1, False), (3, 3, False) ], # 5
    ]

# print(CUBE_SIDE_ORIGINS)

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
            next_pos, next_heading = move_pos(cur_pos, cur_heading)
            if map_get(map_rows, next_pos) == 1: 
                # print(f'blocked: {map_to_cube_pos(next_pos)}, heading: {next_heading}')
                break
            cur_pos, cur_heading = (next_pos, next_heading)
            # print(f'move-dst {map_to_cube_pos(cur_pos)}, heading: {cur_heading}')

print(4 * (cur_pos[0] + 1) + 1000 * (cur_pos[1] + 1) + cur_heading)

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
