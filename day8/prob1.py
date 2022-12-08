input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    tree_grid = []
    for line in lines:
        tree_grid.append([int(t) for t in line])        

    return tree_grid

def print_grid(grid):
    for row in grid:
        print(' '.join([str(c) for c in row]))

tree_grid = parse_input()
grid_width = len(tree_grid[0])
grid_height = len(tree_grid)
print_grid(tree_grid)

total_visible = 0

for orig_y in range(grid_height):
    for orig_x in range(grid_width):
        orig_height = tree_grid[orig_y][orig_x]

        is_visible = True
        for x in range(0, orig_x): 
            if tree_grid[orig_y][x] >= orig_height: 
                is_visible = False
                break
        if is_visible: 
            total_visible += 1
            continue

        is_visible = True
        for x in range(orig_x + 1, grid_width): 
            if tree_grid[orig_y][x] >= orig_height: 
                is_visible = False
                break
        if is_visible: 
            total_visible += 1
            continue

        is_visible = True
        for y in range(0, orig_y): 
            if tree_grid[y][orig_x] >= orig_height: 
                is_visible = False
                break
        if is_visible: 
            total_visible += 1
            continue
                
        is_visible = True
        for y in range(orig_y + 1, grid_height): 
            if tree_grid[y][orig_x] >= orig_height: 
                is_visible = False
                break
        if is_visible: 
            total_visible += 1
            continue

print(total_visible)