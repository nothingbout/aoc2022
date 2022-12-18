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


cubes = parse_input()
# print(cubes)

area = 0
cubes = set(cubes)
for cube in cubes:
    for n in range(6):
        n_pos = get_neighbor(cube, n)
        if not n_pos in cubes:
            area += 1

print(area)