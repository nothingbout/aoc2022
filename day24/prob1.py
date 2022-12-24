from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = 'example_input.txt' if IS_EXAMPLE else 'input.txt'

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
    with open(INPUT_FILE, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    map_rows = []
    for line in lines[1:-1]:
        row = []
        for c in line[1:-1]:
            match c:
                case '>': row.append((True, False, False, False))
                case '^': row.append((False, True, False, False))
                case '<': row.append((False, False, True, False))
                case 'v': row.append((False, False, False, True))
                case _: row.append((False, False, False, False))
        map_rows.append(row)
    return map_rows

def get_neighbor(map_rows, pos, n, wrap):
    offsets = [(1,0), (0,-1), (-1,0), (0,1)]
    nx, ny = v_add(pos, offsets[n])
    if wrap: return (nx % len(map_rows[0]), ny % len(map_rows))
    else: return (nx, ny)

def map_get(map_rows, pos):
    x, y = pos
    return map_rows[y][x]

def next_map(map_rows):
    new_rows = []
    for y in range(len(map_rows)):
        new_row = []
        for x in range(len(map_rows[0])):
            new_row.append((
                map_get(map_rows, get_neighbor(map_rows, (x, y), 2, True))[0], # >
                map_get(map_rows, get_neighbor(map_rows, (x, y), 3, True))[1], # ^
                map_get(map_rows, get_neighbor(map_rows, (x, y), 0, True))[2], # <
                map_get(map_rows, get_neighbor(map_rows, (x, y), 1, True))[3]  # v
                ))
        new_rows.append(new_row)
    return new_rows

def is_end_pos(map_rows, pos):
    x, y = pos
    return  x == len(map_rows[0]) - 1 and y == len(map_rows)

def is_valid_pos(map_rows, pos):
    x, y = pos
    if is_end_pos(map_rows, pos): return True
    if x < 0 or x >= len(map_rows[0]): return False
    if y < 0 or y >= len(map_rows): return False
    if any(map_rows[y][x]): return False
    return True

def print_map(map_rows):
    for row in map_rows:
        s = ''
        for c in row:
            count = sum(map(lambda x: 1 if x else 0, c))
            if count > 1: s += str(count)
            elif c[0]: s += '>'
            elif c[1]: s += '^'
            elif c[2]: s += '<'
            elif c[3]: s += 'v'
            else: s += '.'
        print(s)
    print('')

start_time = datetime.now()

map_rows = parse_input()
print(f'{len(map_rows)} x {len(map_rows[0])}')
# print(map_rows)

elf_positions = set([(0, -1)])
minute = 0
while True:
    # print(f'min: {minute}')
    # print(elf_positions)
    # print_map(map_rows)

    new_positions = set()
    new_map_rows = next_map(map_rows)

    finished = False
    for pos in elf_positions:
        if is_end_pos(new_map_rows, pos):
            finished = True
            break

        if is_valid_pos(new_map_rows, pos):
            new_positions.add(pos)
        for n in range(4):
            n_pos = get_neighbor(new_map_rows, pos, n, False)
            # print(n_pos)
            if is_valid_pos(new_map_rows, n_pos):
                new_positions.add(n_pos)

    if finished: break
    if len(new_positions) == 0: raise Exception("empty set")

    minute += 1
    map_rows = new_map_rows
    elf_positions = new_positions

print(minute)

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
