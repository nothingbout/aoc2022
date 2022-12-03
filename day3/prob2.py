import fileinput

def calc_priority(c):
    if c >= 'a' and c <= 'z':
        return 1 + ord(c) - ord('a')
    if c >= 'A' and c <= 'Z':
        return 27 + ord(c) - ord('A')

lines = []
for line in fileinput.input():
    lines.append(line.strip())

total_priority = 0

for i in range(0, len(lines), 3):
    for j in range(0, len(lines[i])):
        c = lines[i][j]
        if lines[i + 1].find(c) >= 0 and lines[i + 2].find(c) >= 0:
            total_priority += calc_priority(c)
            break

print(total_priority)

