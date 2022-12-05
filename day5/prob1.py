import fileinput

lines = list(fileinput.input())

for i in range(0, len(lines)):
    if lines[i].startswith(' 1 '):
        stacks_count = len(lines[i].split())
        stack_lines = lines[:i]
        op_lines = lines[i + 2:]
        break

stacks = [[] for _ in range(0, stacks_count)]

for line in reversed(stack_lines):
    for i in range(0, stacks_count):
        label = line[1 + i * 4]
        if len(label.strip()) > 0:
            stacks[i].append(label)

for line in op_lines:
    parts = line.split()
    count = int(parts[1])
    src = int(parts[3]) - 1
    dst = int(parts[5]) - 1

    for _ in range(0, count):
        stacks[dst].append(stacks[src].pop())

print(''.join([stack[-1] if len(stack) > 0 else '' for stack in stacks]))

