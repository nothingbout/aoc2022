import fileinput

def calc_priority(c):
    if c >= 'a' and c <= 'z':
        return 1 + ord(c) - ord('a')
    if c >= 'A' and c <= 'Z':
        return 27 + ord(c) - ord('A')

total_priority = 0

for line in fileinput.input():
    line = line.strip()
    per_count = int(len(line)/2)
    comp1 = line[:per_count]
    comp2 = line[per_count:]

    for i in range(0, per_count):
        c = comp1[i]
        if comp2.find(c) >= 0:
            total_priority += calc_priority(c)
            break

print(total_priority)

