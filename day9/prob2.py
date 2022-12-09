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
# print(moves)

state = [(0,0)] * 10
tail_visited = set()
tail_visited.add((0, 0))

for move_dir, move_steps in moves:
    for _ in range(move_steps):
        head_x, head_y = state[0]
        if move_dir == 'R': head_x += 1
        elif move_dir == 'U': head_y += 1
        elif move_dir == 'L': head_x -= 1
        elif move_dir == 'D': head_y -= 1
        state[0] = (head_x, head_y)

        for i in range(1, len(state)):
            head_x, head_y = state[i - 1]
            tail_x, tail_y = state[i]
            
            dx = head_x - tail_x
            dy = head_y - tail_y

            if abs(dx) == 2:
                tail_x += 1 if dx > 0 else -1
                if abs(dy) == 1: tail_y = head_y

            if abs(dy) == 2:
                tail_y += 1 if dy > 0 else -1
                if abs(dx) == 1: tail_x = head_x

            state[i] = (tail_x, tail_y)

        tail_visited.add(state[-1])

print(len(tail_visited))