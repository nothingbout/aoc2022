input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    heightmap = []
    for y in range(len(lines)):
        line = lines[y]
        heights = []
        for x in range(len(line)):
            c = line[x]
            if c == 'S':
                startpos = (x, y)
                heights.append(0)
            elif c == 'E':
                endpos = (x, y)
                heights.append(ord('z') - ord('a'))
            else:
                heights.append(ord(c) - ord('a'))
        heightmap.append(heights)

    return (heightmap, startpos, endpos)

def get_neighbor(x, y, n):
    match n:
        case 0: return (x + 1, y)
        case 1: return (x, y + 1)
        case 2: return (x - 1, y)
        case 3: return (x, y - 1)

def is_valid(x, y, w, h):
    return x >= 0 and x < w and y >= 0 and y < h

heightmap, startpos, endpos = parse_input()
# print(heightmap)
# print(startpos)
# print(endpos)

grid_width = len(heightmap[0])
grid_height = len(heightmap)

minsteps_grid = []
for y in range(grid_height):
    minsteps_grid.append([-1] * grid_width)

search_positions = [startpos]
minsteps_grid[startpos[1]][startpos[0]] = 0

while len(search_positions) > 0:
    x, y = search_positions.pop(0)
    steps = minsteps_grid[y][x]
    height = heightmap[y][x]

    for n in range(4):
        nx, ny = get_neighbor(x, y, n)
        if not is_valid(nx, ny, grid_width, grid_height): continue

        dst_height = heightmap[ny][nx]
        if dst_height - height > 1: continue

        dst_steps = minsteps_grid[ny][nx]       
        if dst_steps < 0 or steps + 1 < dst_steps:
            minsteps_grid[ny][nx] = steps + 1
            search_positions.append((nx, ny))
        
print(minsteps_grid[endpos[1]][endpos[0]])

