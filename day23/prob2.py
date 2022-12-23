from datetime import datetime
import functools
import itertools
import time
import math

input_file = 'input.txt'

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

    elf_positions = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                elf_positions.append((x, y))
    return elf_positions

def get_neighbor(pos, n):
    offsets = [(0,-1), (0,1), (-1,0), (1,0)]
    return v_add(pos, offsets[n])

def get_adjacent_in_dir(pos, n):
    match n:
        case 0: offsets = [(-1,-1), (0,-1), (1,-1)]
        case 1: offsets = [(-1,1), (0,1), (1,1)]
        case 2: offsets = [(-1,1), (-1,0), (-1,-1)]
        case 3: offsets = [(1,1), (1,0), (1,-1)]
    return list(map(lambda x: v_add(pos, x), offsets))

def get_all_adjacent(pos):
    return get_adjacent_in_dir(pos, 0) + get_adjacent_in_dir(pos, 1) + [get_neighbor(pos, 2), get_neighbor(pos, 3)]

def get_elf_bounds(elf_positions):
    bounds_min = functools.reduce(lambda a, b: v_min(a, b), elf_positions)
    bounds_max = v_add(functools.reduce(lambda a, b: v_max(a, b), elf_positions), (1, 1))
    return bounds_min, bounds_max

def print_elves(elf_positions, bounds = None):
    if bounds is None:
        bounds_min, bounds_max = get_elf_bounds(elf_positions)
    else:
        bounds_min, bounds_max = bounds
    for y in range(bounds_min[1], bounds_max[1]):
        s = ''
        for x in range(bounds_min[0], bounds_max[0]):
            if (x, y) in elf_positions:
                s += '#'
            else: 
                s += '.'
        print(s)
    print('')

start_time = datetime.now()

elf_positions = set(parse_input())
# print(elf_positions)

print_bounds = ((0, 0), (5, 6))
# print_elves(elf_positions, print_bounds)

round = 0
while True:
    dst_positions = {}
    propose_counts = {}

    for elf_pos in elf_positions:
        consider_moving = False
        for adj_pos in get_all_adjacent(elf_pos):
            if adj_pos in elf_positions:
                consider_moving = True
                break

        propose_dir = None
        if consider_moving:
            for i in range(4):
                valid = True
                dir = (i + round) % 4
                for adj_pos in get_adjacent_in_dir(elf_pos, dir):
                    if adj_pos in elf_positions:
                        valid = False
                        break
                if valid:
                    propose_dir = dir
                    break

        if propose_dir is not None:
            dst_pos = get_neighbor(elf_pos, propose_dir)
            dst_positions[elf_pos] = dst_pos
            propose_counts[dst_pos] = propose_counts.get(dst_pos, 0) + 1

    moved_count = 0
    new_elf_positions = set()
    for elf_pos in elf_positions:
        dst_pos = dst_positions.get(elf_pos, None)
        moved = False
        if dst_pos is not None:
            if propose_counts[dst_pos] == 1:
                moved = True
                moved_count += 1
                new_elf_positions.add(dst_pos)

        if not moved:
            new_elf_positions.add(elf_pos)

    elf_positions = new_elf_positions
    print(f'End of round {round + 1}, moved: {moved_count}')
    if moved_count == 0: break
    round += 1
    # print_elves(elf_positions, print_bounds)


# bounds_min, bounds_max = get_elf_bounds(elf_positions)
# bounds_size = v_sub(bounds_max, bounds_min)
# bounds_cells = functools.reduce(lambda x, y: x * y, bounds_size)
# print(bounds_cells - len(elf_positions))

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
