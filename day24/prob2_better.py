from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = 'example_input.txt' if IS_EXAMPLE else 'input.txt'

def parse_input():
    with open(INPUT_FILE, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    map_rows = [line[1:-1] for line in lines[1:-1]]
    return map_rows

def get_neighbor(pos, n):
    offsets = [(1,0), (0,-1), (-1,0), (0,1)]
    return tuple(map(lambda a, b: a + b, pos, offsets[n]))

def get_end_pos(map_rows, goal_num):
    if goal_num % 2 == 1: return (0, -1)
    return (len(map_rows[0]) - 1, len(map_rows))

def is_valid_pos(map_rows, pos, minute):
    x, y = pos
    if x < 0 or x >= len(map_rows[0]): return False
    if y < 0 or y >= len(map_rows): return False
    if map_rows[y][(x - minute) % len(map_rows[0])] == '>': return False
    if map_rows[y][(x + minute) % len(map_rows[0])] == '<': return False
    if map_rows[(y + minute) % len(map_rows)][x] == '^': return False
    if map_rows[(y - minute) % len(map_rows)][x] == 'v': return False
    return True

start_time = datetime.now()

map_rows = parse_input()
print(f'{len(map_rows)} x {len(map_rows[0])}')
# print(map_rows)

elf_positions = set([(0, -1)])
minute = 0
goal_num = 0
while True:
    # print(f'min: {minute}')
    # print(elf_positions)

    new_positions = set()
    minute += 1

    finished = False
    for pos in elf_positions:
        if is_valid_pos(map_rows, pos, minute) or (pos == get_end_pos(map_rows, goal_num - 1)):
            new_positions.add(pos)
        for n in range(4):
            n_pos = get_neighbor(pos, n)
            
            if n_pos == get_end_pos(map_rows, goal_num):
                finished = True
            elif is_valid_pos(map_rows, n_pos, minute):
                new_positions.add(n_pos)

    if finished:
        if goal_num == 2: break
        new_positions = set([get_end_pos(map_rows, goal_num)])
        goal_num += 1

    elf_positions = new_positions
    if len(elf_positions) == 0: raise Exception("empty set")

print(minute)

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
