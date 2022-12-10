input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

        commands = []
        for line in lines:
            parts = line.split()
            if len(parts) == 1:
                commands.append((parts[0], None))
            else:
                commands.append((parts[0], int(parts[1])))

        return commands


commands = parse_input()
# print(commands)

memory = 1
cmd_cycles = 0

pixels = ''
crt_cycles = 0

signal_str = 0

for cmd in commands:
    op, value = cmd
    match op:
        case 'noop': 
            cmd_cycles += 1
            new_memory = memory
        case 'addx':
            cmd_cycles += 2
            new_memory = (memory + value)

    while crt_cycles < cmd_cycles:
        x = memory if cmd_cycles > crt_cycles else new_memory

        row_pixel_index = crt_cycles % 40
        pixels += '#' if row_pixel_index >= x - 1 and row_pixel_index <= x + 1 else '.'

        crt_cycles += 1

    memory = new_memory

for y in range(6):
    print(pixels[y * 40 : y * 40 + 40])