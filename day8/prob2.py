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

highest_score = 0

for orig_y in range(grid_height):
    for orig_x in range(grid_width):
        orig_height = tree_grid[orig_y][orig_x]

        score1 = 0
        for x in range(orig_x - 1, -1, -1): 
            score1 += 1
            if tree_grid[orig_y][x] >= orig_height: 
                is_visible = False
                break

        score2 = 0
        for x in range(orig_x + 1, grid_width): 
            score2 += 1
            if tree_grid[orig_y][x] >= orig_height: 
                is_visible = False
                break

        score3 = 0
        for y in range(orig_y - 1, -1, -1): 
            score3 += 1
            if tree_grid[y][orig_x] >= orig_height: 
                is_visible = False
                break
                
        score4 = 0
        for y in range(orig_y + 1, grid_height): 
            score4 += 1
            if tree_grid[y][orig_x] >= orig_height: 
                is_visible = False
                break

        score = score1 * score2 * score3 * score4
        if score > highest_score: highest_score = score
        print(f'{orig_x}, {orig_y}: {score1} {score2} {score3} {score4} -> {score}')

print(highest_score)