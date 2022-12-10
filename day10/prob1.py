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
cycle = 0
check_cycles = [20, 60, 100, 140, 180, 220]
check_cycles_index = 0

signal_str = 0

for cmd in commands:
    op, value = cmd
    match op:
        case 'noop': 
            cycle += 1
            new_memory = memory
        case 'addx':
            cycle += 2
            new_memory = (memory + value)

    if check_cycles_index < len(check_cycles):
        check_cycle = check_cycles[check_cycles_index]
        if cycle >= check_cycle:
            x = memory if cycle > check_cycle else new_memory
            signal_str += memory * check_cycle
            check_cycles_index += 1

    memory = new_memory

print(signal_str)