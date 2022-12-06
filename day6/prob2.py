import fileinput

lines = [line.rstrip() for line in fileinput.input()]
n = 14

for line in lines:
    for i in range(n, len(line)):
        marker = line[i - n:i]
        if len(set(marker)) == n:
            print(i)
            break
    