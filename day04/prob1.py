import fileinput

total = 0

for line in fileinput.input():
    line = line.strip()
    ranges = [[int(x) for x in r.split('-')] for r in line.split(',')]

    if ranges[0][0] <= ranges[1][0] and ranges[0][1] >= ranges[1][1]:
        total += 1
    elif ranges[1][0] <= ranges[0][0] and ranges[1][1] >= ranges[0][1]:
        total += 1

print(total)
