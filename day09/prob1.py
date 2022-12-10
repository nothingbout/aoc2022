input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]
        moves = []
        for line in lines:
            parts = line.split()
            moves.append((parts[0], int(parts[1])))
        return moves


moves = parse_input()
print(moves)

state = ((0,0), (0,0))
tail_visited = set()
tail_visited.add((0, 0))

for move_dir, move_steps in moves:
    for _ in range(move_steps):
        (head_x, head_y), (tail_x, tail_y) = state
        if move_dir == 'R': head_x += 1
        elif move_dir == 'U': head_y += 1
        elif move_dir == 'L': head_x -= 1
        elif move_dir == 'D': head_y -= 1

        dx = head_x - tail_x
        if abs(dx) == 2:
            tail_x += 1 if dx > 0 else -1
            if abs(tail_y - head_y) == 1: tail_y = head_y

        dy = head_y - tail_y
        if abs(dy) == 2:
            tail_y += 1 if dy > 0 else -1
            if abs(tail_x - head_x) == 1: tail_x = head_x

        tail_visited.add((tail_x, tail_y))
        state = ((head_x, head_y), (tail_x, tail_y))

print(len(tail_visited))