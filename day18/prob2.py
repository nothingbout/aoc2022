from datetime import datetime
import itertools

input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    cubes = []
    for line in lines:
        cubes.append(tuple([int(x) for x in line.split(',')]))
    return cubes

def get_neighbor(pos, n):
    x, y, z = pos
    match n:
        case 0: return (x - 1, y, z)
        case 1: return (x + 1, y, z)
        case 2: return (x, y - 1, z)
        case 3: return (x, y + 1, z)
        case 4: return (x, y, z - 1)
        case 5: return (x, y, z + 1)

def in_bounds(bounds_min, bounds_max, pos):
    x, y, z = pos
    if x < bounds_min[0] or y < bounds_min[1] or z < bounds_min[2]: return False
    if x > bounds_max[0] or y > bounds_max[1] or z > bounds_max[2]: return False
    return True

def fill_get(cubes, bounds_min, bounds_max, visited, start_pos):
    visited.add(start_pos)
    queue = [start_pos]
    while len(queue) > 0:
        curr_pos = queue.pop(0)
        
        for n in range(6):
            n_pos = get_neighbor(curr_pos, n)
            if not in_bounds(bounds_min, bounds_max, n_pos): continue
            if n_pos in visited: continue
            if n_pos in cubes: continue
            visited.add(n_pos)
            queue.append(n_pos)

    return visited

cubes = parse_input()
# print(cubes)

bounds_min = (100, 100, 100)
bounds_max = (-100, -100, -100)
for cube in cubes:
    bounds_min = (min(cube[0] - 1, bounds_min[0]), min(cube[1] - 1, bounds_min[1]), min(cube[2] - 1, bounds_min[2]))
    bounds_max = (max(cube[0] + 1, bounds_max[0]), max(cube[1] + 1, bounds_max[1]), max(cube[2] + 1, bounds_max[2]))

# print(bounds_min)
# print(bounds_max)

cubes = set(cubes)
outside_cells = fill_get(cubes, bounds_min, bounds_max, set(), bounds_min)

area = 0
for cube in cubes:
    for n in range(6):
        n_pos = get_neighbor(cube, n)
        if n_pos in outside_cells:
            area += 1

print(area)
