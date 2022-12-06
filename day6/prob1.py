import fileinput

lines = [line.rstrip() for line in fileinput.input()]

for line in lines:
    for i in range(4, len(line)):
        marker = line[i - 4:i]
        if len(set(marker)) == 4:
            print(i)
            break
    