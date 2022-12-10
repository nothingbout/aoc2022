import fileinput

total = 0

for line in fileinput.input():
    line = line.strip()
    ranges = [[int(x) for x in r.split('-')] for r in line.split(',')]

    if ranges[0][1] < ranges[1][0] or ranges[0][0] > ranges[1][1]:
        pass
    else:
        total += 1

print(total)
