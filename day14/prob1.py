import itertools

input_file = 'input.txt'

class Input:
    def __init__(self):
        self.formations = []

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    input = Input()
    for line in lines:
        points = []
        for part in line.split(' -> '):
            c = part.split(',')
            points.append((int(c[0]), int(c[1])))
        input.formations.append(points)

    return input

def get_formation_points(formation):
    points = []
    x, y = formation[0]
    points.append((x, y))
    for nx, ny in formation[1:]:
        while x != nx or y != ny:
            if x < nx: x += 1
            elif x > nx: x -= 1
            elif y < ny: y += 1
            elif y > ny: y -= 1
            points.append((x, y))
    return points

input = parse_input()
# print(input.formations)

occupied_points = set()
for formation in input.formations:
    occupied_points.update(get_formation_points(formation))

max_formation_y = -1
for _, y in occupied_points:
    if max_formation_y < 0 or y > max_formation_y: 
        max_formation_y = y

# print(occupied_points)
# print(max_formation_y)

rest_count = 0
while True:
    did_come_to_rest = False
    sand_x, sand_y = (500, 0)
    while sand_y < max_formation_y:
        # print(f'{sand_x},{sand_y}')
        if not (sand_x, sand_y + 1) in occupied_points:
            sand_y += 1
        elif not (sand_x - 1, sand_y + 1) in occupied_points:
            sand_x -= 1
            sand_y += 1
        elif not (sand_x + 1, sand_y + 1) in occupied_points:
            sand_x += 1
            sand_y += 1
        else:
            did_come_to_rest = True
            occupied_points.add((sand_x, sand_y))
            break

    if did_come_to_rest:
        rest_count += 1
    else:
        break

print(rest_count)