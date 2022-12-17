from datetime import datetime
import itertools

input_file = 'input.txt'

class Grid:
    def __init__(self, rows):
        self.rows = list(rows)

    def __str__(self):
        return f'Grid({self.rows})'
    __repr__ = __str__

    def pretty_print(self):
        for y in range(self.height() - 1, -1, -1):
            # print(self.rows[y])
            print(''.join(map(str, self.rows[y])))
        print('')

    def width(self):
        return len(self.rows[0])
    
    def height(self):
        return len(self.rows)

    def ensure_height(self, height, default_value):
        while self.height() < height:
            self.rows.append([default_value] * self.width())

    def get(self, x, y):
        return self.rows[y][x]

    def set(self, x, y, value):
        self.rows[y][x] = value

    def shape_in_bounds(self, shape, pos):
        pos_x, pos_y = pos
        if pos_x < 0 or pos_y < 0: return False
        if pos_x + shape.width() > self.width(): return False
        if pos_y + shape.height() > self.height(): return False
        return True

    def shape_overlaps(self, shape, pos):
        pos_x, pos_y = pos
        for y in range(shape.height()):
            for x in range(shape.width()):
                if shape.get(x, y) > 0 and self.get(pos_x + x, pos_y + y) > 0:
                    return True
        return False

    def draw(self, shape, pos, value):
        pos_x, pos_y = pos
        for y in range(shape.height()):
            for x in range(shape.width()):
                if shape.get(x, y) > 0:
                    self.set(pos_x + x, pos_y + y, value)

def make_grid(width, height, value):
    rows = []
    for _ in range(height): rows.append([value] * width)
    return Grid(rows)

def parse_pieces():
    with open('pieces.txt', 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    pieces = []
    piece_rows = []
    for line in lines:
        if len(line) == 0:
            if len(piece_rows) > 0: 
                pieces.append(Grid(reversed(piece_rows)))
                piece_rows = []
        else:
            piece_rows.append([1 if c == '#' else 0 for c in line])
    
    if len(piece_rows) > 0: 
        pieces.append(Grid(reversed(piece_rows)))
    return pieces

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    for line in lines:
        return [c for c in line]

pieces = parse_pieces()
jets = parse_input()

# for piece in pieces:
#     print(piece.pretty_print())
# print(jets)

grid = make_grid(7, 10, 0)


jet_index = 0
piece_index = 0
piece_pos = (2, 3)
highest_piece = 0
stopped_pieces = 0

while stopped_pieces < 2022:
    piece = pieces[piece_index]
    pos_x, pos_y = piece_pos
    stop = False

    # if True:
    #     grid.draw(piece, piece_pos, 1)
    #     grid.pretty_print()
    #     grid.draw(piece, piece_pos, 0)

    new_x = pos_x - 1 if jets[jet_index] == '<' else pos_x + 1
    if not grid.shape_in_bounds(piece, (new_x, pos_y)): 
        new_x = pos_x
    elif grid.shape_overlaps(piece, (new_x, pos_y)):
        new_x = pos_x

    new_y = pos_y - 1
    if new_y < 0 or grid.shape_overlaps(piece, (new_x, new_y)): # check overlap too
        new_y = pos_y
        stop = True

    if stop:
        grid.draw(piece, (new_x, new_y), 1)
        highest_piece = max(highest_piece, new_y + piece.height())
        stopped_pieces += 1
        piece_index = (piece_index + 1) % len(pieces)
        piece_pos = (2, highest_piece + 3)
        grid.ensure_height(piece_pos[1] + 4, 0)
    else:
        piece_pos = (new_x, new_y)
    jet_index = (jet_index + 1) % len(jets)

# grid.pretty_print()

print(highest_piece)